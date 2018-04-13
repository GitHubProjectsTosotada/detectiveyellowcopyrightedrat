#!/usr/bin/python3

from telethon import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import ChannelParticipantsSearch, Updates, UpdateShortMessage, UpdateNewMessage, InputPeerEmpty, Chat, Channel, InputChannel, InputFileLocation, ChannelParticipantsAdmins
from telethon.utils import get_input_media

import logging
import json
import web
import time
import sys, os, re
from urllib.parse import parse_qs
import random
import string
import shelve
import http.server
import socketserver
import requests
from threading import Thread

sys.path.append(sys.path[0] + "/../")
from storagemethods import getUser, isActiveInGroup, existsGroup, getGymsByActivity
from config import config

# Logging
logdir = sys.path[0] + "/logs"
if not os.path.exists(logdir):
    os.makedirs(logdir)
logging.basicConfig(filename=logdir+'/debug.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.info("--------------------- Starting admintools! -----------------------")

urls = (
    '/auth', 'auth',
    '/logout', 'logout',
    '/getchats', 'getchats',
    '/getparticipants/([0-9]+)', 'getparticipants',
    '/getnotvalidated/([0-9]+)', 'getnotvalidated',
    '/getteams/([0-9]+)', 'getteams',
    '/getinactive/([0-9]+)/([0-9]+)', 'getinactive',
    '/getgyms/([0-9]+)/([0-9]+)', 'getgyms'
)

cachedir = sys.path[0] + "/cache"

web.config.debug = False
session = None


def get_post(web):
    rawdata = str(web.data())[2:-1]
    return parse_qs(rawdata)

class auth:
    def POST(self):
        data = get_post(web)
        if not hasattr(session,"appstring"):
            session.appstring = os.path.realpath(os.path.dirname(__file__)) + '/tgsessions/' + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15)) + '.session'
        logging.info("admintools:auth:POST: Telegram session at %s" % session.appstring)
        if "telephone" in data:
            # Sanitize phone
            if re.match("\+[0-9]{11,16}$",data['telephone'][0]) is None:
                return "badphone"
            # This operation is expensive, throttle
            if not throttle_status_ok(web):
                return "pleasecooldown"
            client = TelegramClient(session.appstring, config["admintools"]["apiid"], config["admintools"]["apihash"], update_workers=1)
            if client.connect() != True:
                return "cantconnect"
            if not client.is_user_authorized():
                # Check code
                if not "code" in data or not hasattr(session,"codehash"):
                    # Check recaptcha
                    if not 'g-recaptcha-response' in data:
                        return "norecaptcha"
                    else:
                        recode = data['g-recaptcha-response'][0]
                        reurl = "https://www.google.com/recaptcha/api/siteverify"
                        r = requests.post(reurl, {
                            "secret": config["admintools"]["recaptchasecret"],
                            "response": recode
                        })
                        recaptcha_reply = r.json()
                        if recaptcha_reply["success"] is not True:
                            return "badrecaptcha"
                    try:
                        coderesult = client.send_code_request(data['telephone'][0])
                        session.codehash = coderesult.phone_code_hash
                        return "checkphone"
                    except:
                        return "cantsendcode"
                else:
                    client.sign_in(data['telephone'][0], data["code"][0], phone_code_hash=session.codehash)
                    if client.is_user_authorized():
                        session.client_id = str(client.get_me().id)
                        return "ok_signedin"
                    else:
                        return "badcode"
            else:
                session.client_id = str(client.get_me().id)
                return "ok_alreadyauthorized"
        else:
            return web.internalerror()

class logout:
    def GET(self):

        # Check auth
        if not checkauth():
            return "error_noauthdata"

        # This operation is expensive, throttle
        if not throttle_status_ok(web):
            return "pleasecooldown"

        # Logout Telegram Client
        client = getclient()
        if isinstance(client, str):
            return client
        client.log_out()

        return True

class getchats:
    def GET(self):

        # Check auth
        if not checkauth():
            return "error_noauthdata"

        # Handle cache
        clientcachedir = cachedir + "/" + session.client_id
        if not os.path.isdir(clientcachedir):
            os.makedirs(clientcachedir)
        chats_shelve = shelve.open(clientcachedir + "/chats.shelve")
        chats_shelve.sync()
        shelve_ctime = time.gmtime(os.path.getctime(clientcachedir + "/chats.shelve"))
        web.header('X-last-fetched-data', time.strftime("%d %b %Y %H:%M:%S %z", shelve_ctime))

        # Only get data if not cached already
        if not "data" in chats_shelve:

            # This operation is expensive, throttle
            if not throttle_status_ok(web):
                return "pleasecooldown"

            # Get Telegram Client
            client = getclient()
            if isinstance(client, str):
                return client

            # Get chats
            groups = []
            groups_raw = {}
            tgr = client(GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=InputPeerEmpty(), limit=60))
            for chat in tgr.chats:
                logging.debug("admintools:getchats:GET Parsing %s..." % chat)
                if (isinstance(chat, Chat) or isinstance(chat,Channel)) and \
                   (chat.participants_count is None or chat.participants_count>2) and \
                   (not hasattr(chat, "migrated_to")) and \
                   ((hasattr(chat, "admin") and chat.admin is True) or (hasattr(chat, "admin_rights") and chat.admin_rights is not None) or \
                    (hasattr(chat, "creator") and chat.creator is True)) and \
                    (existsGroup(chat.id) or existsGroup(int("-100" + str(chat.id)))):
                    groups.append([chat.id, chat.title])
                    logging.debug("admintools:getchats:GET ACCEPTED")
                else:
                    logging.debug("admintools:getchats:GET REJECTED")

            chats_shelve["data"] = groups

        groups = chats_shelve["data"]
        chats_shelve.close()
        return json.dumps(groups)

class getparticipants:
    def GET(self, chat_id):

        # Check auth
        if not checkauth():
            return "error_noauthdata"

        # Handle cache
        clientcachedir = cachedir + "/" + session.client_id
        if not os.path.isdir(clientcachedir):
            os.makedirs(clientcachedir)
        users_shelve = shelve.open(clientcachedir + "/chat_" + chat_id + ".shelve")
        users_shelve.sync()
        shelve_ctime = time.gmtime(os.path.getctime(clientcachedir + "/chat_" + chat_id + ".shelve"))
        web.header('X-last-fetched-data', time.strftime("%d %b %Y %H:%M:%S %z", shelve_ctime))

        # Only get data if not cached already
        if not "data" in users_shelve:

            # This operation is expensive, throttle
            if not throttle_status_ok(web):
                return "pleasecooldown"

            # Get Telegram Client
            client = getclient()
            if isinstance(client, str):
                return client

            # Check that group exists for this user first
            chats_shelve = shelve.open(clientcachedir + "/chats.shelve")
            if not "data" in chats_shelve:
                return "error_nogroupdata"
            groups = chats_shelve["data"]
            permission = False
            for group in groups:
                if str(group[0]) == str(chat_id):
                    permission = True
                    break
            if not permission:
                return "error_unknownchat"

            # Get group from Telegram dialogs
            groups = []
            tgr = client(GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=InputPeerEmpty(), limit=60))
            chosen_chat = None
            for chat in tgr.chats:
               if str(chat.id) == str(chat_id):
                   chosen_chat = chat
                   logging.info("admintools:getparticipants:GET: Chosen chat %s - %s" % (chat.id, chat.title))
                   break

            if chosen_chat is None:
                print("error_cantfindchat")
                return web.internalerror()

            groupentity = client.get_entity(int(chat_id)) # FIXME for channels?

            offset = 0
            users = []
            while True:
                tgr = client(GetParticipantsRequest(channel=groupentity, filter=ChannelParticipantsSearch(""), offset=offset, limit=200, hash=0))
                for user in tgr.users:
                    if user.bot == False:
                        logging.info("admintools:getparticipants:GET: Adding %s" % user)
                        users.append({"id":user.id, "username":user.username, "last_name":user.last_name, "first_name":user.first_name})

                logging.info("admintools:getparticipants:GET: Received %s users" % len(tgr.users))
                if len(tgr.users) < 200:
                    break
                else:
                    offset += len(tgr.users)
                    time.sleep(0.3)
            users_shelve["data"] = users
        users_shelve.close()
        return "ok"

class getnotvalidated:
    def GET(self, chat_id):

        # Check auth
        if not checkauth():
            return "error_noauthdata"

        # Handle cache
        clientcachedir = cachedir + "/" + session.client_id
        if not os.path.isdir(clientcachedir):
            os.makedirs(clientcachedir)
        notvalidated_shelve = shelve.open(clientcachedir + "/notvalidated_" + chat_id + ".shelve")
        notvalidated_shelve.sync()
        shelve_ctime = time.gmtime(os.path.getctime(clientcachedir + "/notvalidated_" + chat_id + ".shelve"))
        web.header('X-last-fetched-data', time.strftime("%d %b %Y %H:%M:%S %z", shelve_ctime))

        # Only get data if not cached already
        if not "data" in notvalidated_shelve:

            # Get users for this group - assumes permission granted from getparticipants
            users_shelve = shelve.open(clientcachedir + "/chat_" + chat_id + ".shelve")
            if not "data" in users_shelve:
                return "error_notusers"
            participants = users_shelve["data"]

            # Gets list of not validated users
            notvalidated = []
            for participant in participants:
                if not pikavalidated(participant["id"]):
                    notvalidated.append(participant)
                time.sleep(0.05)
            notvalidated_shelve["data"] = notvalidated

        notvalidated = notvalidated_shelve["data"]
        notvalidated_shelve.close()
        return json.dumps(notvalidated)

class getteams:
    def GET(self, chat_id):

        # Check auth
        if not checkauth():
            return "error_noauthdata"

        # Handle cache
        clientcachedir = cachedir + "/" + session.client_id
        if not os.path.isdir(clientcachedir):
            os.makedirs(clientcachedir)
        teams_shelve = shelve.open(clientcachedir + "/teams_" + chat_id + ".shelve")
        teams_shelve.sync()
        shelve_ctime = time.gmtime(os.path.getctime(clientcachedir + "/teams_" + chat_id + ".shelve"))
        web.header('X-last-fetched-data', time.strftime("%d %b %Y %H:%M:%S %z", shelve_ctime))

        # Only get data if not cached already
        if not "data" in teams_shelve:

            # Get users for this group - assumes permission granted from getparticipants
            users_shelve = shelve.open(clientcachedir + "/chat_" + chat_id + ".shelve")
            if not "data" in users_shelve:
                return "error_notusers"
            participants = users_shelve["data"]

            # Gets list of not validated users
            teams = {
                "Rojo": 0,
                "Azul": 0,
                "Amarillo": 0,
                "Desconocido": 0
            }
            for participant in participants:
                user = getUser(participant["id"])
                if user is not None and user["validation"] != "none":
                    if user["team"] == "Rojo":
                        teams["Rojo"] += 1
                    elif user["team"] == "Azul":
                        teams["Azul"] += 1
                    elif user["team"] == "Amarillo":
                        teams["Amarillo"] += 1
                    else:
                        teams["Desconocido"] += 1
                else:
                    teams["Desconocido"] += 1
                time.sleep(0.05)
            teams_shelve["data"] = teams

        teams = teams_shelve["data"]
        teams_shelve.close()
        return json.dumps(teams)

class getgyms:
    def GET(self, chat_id, days):

        if days not in ["4","6","7","14","30","60","90"]:
            return "error_invalidparameter"

        # Check auth
        if not checkauth():
            return "error_noauthdata"

        # Handle cache
        clientcachedir = cachedir + "/" + session.client_id
        if not os.path.isdir(clientcachedir):
            os.makedirs(clientcachedir)
        gyms_shelve = shelve.open(clientcachedir + "/gyms_" + str(days) + "_" + chat_id + ".shelve")
        gyms_shelve.sync()
        shelve_ctime = time.gmtime(os.path.getctime(clientcachedir + "/gyms_" + str(days) + "_" + chat_id + ".shelve"))
        web.header('X-last-fetched-data', time.strftime("%d %b %Y %H:%M:%S %z", shelve_ctime))

        # Only get data if not cached already
        if not "data" in gyms_shelve:

            # Get gyms by activity
            gyms = getGymsByActivity(chat_id, days)
            if gyms == None or len(gyms) == 0:
                gyms = getGymsByActivity(int("-100" + str(chat_id)), days)
            gyms_shelve["data"] = gyms

        gyms = gyms_shelve["data"]
        gyms_shelve.close()
        return json.dumps(gyms)

class getinactive:
    def GET(self, chat_id, days):

        if days not in ["4","6","7","14","30","60","90"]:
            return "error_invalidparameter"

        # Check auth
        if not checkauth():
            return "error_noauthdata"

        # Handle cache
        clientcachedir = cachedir + "/" + session.client_id
        if not os.path.isdir(clientcachedir):
            os.makedirs(clientcachedir)
        inactive_shelve = shelve.open(clientcachedir + "/inactive_" + str(days) + "_" + chat_id + ".shelve")
        inactive_shelve.sync()
        shelve_ctime = time.gmtime(os.path.getctime(clientcachedir + "/inactive_" + str(days) + "_" + chat_id + ".shelve"))
        web.header('X-last-fetched-data', time.strftime("%d %b %Y %H:%M:%S %z", shelve_ctime))

        # Only get data if not cached already
        if not "data" in inactive_shelve:

            # Get users for this group - assumes permission granted from getparticipants
            users_shelve = shelve.open(clientcachedir + "/chat_" + chat_id + ".shelve")
            if not "data" in users_shelve:
                return "error_notusers"
            participants = users_shelve["data"]

            # Gets list of inactive users
            inactive = []
            for participant in participants:
                if not pikaactive(participant["id"], chat_id, days):
                    inactive.append(participant)
                time.sleep(0.05)
            inactive_shelve["data"] = inactive

        inactive = inactive_shelve["data"]
        inactive_shelve.close()
        return json.dumps(inactive)


def checkauth():
    logging.info("admintools:checkauth")
    if not "client_id" in session:
        return False
    else:
        return True

def getclient():
    logging.info("admintools:getclient")
    client = TelegramClient(session.appstring, config["admintools"]["apiid"], config["admintools"]["apihash"], update_workers=1)
    if client.connect() != True:
        return "cantconnect"
    if not client.is_user_authorized():
        return "needauth_notclientauthorized"
    return client

def pikavalidated(user_id):
    logging.info("admintools:Pikavalidated: %s" % user_id)
    user = getUser(user_id)
    if user is None or user["validation"] == "none":
        return False
    else:
        return True

def pikaactive(user_id, group_id, days="30"):
    logging.info("admintools:Pikaactive: %s %s %s" % (user_id, group_id, days))
    if not isActiveInGroup(user_id, group_id, days):
        if not isActiveInGroup(user_id, int("-100" + str(group_id)), days):
            return False
    return True

def throttle_status_ok(web):
    logging.info("admintools:throttle_status_ok")
    try:
        ipaddress = "ipaddress" + str(web.ctx['env']["HTTP_X_REAL_IP"])
    except:
        ipaddress = "ipaddress" + str(web['ip'])

    throttle_shelve = shelve.open(cachedir + "/throttle.shelve")
    if ipaddress in throttle_shelve.keys():
        throttle_shelve[ipaddress] = str(int(throttle_shelve[ipaddress])+1)
    else:
        throttle_shelve[ipaddress] = "1"
    logging.info("admintools:decrease_throttle_values Increased %s to %s" % (ipaddress,throttle_shelve[ipaddress]))
    throttle_value = throttle_shelve[ipaddress]
    throttle_shelve.close()
    if int(throttle_value)>7:
        return False
    else:
        return True

def decrease_throttle_values():
    logging.info("admintools:decrease_throttle_values")
    while True:
        throttle_shelve = shelve.open(cachedir + "/throttle.shelve")
        klist = list(throttle_shelve.keys())
        for k in klist:
            if throttle_shelve[k] == "0":
                continue
            throttle_shelve[k] = str(int(throttle_shelve[k])-1)
            logging.info("admintools:decrease_throttle_values Decreased %s to %s" % (k,throttle_shelve[k]))
        throttle_shelve.close()
        time.sleep(3600)

class MyApplication(web.application):
    def run(self, port=8044, *middleware):
        func = self.wsgifunc(*middleware)
        logging.info("admintools:web.application: Starting backend at port %s" % port)
        return web.httpserver.runsimple(func, ("127.0.0.1", port))

def serve_frontend(port=8045):
    # Serve frontend assets
    web_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'frontend')
    os.chdir(web_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("127.0.0.1", 8045), Handler)
    logging.info("admintools:serve_frontend: Starting frontend at port %s" % 8045)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        self.server_close()

def delete_old_cached_files():
    while True:
        now = time.time()
        for f in os.listdir(cachedir):
            usercachedir = os.path.join(cachedir, f)
            if os.path.isdir(usercachedir):
                for g in os.listdir(usercachedir):
                    usercachefile = os.path.join(usercachedir, g)
                    if os.stat(usercachefile).st_mtime < (now - 75600):
                        if os.path.isfile(usercachefile):
                            logging.info("admintools:delete_old_cached_files: Delete file %s" % usercachefile)
                            os.remove(usercachefile)
        time.sleep(60)

if __name__ == "__main__":

    # Create cache directory if it does not exist
    logging.info("admintools:main: Cache dir %s" % cachedir)
    if not os.path.isdir(cachedir):
        os.makedirs(cachedir)

    # Server frontend
    t = Thread(target=serve_frontend, args=(8045,))
    t.daemon = True
    t.start()
    time.sleep(1)

    # Decrease throttle values
    t2 = Thread(target=decrease_throttle_values)
    t2.daemon = True
    t2.start()
    time.sleep(1)

    # Delete old cached files
    t3 = Thread(target=delete_old_cached_files)
    t3.daemon = True
    t3.start()
    time.sleep(1)

    # Run webapp
    app = MyApplication(urls, globals())
    sessionsdir = os.path.realpath(os.path.dirname(__file__)) + '/sessions'
    logging.info("admintools:main: Web sessions dir %s" % sessionsdir)
    session = web.session.Session(app, web.session.DiskStore(sessionsdir), initializer={'count': 0})
    app.run(port=8044)
