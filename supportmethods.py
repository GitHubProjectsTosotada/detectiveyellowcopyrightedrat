# Detective Yellowcopyrightedrat - A Telegram bot to organize Pokémon GO raids
# Copyright (C) 2017 Jorge Suárez de Lis <hey@gentakojima.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
from datetime import datetime, timedelta
from pytz import timezone
import time
import html
import logging
from threading import Thread
import telegram
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from Levenshtein import distance
import cv2
import tempfile
import os, sys
import numpy as np
import pytesseract
from PIL import Image, ImageOps
from skimage.measure import compare_ssim as ssim
from unidecode import unidecode
import googlemaps
import math

from config import config
from storagemethods import getRaidbyMessage, getCreadorRaid, getRaidPeople, getRaid, getAlertsByPlace, getGroup, getZones, updateRaidsStatus, updateValidationsStatus, getPlace, getAutorefloatGroups, getActiveRaidsforGroup, saveRaid, updateLastAutorefloat, savePlace, getGroupTimezoneOffsetFromServer, getCurrentPokemons, getCurrentGyms, removeIncompleteRaids
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

pokemonlist = ['Bulbasaur','Ivysaur','Venusaur','Charmander','Charmeleon','Charizard','Squirtle','Wartortle','Blastoise','Caterpie','Metapod','Butterfree','Weedle','Kakuna','Beedrill','Pidgey','Pidgeotto','Pidgeot','Rattata','Raticate','Spearow','Fearow','Ekans','Arbok','Pikachu','Raichu','Sandshrew','Sandslash','Nidoran♀','Nidorina','Nidoqueen','Nidoran♂','Nidorino','Nidoking','Clefairy','Clefable','Vulpix','Ninetales','Jigglypuff','Wigglytuff','Zubat','Golbat','Oddish','Gloom','Vileplume','Paras','Parasect','Venonat','Venomoth','Diglett','Dugtrio','Meowth','Persian','Psyduck','Golduck','Mankey','Primeape','Growlithe','Arcanine','Poliwag','Poliwhirl','Poliwrath','Abra','Kadabra','Alakazam','Machop','Machoke','Machamp','Bellsprout','Weepinbell','Victreebel','Tentacool','Tentacruel','Geodude','Graveler','Golem','Ponyta','Rapidash','Slowpoke','Slowbro','Magnemite','Magneton','Farfetch\'d','Doduo','Dodrio','Seel','Dewgong','Grimer','Muk','Shellder','Cloyster','Gastly','Haunter','Gengar','Onix','Drowzee','Hypno','Krabby','Kingler','Voltorb','Electrode','Exeggcute','Exeggutor','Cubone','Marowak','Hitmonlee','Hitmonchan','Lickitung','Koffing','Weezing','Rhyhorn','Rhydon','Chansey','Tangela','Kangaskhan','Horsea','Seadra','Goldeen','Seaking','Staryu','Starmie','Mr.Mime','Scyther','Jynx','Electabuzz','Magmar','Pinsir','Tauros','Magikarp','Gyarados','Lapras','Ditto','Eevee','Vaporeon','Jolteon','Flareon','Porygon','Omanyte','Omastar','Kabuto','Kabutops','Aerodactyl','Snorlax','Articuno','Zapdos','Moltres','Dratini','Dragonair','Dragonite','Mewtwo','Mew','Chikorita','Bayleef','Meganium','Cyndaquil','Quilava','Typhlosion','Totodile','Croconaw','Feraligatr','Sentret','Furret','Hoothoot','Noctowl','Ledyba','Ledian','Spinarak','Ariados','Crobat','Chinchou','Lanturn','Pichu','Cleffa','Igglybuff','Togepi','Togetic','Natu','Xatu','Mareep','Flaaffy','Ampharos','Bellossom','Marill','Azumarill','Sudowoodo','Politoed','Hoppip','Skiploom','Jumpluff','Aipom','Sunkern','Sunflora','Yanma','Wooper','Quagsire','Espeon','Umbreon','Murkrow','Slowking','Misdreavus','Unown','Wobbuffet','Girafarig','Pineco','Forretress','Dunsparce','Gligar','Steelix','Snubbull','Granbull','Qwilfish','Scizor','Shuckle','Heracross','Sneasel','Teddiursa','Ursaring','Slugma','Magcargo','Swinub','Piloswine','Corsola','Remoraid','Octillery','Delibird','Mantine','Skarmory','Houndour','Houndoom','Kingdra','Phanpy','Donphan','Porygon2','Stantler','Smeargle','Tyrogue','Hitmontop','Smoochum','Elekid','Magby','Miltank','Blissey','Raikou','Entei','Suicune','Larvitar','Pupitar','Tyranitar','Lugia','Ho-Oh','Celebi','Treecko','Grovyle','Sceptile','Torchic','Combusken','Blaziken','Mudkip','Marshtomp','Swampert','Poochyena','Mightyena','Zigzagoon','Linoone','Wurmple','Silcoon','Beautifly','Cascoon','Dustox','Lotad','Lombre','Ludicolo','Seedot','Nuzleaf','Shiftry','Taillow','Swellow','Wingull','Pelipper','Ralts','Kirlia','Gardevoir','Surskit','Masquerain','Shroomish','Breloom','Slakoth','Vigoroth','Slaking','Nincada','Ninjask','Shedinja','Whismur','Loudred','Exploud','Makuhita','Hariyama','Azurill','Nosepass','Skitty','Delcatty','Sableye','Mawile','Aron','Lairon','Aggron','Meditite','Medicham','Electrike','Manectric','Plusle','Minun','Volbeat','Illumise','Roselia','Gulpin','Swalot','Carvanha','Sharpedo','Wailmer','Wailord','Numel','Camerupt','Torkoal','Spoink','Grumpig','Spinda','Trapinch','Vibrava','Flygon','Cacnea','Cacturne','Swablu','Altaria','Zangoose','Seviper','Lunatone','Solrock','Barboach','Whiscash','Corphish','Crawdaunt','Baltoy','Claydol','Lileep','Cradily','Anorith','Armaldo','Feebas','Milotic','Castform','Kecleon','Shuppet','Banette','Duskull','Dusclops','Tropius','Chimecho','Absol','Wynaut','Snorunt','Glalie','Spheal','Sealeo','Walrein','Clamperl','Huntail','Gorebyss','Relicanth','Luvdisc','Bagon','Shelgon','Salamence','Beldum','Metang','Metagross','Regirock','Regice','Registeel','Latias','Latios','Kyogre','Groudon','Rayquaza','Jirachi','Deoxys']
egglist = ['N1','N2','N3','N4','N5','EX']
iconthemes = [
    { "Rojo": "🔥", "Azul": "❄️", "Amarillo": "⚡️" },
    { "Rojo": "🔴", "Azul": "🔵", "Amarillo": "🌕" },
    { "Rojo": "❤", "Azul": "💙", "Amarillo": "💛" },
    { "Rojo": "🔴", "Azul": "🔵", "Amarillo": "🔶" },
    { "Rojo": "♨️", "Azul": "🌀", "Amarillo": "🔆" },
    { "Rojo": "🦊", "Azul": "🐳", "Amarillo": "🐥" }
]

validation_pokemons = ["chikorita", "machop", "growlithe", "diglett", "spinarak", "ditto", "teddiursa", "cubone", "sentret", "voltorb"]
validation_profiles = ["model1", "model2", "model3", "model4", "model5"]
validation_names = ["Calabaza", "Puerro", "Cebolleta", "Remolacha", "Aceituna", "Pimiento", "Zanahoria", "Tomate", "Guisante", "Coliflor", "Pepino", "Berenjena", "Perejil", "Batata", "Aguacate", "Alcaparra", "Escarola", "Lechuga", "Hinojo"]

def is_admin(chat_id, user_id, bot):
    is_admin = False
    for admin in bot.get_chat_administrators(chat_id):
      if user_id == admin.user.id:
        is_admin = True
    return is_admin

def extract_update_info(update):
    logging.debug("supportmethods:extract_update_info")
    try:
        message = update.message
    except:
        message = update.channel_post
    if message is None:
        message = update.channel_post
    text = message.text
    try:
        user_id = message.from_user.id
    except:
        user_id = None
    chat_id = message.chat.id
    chat_type = message.chat.type
    return (chat_id, chat_type, user_id, text, message)

def send_message_timed(chat_id, text, sleep_time, bot):
    logging.debug("supportmethods:send_message_timed: %s %s %s %s" % (chat_id, text, sleep_time, bot))
    time.sleep(sleep_time)
    bot.sendMessage(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

def delete_message_timed(chat_id, message_id, sleep_time, bot):
    time.sleep(sleep_time)
    delete_message(chat_id, message_id, bot)

def delete_message(chat_id, message_id, bot):
    try:
        bot.deleteMessage(chat_id=chat_id,message_id=message_id)
        return True
    except:
        return False

def count_people(gente):
    count = 0
    if gente is not None:
        for user in gente:
            if user["novoy"] > 0:
                continue
            count = count + 1
            if (user["plus"] is not None and user["plus"]>0) or\
               (user["plusb"] is not None and user["plusb"]>0) or\
               (user["plusy"] is not None and user["plusy"]>0) or\
               (user["plusr"] is not None and user["plusr"]>0):
                count = count + user["plus"] + user["plusr"] + user["plusy"] + user["plusb"]
    return count

def count_people_disaggregated(gente):
    numrojos = 0
    numazules = 0
    numamarillos = 0
    numotros = 0
    count = 0
    if gente is not None:
        for user in gente:
            if user["novoy"] > 0:
                continue
            count = count + 1
            if user["plus"] is not None and user["plus"] > 0:
                count = count + user["plus"]
                numotros = numotros + user["plus"]
            if user["plusr"] is not None and user["plusr"] > 0:
                count = count + user["plusr"]
                numrojos = numrojos + user["plusr"]
            if user["plusb"] is not None and user["plusb"] > 0:
                count = count + user["plusb"]
                numazules = numazules + user["plusb"]
            if user["plusy"] is not None and user["plusy"] > 0:
                count = count + user["plusy"]
                numamarillos = numamarillos + user["plusy"]
            if user["team"] == "Rojo":
                numrojos = numrojos + 1
            elif user["team"] == "Azul":
                numazules = numazules + 1
            elif user["team"] == "Amarillo":
                numamarillos = numamarillos + 1
            else:
                numotros = numotros + 1
    return (numazules, numrojos, numamarillos, numotros, count)

def send_alerts_delayed(raid, bot):
    time.sleep(2)
    send_alerts(raid, bot)

def send_alerts(raid, bot):
    logging.debug("supportmethods:send_alerts: %s" % (raid))
    alerts = getAlertsByPlace(raid["gimnasio_id"])
    group = getGroup(raid["grupo_id"])
    if group["alerts"] == 1:
        what_text = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
        what_day = format_text_day(raid["timeraid"], group["timezone"])
        if group["alias"] is not None:
            incursion_text = "<a href='https://t.me/%s/%s'>incursión</a>" % (group["alias"], raid["message"])
            group_text =  "<a href='https://t.me/%s'>%s</a>" % (group["alias"], html.escape(group["title"]))
        else:
            incursion_text = "incursión"
            try:
                group_text = "<i>%s</i>" % (html.escape(group["title"]))
            except:
                group_text = "<i>(Grupo sin nombre guardado)</i>"
        logging.debug("supportmethods:send_alerts: Sending %i alerts" % len(alerts))
        for alert in alerts:
            logging.debug("supportmethods:send_alerts: Sending alert %s" % alert)
            bot.sendMessage(chat_id=alert["user_id"], text="🔔 Se ha creado una %s %s en <b>%s</b> %sa las <b>%s</b> en el grupo %s.\n\n<i>Recibes esta alerta porque has activado las alertas para ese gimnasio. Si no deseas recibir más alertas, puedes usar el comando</i> <code>/clearalerts</code>" % (incursion_text, what_text, raid["gimnasio_text"], what_day, extract_time(raid["timeraid"]), group_text), parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

def update_message(chat_id, message_id, reply_markup, bot):
    logging.debug("supportmethods:update_message: %s %s %s" % (chat_id, message_id, reply_markup))
    raid = getRaidbyMessage(chat_id, message_id)
    text = format_message(raid)
    return bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True, timeout=8)

def format_gym_emojis(tags):
    logging.debug("supportmethods:format_gym_emojis: %s" % tags)
    tags_emojis = ""
    for t in tags:
        if unidecode(t).lower() == "jardin":
            tags_emojis = tags_emojis + "🌷"
        if unidecode(t).lower() == "parque":
            tags_emojis = tags_emojis + "🌳"
        if unidecode(t).lower() == "juegos":
            tags_emojis = tags_emojis + "⚽️"
        if unidecode(t).lower() in ["hierba","campo"]:
            tags_emojis = tags_emojis + "🌱"
        if unidecode(t).lower() == "patrocinado":
            tags_emojis = tags_emojis + "💵"
        if unidecode(t).lower() == "ex":
            tags_emojis = tags_emojis + "🌟"
    return tags_emojis

def fetch_gym_address(gym):
    logging.debug("supportmethods:fetch_gym_address %s" % gym["id"])
    try:
      gmaps = googlemaps.Client(key=config["googlemaps"]["key"], retry_timeout=3)
      reverse_geocode_result = gmaps.reverse_geocode((gym["latitude"], gym["longitude"]))
      address = reverse_geocode_result[0]["formatted_address"]
      gym["address"] = address
      savePlace(gym)
    except:
      logging.debug("detectivepikachubot:raidbutton:ubicacion Error fetching address! Key limit reached?")
      gym["address"] = "-"
    return gym

def format_message(raid):
    logging.debug("supportmethods:format_message: %s" % (raid))

    creador = getCreadorRaid(raid["id"])
    group = getGroup(raid["grupo_id"])
    icons = iconthemes[group["icontheme"]]
    ordering = "addedtime" if group["listorder"] == 0 else "teamlevel"
    gente = getRaidPeople(raid["id"], ordering)

    if "edited" in raid.keys() and raid["edited"]>0:
        text_edited = " <em>(editada)</em>"
    else:
        text_edited = ""
    if "refloated" in raid.keys() and raid["refloated"]>0:
        text_refloated = " <em>(reflotada)</em>"
    else:
        text_refloated = ""
    if "timeend" in raid.keys() and raid["timeend"] is not None:
        t = extract_time(raid["timeend"], group["timeformat"])
        raidend_near = raidend_is_near_raidtime(raid["timeraid"], raid["timeend"], group["timezone"])
        timeend_warn = "⚠️" if raidend_near >= 0 else ""
        text_endtime = "\n%s<em>Desaparece a las %s</em>" % (timeend_warn, t)
    else:
        timeend_warn = ""
        text_endtime = ""
    if group["locations"] == 1:
        if "gimnasio_id" in raid.keys() and raid["gimnasio_id"] is not None:
            gym_emoji="🌎"
            place = getPlace(raid["gimnasio_id"])
            if place["tags"] is not None:
                tags_emojis = format_gym_emojis(place["tags"])
            if len(tags_emojis) > 0:
                gym_emoji = tags_emojis
        else:
            gym_emoji="❓"
    else:
        gym_emoji=""
    what_text = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
    what_day = format_text_day(raid["timeraid"], group["timezone"], "html")
    if creador["username"] is not None:
        if creador["trainername"] is not None:
            created_text = "\nCreada por <a href='https://t.me/%s'>%s</a>%s%s" % (creador["username"], creador["trainername"], text_edited, text_refloated)
        else:
            created_text = "\nCreada por @%s%s%s" % (creador["username"], text_edited, text_refloated)
    else:
        created_text = ""
    text = "Incursión %s %sa las %s<b>%s</b> en %s<b>%s</b>%s%s\n" % (what_text, what_day, timeend_warn, extract_time(raid["timeraid"], group["timeformat"]), gym_emoji, raid["gimnasio_text"], created_text, text_endtime)
    if raid["status"] == "cancelled":
        text = text + "❌ <b>Incursión cancelada</b>"
    else:
        if group["disaggregated"] == 1:
            (numazules, numrojos, numamarillos, numotros, numgente) = count_people_disaggregated(gente)
            if numotros > 0:
                otros_text = "❓%s · " % numotros
            else:
                otros_text = ""
            text = text + "%s%s · %s%s · %s%s · %s👩‍👩‍👧‍👧%s" % (icons["Amarillo"], numamarillos, icons["Azul"], numazules, icons["Rojo"], numrojos, otros_text, numgente)
        else:
            numgente = count_people(gente)
            text = text + "%s entrenadores apuntados:" % numgente
    if raid["status"] != "cancelled" and gente is not None:
        diff_hours = getGroupTimezoneOffsetFromServer(group["id"])
        for user in gente:
            if group["plusdisaggregatedinline"] == 1:
                plus_text = ""
                if user["team"] == "Rojo":
                    if user["plusr"] > 0:
                        plus_text = plus_text + " +%i" % user["plusr"]
                    if user["plusy"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Amarillo"],user["plusy"])
                    if user["plusb"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Azul"],user["plusb"])
                elif user["team"] == "Azul":
                    if user["plusb"] > 0:
                        plus_text = plus_text + " +%i" % user["plusb"]
                    if user["plusy"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Amarillo"],user["plusy"])
                    if user["plusr"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Rojo"],user["plusr"])
                elif user["team"] == "Amarillo":
                    if user["plusy"] > 0:
                        plus_text = plus_text + " +%i" % user["plusy"]
                    if user["plusb"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Azul"],user["plusb"])
                    if user["plusr"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Rojo"],user["plusr"])
                else:
                    if user["plusy"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Amarillo"],user["plusy"])
                    if user["plusb"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Azul"],user["plusb"])
                    if user["plusr"] > 0:
                        plus_text = plus_text + " %s+%i" % (icons["Rojo"],user["plusr"])
                if user["plus"] > 0:
                    plus_text = plus_text + " ❓+%i" % user["plus"]
            else:
                if (user["plus"] is not None and user["plus"]>0) or\
                   (user["plusb"] is not None and user["plusb"]>0) or\
                   (user["plusy"] is not None and user["plusy"]>0) or\
                   (user["plusr"] is not None and user["plusr"]>0):
                    plus_text = " +%i" % (user["plus"]+user["plusr"]+user["plusb"]+user["plusy"])
                else:
                    plus_text = ""
            if user["estoy"] is not None and user["estoy"]>0:
                estoy_text = "✅ "
            elif user["tarde"] is not None and user["tarde"]>0:
                estoy_text = "🕒 "
            elif user["novoy"] >0:
                estoy_text = "❌ "
            else:
                estoy_text = "▪️ "
            if group["snail"] > 0:
                user_addedtime = user["addedtime"].replace(tzinfo=timezone(group["timezone"]))
                raid_starttime = raid["timeraid"].replace(tzinfo=timezone(group["timezone"])) - timedelta(minutes=diff_hours*60) - timedelta(minutes=group["snail"])
                if user_addedtime > raid_starttime:
                    lateadded_text = "🐌"
                else:
                    lateadded_text = ""
            else:
                lateadded_text = ""
            if user["lotengo"] == 0:
                lotengo_text = "👎"
            elif user["lotengo"] == 1:
                lotengo_text = "👍"
            else:
                lotengo_text = ""
            if user["level"] is not None and user["team"] is not None:
                if user["team"] is not None:
                    if user["team"]=="Rojo":
                        team_badge = icons["Rojo"]
                    elif user["team"]=="Amarillo":
                        team_badge = icons["Amarillo"]
                    else:
                        team_badge = icons["Azul"]
                if user["trainername"] is not None:
                    text = text + "\n%s%s%s <a href='https://t.me/%s'>%s</a>%s%s%s" % (estoy_text,team_badge,user["level"],user["username"],user["trainername"],lateadded_text,lotengo_text,plus_text)
                else:
                    text = text + "\n%s%s%s <a href='https://t.me/%s'>@%s</a>%s%s%s" % (estoy_text,team_badge,user["level"],user["username"],user["username"],lateadded_text,lotengo_text,plus_text)
            else:
                text = text + "\n%s➖ - - <a href='https://t.me/%s'>@%s</a>%s%s%s" % (estoy_text,user["username"],user["username"],lotengo_text,lateadded_text,plus_text)
    return text

def format_text_pokemon(pokemon, egg, format="markdown"):
    if pokemon is not None:
        what_text = "de <b>%s</b>" % pokemon if format == "html" else "de *%s*" % pokemon
    else:
        if egg == "EX":
            what_text = "<b>🌟EX</b>" if format == "html" else "*🌟EX*"
        else:
            what_text = egg.replace("N","de <b>nivel ") + "</b>" if format == "html" else egg.replace("N","de *nivel ") + "*"
    return what_text

def format_text_day(timeraid, tzone, format="markdown"):
    logging.debug("supportmethods:format_text_day %s %s" % (timeraid, tzone))
    try:
        raid_datetime = datetime.strptime(timeraid,"%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(tzone))
    except:
        raid_datetime = timeraid.replace(tzinfo=timezone(tzone))
    now_datetime = datetime.now(timezone(tzone))
    difftime = raid_datetime - now_datetime
    if difftime.total_seconds() > (3600*16):
        weekdays = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        what_day = "el <b>%s día %s</b> " % (weekdays[raid_datetime.weekday()], raid_datetime.day) if format == "html" else "el *%s día %s* " % (weekdays[raid_datetime.weekday()], raid_datetime.day)
    else:
        what_day = ""
    return what_day

def format_text_creating(creator):
    logging.debug("supportmethods:format_text_creating");
    if creator is not None and creator["username"] is not None:
        if creator["trainername"] is not None:
            creating_text = "<a href='https://t.me/%s'>%s</a> está creando una incursión..." % (creator["username"], creator["trainername"])
        else:
            creating_text = "@%s está creando una incursión..." % (creator["username"])
    else:
        creating_text = "Se está creando una incursión..."
    return creating_text

def ensure_escaped(username):
    if username.find("_") != -1 and username.find("\\_") == -1:
        username = username.replace("_","\\_")
    return username

def update_raids_status(bot):
    logging.debug("supportmethods:update_raids_status")
    raids = updateRaidsStatus()
    for raid in raids:
        logging.debug(raid)
        r = getRaid(raid["id"])
        logging.debug("Updating message for raid ID %s" % (raid["id"]))
        try:
            reply_markup = get_keyboard(r)
            updated = update_message(r["grupo_id"], r["message"], reply_markup, bot)
            logging.debug(updated)
        except Exception as e:
            logging.debug("supportmethods:update_raids_status error: %s" % str(e))
        time.sleep(0.015)

def update_validations_status(bot):
    logging.debug("supportmethods:update_validations_status")
    validations = updateValidationsStatus()
    for v in validations:
        logging.debug(v)
        logging.debug("Sending notification for validation ID %s, user ID %s" % (v["id"], v["usuario_id"]))
        try:
            bot.sendMessage(chat_id=v["usuario_id"], text="⚠ El proceso de validación pendiente ha caducado porque han pasado 6 horas desde que empezó. Si quieres validarte, debes volver a empezar el proceso.", parse_mode=telegram.ParseMode.MARKDOWN)
        except Exception as e:
            logging.debug("supportmethods:update_validations_status error: %s" % str(e))
        time.sleep(0.015)

def remove_incomplete_raids(bot):
    logging.debug("supportmethods:remove_incomplete_raids")
    raids = removeIncompleteRaids()
    for raid in raids:
        logging.debug(raid)
        r = getRaid(raid["id"])
        logging.debug("Removing message for raid ID %s" % (raid["id"]))
        try:
            reply_markup = get_keyboard(r)
            updated = bot.deleteMessage(chat_id = r["grupo_id"], message_id = r["message"])
        except Exception as e:
            logging.debug("supportmethods:remove_incomplete_raids error: %s" % str(e))
        time.sleep(0.015)

def auto_refloat(bot):
    logging.debug("supportmethods:auto_refloat")
    groups = getAutorefloatGroups()
    for g in groups:
        logging.debug("supportmethods:auto_refloat auto refloat group %s %s" % (g["id"],g["title"]))
        updateLastAutorefloat(g["id"])
        group = getGroup(g["id"])
        intwohours_datetime = datetime.now(timezone(group["timezone"])).replace(tzinfo=timezone(group["timezone"])) + timedelta(minutes = 90)
        tenminsago_datetime = datetime.now(timezone(group["timezone"])).replace(tzinfo=timezone(group["timezone"])) - timedelta(minutes = 9)
        fifminsago_datetime = datetime.now(timezone(group["timezone"])).replace(tzinfo=timezone(group["timezone"])) - timedelta(minutes = 15)
        tweminsago_datetime = datetime.now(timezone(group["timezone"])).replace(tzinfo=timezone(group["timezone"])) - timedelta(minutes = 20)
        raids = getActiveRaidsforGroup(g["id"])
        for raid in raids:
            timeraid = raid["timeraid"].replace(tzinfo=timezone(group["timezone"]))
            if raid["id"] is not None and raid["status"] != "ended" and timeraid <= intwohours_datetime and (\
                (g["refloatauto"] == 5 and timeraid > tenminsago_datetime) or \
                (g["refloatauto"] == 10 and timeraid > fifminsago_datetime) or \
                (g["refloatauto"] == 15 and timeraid > tweminsago_datetime) or \
                 g["refloatauto"] == 30):
                try:
                    raid["refloated"] = 1
                    text = format_message(raid)
                    reply_markup = get_keyboard(raid)
                    sent_message = bot.sendMessage(chat_id=raid["grupo_id"], text=text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
                    delete_message_id = raid["message"]
                    raid["message"] = sent_message.message_id
                    saveRaid(raid)
                    logging.debug("supportmethods:auto_refloat: auto reflotada incursión %s mensaje %s" % (raid["id"], raid["message"]))
                    try:
                        bot.deleteMessage(chat_id=raid["grupo_id"],message_id=delete_message_id)
                    except Exception as e:
                        logging.debug("supportmethods:auto_refloat: error borrando post antiguo %s" % raid["message"])
                except:
                    logging.debug("supportmethods:auto_refloat: error reflotando incursión %s mensaje %s" % (raid["id"], raid["message"]))
                time.sleep(0.015)

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        logging.debug("TELEGRAM ERROR: Unauthorized - %s" % error)
    except BadRequest:
        logging.debug("TELEGRAM ERROR: Bad Request - %s" % error)
    except TimedOut:
        logging.debug("TELEGRAM ERROR: Slow connection problem - %s" % error)
    except NetworkError:
        logging.debug("TELEGRAM ERROR: Other connection problems - %s" % error)
    except ChatMigrated as e:
        logging.debug("TELEGRAM ERROR: Chat ID migrated?! - %s" % error)
    except TelegramError:
        logging.debug("TELEGRAM ERROR: Other error - %s" % error)
    except:
        logging.debug("TELEGRAM ERROR: Unknown - %s" % error)

def send_edit_instructions(group, raid, user_id, bot):
    what_text = format_text_pokemon(raid["pokemon"], raid["egg"])
    what_day = format_text_day(raid["timeraid"], group["timezone"])
    day = extract_day(raid["timeraid"], group["timezone"])
    if group["refloat"] == 1 or is_admin(raid["grupo_id"], user_id, bot):
        text_refloat="\n🎈 *Reflotar incursión*: `/reflotar`"
    else:
        text_refloat=""
    if group["candelete"] == 1 or is_admin(raid["grupo_id"], user_id, bot):
        text_delete="\n❌ *Borrar incursión*: `/borrar`"
    else:
        text_delete=""
    if raid["timeend"] is not None:
        text_endtime = extract_time(raid["timeend"])
    else:
        text_endtime = extract_time(raid["timeraid"])
    if day is None:
        daystr = ""
    else:
        daystr = "%s/" % day
    if raid["pokemon"] is None:
        pokemon = raid["egg"]
    else:
        pokemon = raid["pokemon"]
    try:
        bot.send_message(chat_id=user_id, text="Puedes editar la incursión %s %sa las *%s* en *%s* (identificador `%s`) contestando al mensaje de la incursión con los siguientes comandos:\n\n🕒 *Día/hora*: `/hora %s%s`\n🕒 *Hora a la que desaparece*: `/horafin %s`\n🌎 *Gimnasio*: `/gimnasio %s`\n👿 *Pokémon/nivel*: `/pokemon %s`\n\n🚫 *Cancelar incursión*: `/cancelar`%s%s" % (what_text, what_day, extract_time(raid["timeraid"]), raid["gimnasio_text"], raid["id"], daystr, extract_time(raid["timeraid"]), text_endtime, raid["gimnasio_text"], pokemon, text_delete, text_refloat), parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        logging.debug("Error sending instructions in private. Maybe conversation not started?")

def warn_people(warntype, raid, user_username, chat_id, bot):
    logging.debug("supportmethods:warn_people")
    people = getRaidPeople(raid["id"])
    group = getGroup(raid["grupo_id"])
    warned = []
    notwarned = []
    if people is None:
        return
    if group["alias"] is not None:
        incursion_text = "<a href='https://t.me/%s/%s'>incursión</a>" % (group["alias"], raid["message"])
    else:
        incursion_text = "incursión"
    for p in people:
        if p["username"] == user_username or p["novoy"] > 0:
            continue
        try:
            user_text = "@%s" % user_username if user_username is not None else "Se"
            if warntype == "cancelar":
                text_pokemon = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
                text = "❌ %s ha <b>cancelado</b> la %s %s a las %s en %s" % (user_text, incursion_text, text_pokemon, extract_time(raid["timeraid"]), raid["gimnasio_text"])
            elif warntype == "descancelar":
                text_pokemon = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
                text = "⚠️ %s ha <b>descancelado</b> la %s %s a las %s en %s" % (user_text, incursion_text, text_pokemon, extract_time(raid["timeraid"]), raid["gimnasio_text"])
            elif warntype == "borrar":
                text_pokemon = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
                text = "🚫 %s ha <b>borrado</b> la incursión %s a las %s en %s" % (user_text, text_pokemon, extract_time(raid["timeraid"]), raid["gimnasio_text"])
            elif warntype == "cambiarhora":
                text_day = format_text_day(raid["timeraid"], group["timezone"], "html")
                if text_day != "":
                    text_day = " " + text_day
                text_pokemon = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
                text = "⚠️ %s ha cambiado la hora de la %s %s en %s para las <b>%s</b>%s" % (user_text, incursion_text, text_pokemon, raid["gimnasio_text"], extract_time(raid["timeraid"]), text_day)
            elif warntype == "cambiarhorafin":
                text_pokemon = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
                text = "⚠️ %s ha cambiado la hora a la que se termina la %s %s en %s a las <b>%s</b> (¡ojo, la incursión sigue programada para la misma hora: %s!)" % (user_text, incursion_text, text_pokemon, raid["gimnasio_text"], extract_time(raid["timeend"]), extract_time(raid["timeraid"]))
            elif warntype == "borrarhorafin":
                text = "⚠️ %s ha borrado la hora a la que se termina la %s %s en %s (¡ojo, la incursión sigue programada para la misma hora: %s!)" % (user_text, incursion_text, raid["pokemon"], raid["gimnasio_text"], extract_time(raid["timeraid"]))
            elif warntype == "cambiargimnasio":
                text_pokemon = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
                text = "⚠️ %s ha cambiado el gimnasio de la %s %s para las %s a <b>%s</b>" % (user_text, incursion_text, text_pokemon, extract_time(raid["timeraid"]), raid["gimnasio_text"])
            elif warntype == "cambiarpokemon":
                text_pokemon = format_text_pokemon(raid["pokemon"], raid["egg"], "html")
                text = "⚠️ %s ha cambiado la %s para las %s en %s a incursión %s" % (user_text, incursion_text, extract_time(raid["timeraid"]), raid["gimnasio_text"], text_pokemon)
            bot.sendMessage(chat_id=p["id"], text=text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            warned.append(p["username"])
        except Exception as e:
            logging.debug("supportmethods:warn_people error sending message to %s: %s" % (p["username"],str(e)))
            notwarned.append(p["username"])
    if len(warned)>0:
        bot.sendMessage(chat_id=chat_id, text="He avisado por privado a: @%s" % ensure_escaped(", @".join(warned)), parse_mode=telegram.ParseMode.MARKDOWN)
    if len(notwarned)>0:
        bot.sendMessage(chat_id=chat_id, text="No he podido avisar a: @%s" % ensure_escaped(", @".join(notwarned)), parse_mode=telegram.ParseMode.MARKDOWN)

def get_settings_keyboard(chat_id, keyboard="main"):
    logging.debug("supportmethods:get_settings_keyboard")
    group = getGroup(chat_id)
    if group["alerts"] == 1:
        alertas_text = "✅ Permitir configurar alertas"
    else:
        alertas_text = "▪️ Permitir configurar alertas"
    if group["disaggregated"] == 1:
        disaggregated_text = "✅ Mostrar totales disgregados"
    else:
        disaggregated_text = "▪️ Mostrar totales disgregados"
    if group["plusdisaggregatedinline"] == 1:
        plusdisaggregatedinline_text = "✅ Mostrar «+1» disgregados por línea"
    else:
        plusdisaggregatedinline_text = "▪️ Mostrar «+1» disgregados por línea"
    if group["latebutton"] == 1:
        latebutton_text = "✅ Botón «Tardo»"
    else:
        latebutton_text = "▪️ Botón «Tardo»"
    if group["refloat"] == 1:
        refloat_text = "✅ Reflotar incursiones (comando /reflotar)"
    else:
        refloat_text = "▪️ Reflotar incursiones (comando /reflotar)"
    if group["candelete"] == 1:
        candelete_text = "✅ Borrar incursiones (comando /borrar)"
    else:
        candelete_text = "▪️ Borrar incursiones (comando /borrar)"
    if group["gotitbuttons"] == 1:
        gotitbuttons_text = "✅ Botones «¡Lo tengo!»"
    else:
        gotitbuttons_text = "▪️ Botones «¡Lo tengo!»"
    if group["locations"] == 1:
        locations_text = "✅ Ubicaciones"
    else:
        locations_text = "▪️ Ubicaciones"
    if group["validationrequired"] == 1:
        validationrequired_text = "✅ Validación obligatoria"
    else:
        validationrequired_text = "▪️ Validación obligatoria"
    if group["gymcommand"] == 1:
        gymcommand_text = "✅ Consultar gimnasios (comando /gym)"
    else:
        gymcommand_text = "▪️ Consultar gimnasios (comando /gym)"
    if group["raidcommand"] == 1:
        raidcommand_text = "✅ Crear incursiones (comando /raid)"
    else:
        raidcommand_text = "▪️ Crear incursiones (comando /raid)"
    if group["raidcommandorder"] == 1:
        raidcommandorder_text = "✅ Ordenar zonas/gimnasios por actividad"
    else:
        raidcommandorder_text = "▪️ Ordenar zonas/gimnasios por actividad"
    if group["babysitter"] == 1:
        babysitter_text = "✅ Modo niñero (borra mensajes)"
    else:
        babysitter_text = "▪️ Modo niñero (borra mensajes)"
    if group["timeformat"] == 1:
        timeformat_text = "✅ Mostrar horas en formato AM/PM"
    else:
        timeformat_text = "▪️ Mostrar horas en formato AM/PM"
    if group["listorder"] == 1:
        listorder_text = "✅ Agrupar apuntados por nivel/equipo"
    else:
        listorder_text = "▪️ Agrupar apuntados por nivel/equipo"
    if group["plusmax"] == 1:
        plusmax_text = "✅ Botón «+1» (máx. 1 acompañante)"
    elif group["plusmax"] in [2,3,5,10]:
        plusmax_text = "✅ Botón «+1» (máx. %s acompañantes)" % group["plusmax"]
    else:
        plusmax_text = "▪️ Botón «+1»"
    if group["plusdisaggregated"] == 1:
        plusdisaggregated_text = "✅ Botón «+1» por cada equipo"
    else:
        plusdisaggregated_text = "▪️ Botón «+1» por cada equipo"
    if group["snail"] == 1:
        snail_text = "✅ Marcar apuntados tarde (1 minuto)"
    elif group["snail"] in [3,5,10]:
        snail_text = "✅ Marcar apuntados tarde (%s minutos)" % group["snail"]
    else:
        snail_text = "▪️ Marcar apuntados tarde"
    if group["refloatauto"] in [5,10,15,30]:
        refloatauto_text = "✅ Reflotar automático (%s minutos)" % group["refloatauto"]
    else:
        refloatauto_text = "▪️ Reflotar automático"
    if group["rankingweek"] in [5,10,15,20,25]:
        rankingweek_text = "✅ Ranking semanal (TOP %s)" % group["rankingweek"]
    else:
        rankingweek_text = "▪️ Ranking semanal"
    if group["rankingmonth"] in [15,25,35,50]:
        rankingmonth_text = "✅ Ranking mensual (TOP %s)" % group["rankingmonth"]
    else:
        rankingmonth_text = "▪️ Ranking mensual"
    icons = iconthemes[group["icontheme"]]
    icontheme_text = "%s%s%s Tema de iconos" % (icons["Rojo"],icons["Azul"],icons["Amarillo"])

    if keyboard == "main":
        settings_keyboard = [[InlineKeyboardButton("Funcionamiento del grupo/canal »", callback_data='settings_goto_behaviour')], [InlineKeyboardButton("Comandos disponibles para usuarios »", callback_data='settings_goto_commands')], [InlineKeyboardButton("Opciones de vista de incursiones »", callback_data='settings_goto_raids')], [InlineKeyboardButton("Funcionamiento de incursiones »", callback_data='settings_goto_raidbehaviour')], [InlineKeyboardButton("Funcionamiento de rankings »", callback_data='settings_goto_ranking')], [InlineKeyboardButton("Terminado", callback_data='settings_done')]]
    elif keyboard == "behaviour":
        settings_keyboard = [[InlineKeyboardButton(locations_text, callback_data='settings_locations')], [InlineKeyboardButton(alertas_text, callback_data='settings_alertas')], [InlineKeyboardButton(babysitter_text, callback_data='settings_babysitter')], [InlineKeyboardButton(validationrequired_text, callback_data='settings_validationrequired')], [InlineKeyboardButton(refloatauto_text, callback_data='settings_refloatauto')], [InlineKeyboardButton("« Menú principal", callback_data='settings_goto_main')]]
    elif keyboard == "commands":
        settings_keyboard = [[InlineKeyboardButton(gymcommand_text, callback_data='settings_gymcommand')], [InlineKeyboardButton(raidcommand_text, callback_data='settings_raidcommand')], [InlineKeyboardButton(refloat_text, callback_data='settings_reflotar')], [InlineKeyboardButton(candelete_text, callback_data='settings_borrar')], [InlineKeyboardButton("« Menú principal", callback_data='settings_goto_main')]]
    elif keyboard == "raidbehaviour":
        settings_keyboard = [[InlineKeyboardButton(latebutton_text, callback_data='settings_botonllegotarde')], [InlineKeyboardButton(gotitbuttons_text, callback_data='settings_lotengo')], [InlineKeyboardButton(plusmax_text, callback_data='settings_plusmax')], [InlineKeyboardButton(plusdisaggregated_text, callback_data='settings_plusdisaggregated')], [InlineKeyboardButton("« Menú principal", callback_data='settings_goto_main')]]
    elif keyboard == "raids":
        settings_keyboard = [[InlineKeyboardButton(disaggregated_text, callback_data='settings_desagregado')], [InlineKeyboardButton(plusdisaggregatedinline_text, callback_data='settings_plusdisaggregatedinline')], [InlineKeyboardButton(timeformat_text, callback_data='settings_timeformat')], [InlineKeyboardButton(icontheme_text, callback_data='settings_icontheme')], [InlineKeyboardButton(listorder_text, callback_data='settings_listorder')], [InlineKeyboardButton(raidcommandorder_text, callback_data='settings_raidcommandorder')], [InlineKeyboardButton(snail_text, callback_data='settings_snail')], [InlineKeyboardButton("« Menú principal", callback_data='settings_goto_main')]]
    elif keyboard == "ranking":
        settings_keyboard = [[InlineKeyboardButton(rankingweek_text, callback_data='settings_rankingweek')], [InlineKeyboardButton(rankingmonth_text, callback_data='settings_rankingmonth')], [InlineKeyboardButton("« Menú principal", callback_data='settings_goto_main')]]

    settings_markup = InlineKeyboardMarkup(settings_keyboard)
    return settings_markup

def get_pokemons_keyboard():
    logging.debug("supportmethods:get_pokemons_keyboard")
    keyboard = []
    current_pokemons = getCurrentPokemons()
    for i in range(0,min(12,len(current_pokemons)-2),3):
        keyboard.append([InlineKeyboardButton(current_pokemons[i]["pokemon"], callback_data="iraid_pokemon_%s" % current_pokemons[i]["pokemon"]), InlineKeyboardButton(current_pokemons[i+1]["pokemon"], callback_data="iraid_pokemon_%s" % current_pokemons[i+1]["pokemon"]), InlineKeyboardButton(current_pokemons[i+2]["pokemon"], callback_data="iraid_pokemon_%s" % current_pokemons[i+2]["pokemon"])])
    keyboard.append([InlineKeyboardButton("Niv. 5", callback_data="iraid_pokemon_N5"), InlineKeyboardButton("Niv. 4", callback_data="iraid_pokemon_N4"), InlineKeyboardButton("Niv. 3", callback_data="iraid_pokemon_N3"), InlineKeyboardButton("EX", callback_data="iraid_pokemon_EX")])
    keyboard.append([InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def get_gyms_keyboard(group_id, page=0, zone=None, order="activity"):
    logging.debug("supportmethods:get_gyms_keyboard %s %s" % (group_id, page))
    keyboard = []
    current_gyms = getCurrentGyms(group_id, zone, order=order)
    maxgyms = min(14*page+13, len(current_gyms))

    for i in range(page*14, maxgyms,2):
        keyboard_row = [InlineKeyboardButton(current_gyms[i]["name"], callback_data="iraid_gym_%s" % current_gyms[i]["id"])]
        if i+1 < len(current_gyms):
            keyboard_row.append(InlineKeyboardButton(current_gyms[i+1]["name"], callback_data="iraid_gym_%s" % current_gyms[i+1]["id"]))
        keyboard.append(keyboard_row)

    if len(current_gyms)>14 and int(page) == 0:
        keyboard.append([InlineKeyboardButton("Página 2 >", callback_data="iraid_gyms_page2"), InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
    elif int(page) > 0:
        if len(current_gyms) > 14*(int(page)+1)+1:
            keyboard.append([InlineKeyboardButton("< Pág.%s" % str(page), callback_data="iraid_gyms_page%s" % str(page)), InlineKeyboardButton("Pág.%s >" % str(int(page)+2), callback_data="iraid_gyms_page%s" % str(int(page)+2)), InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
        else:
            keyboard.append([InlineKeyboardButton("< Página %s" % str(page), callback_data="iraid_gyms_page%s" % str(page)), InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
    else:
        keyboard.append([InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def get_zones_keyboard(group_id, order="activity"):
    logging.debug("supportmethods:get_zones_keyboard %s" % (group_id))
    keyboard = []
    zones = getZones(group_id, order=order)

    if len(zones) == 0:
        return False

    for i in range(0, len(zones), 2):
        keyboard_row = [InlineKeyboardButton(zones[i], callback_data="iraid_zone_%s" % zones[i].lower())]
        if i+1 < len(zones):
            keyboard_row.append(InlineKeyboardButton(zones[i+1], callback_data="iraid_zone_%s" % zones[i+1].lower()))
        keyboard.append(keyboard_row)

    keyboard.append([InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup

def get_days_keyboard(tz):
    logging.debug("supportmethods:get_days_keyboard")
    keyboard = []

    basedt = datetime.now(timezone(tz))
    minute = math.floor(basedt.minute/10)*10
    basedt = basedt.replace(minute=0,hour=0)

    dts = []
    for x in range(1,13):
        dts.append(basedt + timedelta(days=x))

    for i in range(0,10,3):
        h1 = dts[i].strftime('Día %d')
        h1k = dts[i].strftime('%d/00:00')
        h2 = dts[i+1].strftime('Día %d')
        h2k = dts[i+1].strftime('%d/00:00')
        h3 = dts[i+2].strftime('Día %d')
        h3k = dts[i+2].strftime('%d/00:00')
        keyboard.append([InlineKeyboardButton(h1, callback_data="iraid_date_%s" % h1k), InlineKeyboardButton(h2, callback_data="iraid_date_%s" % h2k), InlineKeyboardButton(h3, callback_data="iraid_date_%s" % h3k)])
    keyboard.append([InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
    pass

def get_times_keyboard(tz, date=None, offset=False):
    logging.debug("supportmethods:get_times_keyboard")
    keyboard = []
    dts = []

    nowdt = datetime.now(timezone(tz))
    try:
        argdt = datetime.strptime(date,"%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(tz))
    except:
        date = None

    if date == None or argdt.day == nowdt.day:
        basedt = nowdt
        minute = math.floor(basedt.minute/10)*10
        if offset is True:
            basedt = basedt.replace(minute=int(minute)+5)
        else:
            basedt = basedt.replace(minute=int(minute))
        for x in range(20,160,10):
            dts.append(basedt + timedelta(minutes=x))
        if offset == False:
            newoffset = 5
        else:
            newoffset = -5
    else:
        try:
            date = datetime.strptime(date,"%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(tz))
        except:
            date = date.replace(tzinfo=timezone(tz))
        if offset is True:
            basedt = date.replace(hour=9,minute=15)
        else:
            basedt = date.replace(hour=9,minute=0)
        for x in range(30,600,30):
            dts.append(basedt + timedelta(minutes=x))
        if offset == False:
            newoffset = 15
        else:
            newoffset = -15

    for i in range(0,len(dts)-3,3):
        h1 = dts[i].strftime('%H:%M')
        h1k = dts[i].strftime('%d/%H:%M')
        h2 = dts[i+1].strftime('%H:%M')
        h2k = dts[i+1].strftime('%d/%H:%M')
        h3 = dts[i+2].strftime('%H:%M')
        h3k = dts[i+2].strftime('%d/%H:%M')
        keyboard.append([InlineKeyboardButton(h1, callback_data="iraid_time_%s" % h1k), InlineKeyboardButton(h2, callback_data="iraid_time_%s" % h2k), InlineKeyboardButton(h3, callback_data="iraid_time_%s" % h3k)])

    if newoffset is not False:
        if newoffset > 0:
            hk = dts[0].strftime("%d/00" + (":" + str(newoffset).zfill(2)))
            timechange_text = "+%i minutos >" % newoffset
        else:
            hk = dts[0].strftime('%d/00:00')
            timechange_text = "< %i minutos" % newoffset
        keyboard.append([InlineKeyboardButton(timechange_text, callback_data="iraid_date_%s" % hk), InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
    else:
        keyboard.append([InlineKeyboardButton("Cancelar", callback_data="iraid_cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
    pass

def get_keyboard(raid):
    logging.debug("supportmethods:get_keyboard")
    global iconthemes
    group = getGroup(raid["grupo_id"])
    if raid["status"] == "started" or raid["status"] == "waiting":
        icons = iconthemes[group["icontheme"]]
        button_voy = InlineKeyboardButton("🙋Voy", callback_data='voy')
        button_novoy = InlineKeyboardButton("🙅No voy", callback_data='novoy')
        button_estoy = InlineKeyboardButton("✅Estoy", callback_data='estoy')
        button_plus = InlineKeyboardButton("👭+1", callback_data='plus1')
        button_plusy = InlineKeyboardButton("%s+1" % icons["Amarillo"], callback_data='plus1yellow')
        button_plusb = InlineKeyboardButton("%s+1" % icons["Azul"], callback_data='plus1blue')
        button_plusr = InlineKeyboardButton("%s+1" % icons["Rojo"], callback_data='plus1red')
        button_tardo = InlineKeyboardButton("🕒Tardo", callback_data='llegotarde')
        button_location = InlineKeyboardButton("🌎Ubicación", callback_data='ubicacion')
        button_loc = InlineKeyboardButton("🌎Ubi", callback_data='ubicacion')
        if group["plusdisaggregated"] == 0:
            keyboard_row1 = [button_voy]
            if group["plusmax"] > 0:
                keyboard_row1.append(button_plus)
            keyboard_row1.append(button_novoy)
            keyboard_row2 = [button_estoy]
            if group["latebutton"] == 1:
                keyboard_row2.append(button_tardo)
            if raid["gimnasio_id"] is not None:
                keyboard_row2.append(button_location)
            keyboard = [keyboard_row1, keyboard_row2]
        else:
            keyboard_row1 = [button_voy]
            if group["plusmax"] > 0:
                keyboard_row1.append(button_plusy)
                keyboard_row1.append(button_plusb)
                keyboard_row1.append(button_plusr)
            keyboard_row2 = [button_estoy]
            if group["latebutton"] == 1:
                keyboard_row2.append(button_tardo)
            keyboard_row2.append(button_novoy)
            if raid["gimnasio_id"] is not None:
                keyboard_row2.append(button_loc)
            keyboard = [keyboard_row1, keyboard_row2]
    else:
        keyboard = []
    if group is not None and group["gotitbuttons"] == 1 and (raid["status"] == "started" or raid["status"] == "ended"):
        keyboard.append([InlineKeyboardButton("👍¡Lo tengo!", callback_data='lotengo'), InlineKeyboardButton("👎¡Ha escapado!", callback_data='escapou')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def update_settings_message_timed(chat_id, sleep_time, bot):
    time.sleep(sleep_time)
    update_settings_message(chat_id, bot)

def update_settings_message(chat_id, bot, keyboard = "main"):
    logging.debug("supportmethods:update_settings_message: %s %s" % (chat_id, keyboard))
    group = getGroup(chat_id)

    settings_markup = get_settings_keyboard(chat_id, keyboard = keyboard)
    if keyboard == "main":
        text = "Elige una categoría para ver las opciones disponibles. Cuando termines, pulsa el botón <b>Terminado</b> para borrar el mensaje."
    elif keyboard == "raids":
        text = "Estas opciones permiten cambiar la forma en la que se muestran los listados de las incursiones."
    elif keyboard == "commands":
        text = "Estas opciones definen qué comandos pueden utilizar los usuarios que no son administradores. Los administradores siempre pueden utilizarlos igualmente."
    elif keyboard == "raidbehaviour":
        text = "Estas opciones permiten configurar características opcionales de las incursiones."
    elif keyboard == "behaviour":
        text = "Estas opciones son muy importantes porque definen el funcionamiento general del bot en el grupo/canal. Revisa la ayuda en caso de duda."
    elif keyboard == "ranking":
        text = "Estas opciones definen el comportamiento de los rankings del bot en el grupo/canal."

    return bot.edit_message_text(text=text, chat_id=chat_id, message_id=group["settings_message"], reply_markup=settings_markup, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

def edit_check_private(chat_id, chat_type, user_username, command, bot):
    logging.debug("supportmethods:edit_check_private")
    if chat_type != "private":
        if user_username is not None:
            text = "@%s el comando `/%s` solo funciona por privado.\n\n_(Este mensaje se borrará en unos segundos)_" % (ensure_escaped(user_username), command)
        else:
            text = "El comando `/%s` solo funciona por privado.\n\n_(Este mensaje se borrará en unos segundos)_" % command
        sent_message = bot.sendMessage(chat_id=chat_id, text=text,parse_mode=telegram.ParseMode.MARKDOWN)
        Thread(target=delete_message_timed, args=(chat_id, sent_message.message_id, 15, bot)).start()
        return False
    else:
        return True

def edit_check_private_or_reply(chat_id, chat_type, message, args, user_username, command, bot):
    logging.debug("supportmethods:edit_check_private_or_reply")
    if command in ["borrar", "cancelar", "reflotar", "descancelar", "cerrar"]:
        expectedargs = 0
    else:
        expectedargs = 1
    if len(args)>=expectedargs and hasattr(message, 'reply_to_message') and message.reply_to_message is not None:
        delete_message(chat_id, message.message_id, bot)
        reply_chat_id = message.reply_to_message.chat.id
        reply_message_id = message.reply_to_message.message_id
        raid = getRaidbyMessage(reply_chat_id, reply_message_id)
    elif chat_type == "private":
        if len(args)<(expectedargs+1) or (expectedargs>0 and not str(args[expectedargs-1]).isnumeric()):
            bot.sendMessage(chat_id=chat_id, text="¡No he reconocido los datos que me envías!",parse_mode=telegram.ParseMode.MARKDOWN)
            return
        raid_id = args[0]
        raid = getRaid(raid_id)
    else:
        delete_message(chat_id, message.message_id, bot)
        user_text = "@%s el" % ensure_escaped(user_username) if user_username is not None else "El"
        text = "%s comando `/%s` solo funciona por privado o contestando al mensaje de la incursión.\n\n_(Este mensaje se borrará en unos segundos)_" % (user_text, command)
        sent_message = bot.sendMessage(chat_id=chat_id, text=text,parse_mode=telegram.ParseMode.MARKDOWN)
        Thread(target=delete_message_timed, args=(chat_id, sent_message.message_id, 15, bot)).start()
        raid = None
    return raid

def parse_pokemon(pokestr):
    ret_pok = None
    ret_egg = None
    for pokemon in pokemonlist:
      m = re.match("^%s$" % pokemon, pokestr, flags=re.IGNORECASE)
      if m is not None:
        ret_pok = pokemon
        break

    if ret_pok is None:
        for egg in egglist:
            m = re.match("^%s$" % egg, pokestr, flags=re.IGNORECASE)
            if m is not None:
                ret_egg = egg
                break

    if ret_pok is None and ret_egg is None:
        for pokemon in pokemonlist:
            if distance(pokestr.lower(), pokemon.lower()) < 3:
                ret_pok = pokemon
                break

    return (ret_pok, ret_egg)

def parse_time(st, tz, strict=False):
    logging.debug("supportmethods:parse_time %s %s" % (st,tz))
    if strict:
        m = re.match("([0-9]{1,2}/)?([0-9]{1,2})[:.]([0-9]{1,2})h?", st, flags=re.IGNORECASE)
    else:
        m = re.match("([0-9]{1,2}/)?([0-9]{1,2})[:.]?([0-9]{0,2})h?", st, flags=re.IGNORECASE)
    if m is not None:
        hour = str(m.group(2))
        minute = m.group(3) or "00"
        logging.debug("supportmethods:parse_time parsing time %s %s" % (hour, minute))
        if m.group(1) is not None:
            day = m.group(1).replace("/","")
            logging.debug("supportmethods:parse_time parsing day %s" % (day))
        else:
            day = None
        if int(hour)<0 or int(hour)>24 or int(minute)<0 or int(minute)>59 or \
                                (day is not None and (int(day)<0 or int(day)>31)):
            logging.debug("supportmethods::parse_time failed parsing time from %s" % st)
            return None
    else:
        logging.debug("supportmethods::parse_time failed parsing time from %s" % st)
        return None

    localdatetime = datetime.now(timezone(tz))
    localtime = localdatetime.time()
    if int(hour) <= 12 and day is None:
        if (int(hour) <= 5 and int(localtime.hour) > 5) or \
            (int(localtime.hour) >= 15 and int(hour) <= 9 and int(hour)!=0):
            hour = int(hour) + 12

    dt = datetime.now(timezone(tz))
    if day is not None:
        if int(day) >= dt.day:
            dt = dt.replace(day=int(day))
        else:
            if dt.month == 12:
                dt = dt.replace(month=1, year=dt.year+1, day=int(day))
            else:
                dt = dt.replace(month=dt.month+1, day=int(day))
    dt = dt.replace(hour=int(hour),minute=int(minute))
    dt_str = dt.strftime("%Y-%m-%d %H:%M:00")
    logging.debug("supportmethods::parse_time parsed %s" % dt_str)
    return dt_str

def extract_time(formatted_datetime, format=0):
    logging.debug("supportmethods:extract_time %s" % formatted_datetime)
    if not isinstance(formatted_datetime,str):
        formatted_datetime = formatted_datetime.strftime("%Y-%m-%d %H:%M:%S")
    m = re.search("([0-9]{1,2}):([0-9]{0,2}):[0-9]{0,2}", formatted_datetime, flags=re.IGNORECASE)
    if m is not None:
        if format == 0:
            extracted_time = "%02d:%02d" % (int(m.group(1)), int(m.group(2)))
        else:
            hour = int(m.group(1))
            if hour >=12:
                ampm = "PM"
                if hour > 12:
                    hour = hour -12
            else:
                ampm = "AM"
            extracted_time = "%d:%02d %s" % (hour, int(m.group(2)), ampm)
        logging.debug("supportmethods::extract_time extracted %s" % extracted_time)
        return extracted_time
    else:
        logging.debug("supportmethods::parse_time failed extracting time from %s" % formatted_datetime)
        return None

def extract_day(timeraid, tzone):
    try:
        raid_datetime = datetime.strptime(timeraid,"%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(tzone))
    except:
        raid_datetime = timeraid.replace(tzinfo=timezone(tzone))
    now_datetime = datetime.now(timezone(tzone))
    difftime = raid_datetime - now_datetime
    if difftime.days > 1:
        return raid_datetime.day
    else:
        return None

def raidend_is_near_raidtime(timeraid, timeend, tzone):
    try:
        raid_datetime = datetime.strptime(timeraid,"%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(tzone))
    except:
        raid_datetime = timeraid.replace(tzinfo=timezone(tzone))
    try:
        raidend_datetime = datetime.strptime(timeend,"%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(tzone))
    except:
        raidend_datetime = timeend.replace(tzinfo=timezone(tzone))
    difftime = raidend_datetime - raid_datetime
    if difftime.seconds < 780:
        return round(difftime.seconds/60)
    else:
        return -1

def parse_profile_image(filename, desired_pokemon, inspect=False, inspectFilename="failed"):
    logging.debug("supportmethods:parse_profile_image %s" % filename)

    new_file, tmpfilename = tempfile.mkstemp(suffix=".png")
    os.close(new_file)

    # Validations will be saved for debugging purposes if passed inspect=True
    inspectdir = sys.path[0] + "/inspectimages"
    if not os.path.exists(inspectdir):
        os.makedirs(inspectdir)

    # Load possible pokemons
    if desired_pokemon is not None:
        thispoke_models = []
        for j in range(1, 10):
            pokfname = sys.path[0] + "/modelimgs/pokemon/%s%d.png" % (desired_pokemon,j)
            if not os.path.isfile(pokfname):
                break
            p = cv2.imread(pokfname)
            p = cv2.cvtColor(p, cv2.COLOR_BGR2GRAY)
            p = cv2.resize(p, (60,60))
            thispoke_models.append(p)
        pokemon = { "models":thispoke_models }

    # Load possible profiles
    profiles = {}
    for i in validation_profiles:
        p = cv2.imread(sys.path[0] + "/modelimgs/profiles/%s.png" % i)
        p = cv2.cvtColor(p, cv2.COLOR_BGR2GRAY)
        p = cv2.resize(p, (120,120))
        profiles[i] = { "model":p }

    # Load the full image
    image = cv2.imread(filename)
    height, width, _ = image.shape
    aspect_ratio = height/width

    logging.debug("supportmethods:parse_profile_image: Preprocessing image...")

    # Raise error for unsupported aspect ratios
    if aspect_ratio <= 1.64 or aspect_ratio >= 2.17:
        if inspect:
            cv2.imwrite(inspectdir + "/%s_img.png" % inspectFilename, image)
        raise Exception("Aspect ratio not supported")

    # Crop GalaxyS8+ fullscreen and normal mode bars
    if aspect_ratio > 2.04 and aspect_ratio < 2.06:
        logging.debug("supportmethods:parse_profile_image: Detected Galaxy S8+ Ratio")
        bottombar_img = image[int(height-height/12.3):int(height),int(0):int(width)] # y1:y2,x1:x2
        bottombar_gray = cv2.cvtColor(bottombar_img, cv2.COLOR_BGR2GRAY)
        topbar_img = image[int(0):int(height/12.3),int(0):int(width)] # y1:y2,x1:x2
        topbar_gray = cv2.cvtColor(bottombar_img, cv2.COLOR_BGR2GRAY)
        if inspect:
            cv2.imwrite(inspectdir + "/%s_img_s8_topbar_nml.png" % inspectFilename, topbar_img)
            cv2.imwrite(inspectdir + "/%s_img_s8_bottombar_nml.png" % inspectFilename, bottombar_img)
        if bottombar_gray.mean() < 40 and topbar_gray.mean() < 40:
            logging.debug("supportmethods:parse_profile_image: Detected Normal Black bars, cropping!")
            image = image[int(height/17.2):int(height-height/12.3),int(0):int(width)] # y1:y2,x1:x2
            height, width, _ = image.shape
            aspect_ratio = height/width
            if inspect:
                cv2.imwrite(inspectdir + "/%s_img_s8_nml.png" % inspectFilename, image)
        else:
            bottombar_img = image[int(height-height/15):int(height),int(0):int(width)] # y1:y2,x1:x2
            bottombar_gray = cv2.cvtColor(bottombar_img, cv2.COLOR_BGR2GRAY)
            bottombar_img = image[int(height-height/15):int(height),int(0):int(width)] # y1:y2,x1:x2
            bottombar_gray = cv2.cvtColor(bottombar_img, cv2.COLOR_BGR2GRAY)
            topbar_img = image[int(height/60):int(height/15),int(0):int(width)] # y1:y2,x1:x2
            topbar_gray = cv2.cvtColor(topbar_img, cv2.COLOR_BGR2GRAY)
            if inspect:
                cv2.imwrite(inspectdir + "/%s_img_s8_topbar_fs.png" % inspectFilename, topbar_img)
                cv2.imwrite(inspectdir + "/%s_img_s8_bottombar_fs.png" % inspectFilename, bottombar_img)
            if bottombar_gray.mean() < 40 and topbar_gray.mean() < 40:
                logging.debug("supportmethods:parse_profile_image: Detected Fullscreen Black bars, cropping!")
                image = image[int(height/14):int(height-height/14),int(0):int(width)] # y1:y2,x1:x2
                height, width, _ = image.shape
                aspect_ratio = height/width
                if inspect:
                    cv2.imwrite(inspectdir + "/%s_img_s8_fs.png" % inspectFilename, image)

    # Partially crop Oneplus T5S top bar
    if aspect_ratio > 1.99 and aspect_ratio < 2.01:
        logging.debug("supportmethods:parse_profile_image: Detected OnePlus T5S Ratio")
        topbar_img = image[int(height/44):int(height/22),int(0):int(width)] # y1:y2,x1:x2
        topbar_gray = cv2.cvtColor(topbar_img, cv2.COLOR_BGR2GRAY)
        if topbar_gray.mean() < 40:
            logging.debug("supportmethods:parse_prof ile_image: Detected Black top bar, cropping!")
            image = image[int(height/18):int(height),int(0):int(width)] # y1:y2,x1:x2
            height, width, _ = image.shape
            aspect_ratio = height/width
            if inspect:
                cv2.imwrite(inspectdir + "/%s_img_oneplus.png" % inspectFilename, image)

    # Crop large bars
    bottombar_img = image[int(height-height/14):int(height),int(0):int(width)] # y1:y2,x1:x2
    bottombar_gray = cv2.cvtColor(bottombar_img, cv2.COLOR_BGR2GRAY)
    if bottombar_gray.mean() < 40:
        image = image[int(0):int(height-height/14),int(0):int(width)] # y1:y2,x1:x2
        height, width, _ = image.shape
        aspect_ratio = height/width
        if inspect:
            cv2.imwrite(inspectdir + "/%s_img_largebar.png" % inspectFilename, image)

    # Crop small bars
    bottombar_img = image[int(height-height/17):int(height),int(0):int(width)] # y1:y2,x1:x2
    bottombar_gray = cv2.cvtColor(bottombar_img, cv2.COLOR_BGR2GRAY)
    if bottombar_gray.mean() < 40:
        image = image[int(0):int(height-height/17),int(0):int(width)] # y1:y2,x1:x2
        height, width, _ = image.shape
        aspect_ratio = height/width
        if inspect:
            cv2.imwrite(inspectdir + "/%s_img_smallbar.png" % inspectFilename, image)

    logging.debug("supportmethods:parse_profile_image: Ratio: %.2f" % aspect_ratio)
    logging.debug("supportmethods:parse_profile_image: Extracting image info...")

    # Extract profile layout for profile Testing
    profile_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    profile_gray = profile_gray[int(height/20):int(height),int(0):int(width)] # y1:y2,x1:x2
    profile_gray = cv2.resize(profile_gray, (120,120))
    cv2.rectangle(profile_gray,(60,1),(100,75),(255,255,255),-1) # delete trainer
    cv2.rectangle(profile_gray,(20,20),(60,75),(255,255,255),-1) # delete pokemon
    cv2.rectangle(profile_gray,(8,5),(60,20),(255,255,255),-1)   # delete nickname
    cv2.rectangle(profile_gray,(48,75),(72,85),(255,255,255),-1) # delete level

    # Test extracted profile layout against possible profile models
    chosen_profile = None
    chosen_similarity = 0.0
    for i in validation_profiles:
        profiles[i]["similarity"] = ssim(profiles[i]["model"], profile_gray)
        logging.debug("supportmethods:parse_profile_image: Similarity with %s: %.2f" % (i,profiles[i]["similarity"]))
        if profiles[i]["similarity"] > 0.7 and (chosen_profile is None or chosen_similarity < profiles[i]["similarity"]):
            chosen_profile = i
            chosen_similarity = profiles[i]["similarity"]
            if profiles[i]["similarity"] > 0.9:
                break
    if inspect:
        cv2.imwrite(inspectdir + "/%s_profile.png" % inspectFilename, profile_gray)
    logging.debug("supportmethods:parse_profile_image: Chosen profile: %s" % chosen_profile)

    # Prepare color boundaries to extract team
    team1_img = image[int(height/2):int(height/2+height/10),0:int(width/60)] # y1:y2,x1:x2
    boundaries = {
        "Rojo": ([0, 0, 140], [100, 70, 255]),
        "Azul": ([180, 50, 0], [255, 140, 60]),
        "Amarillo": ([0, 180, 200], [100, 225, 255])
    }
    chosen_color = None
    values = {}
    for color in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(boundaries[color][0], dtype = "uint8")
        upper = np.array(boundaries[color][1], dtype = "uint8")

        # find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(team1_img, lower, upper)
        output = cv2.bitwise_and(team1_img, team1_img, mask = mask)

        values[color] = output.mean()
        logging.debug("supportmethods:parse_profile_image: Mean value for color %s: %s" %(color,values[color]))

        if chosen_color is None or values[color] > values[chosen_color]:
            chosen_color = color
    if inspect:
        cv2.imwrite(inspectdir + "/%s_team.png" % inspectFilename, team1_img)
    logging.debug("supportmethods:parse_profile_image: Chosen color: %s" % chosen_color)

    # Prepare color boundaries to extract level, trainer and pokémon name
    boundaries = {
        "Rojo": ([35, 10, 105], [110, 100, 190]),
        "Azul": ([90, 75, 0], [190, 145, 80]),
        "Amarillo": ([0, 105, 180], [110, 198, 255])
    }
	# create NumPy arrays from the boundaries
    lower = np.array(boundaries[chosen_color][0], dtype = "uint8")
    upper = np.array(boundaries[chosen_color][1], dtype = "uint8")

    # Extract and OCR trainer and Pokémon name
    if aspect_ratio < 1.88:
        nick1_img = image[int(height/9):int(height/9*2),int(width/15):int(width/15+5*width/10)] # y1:y2,x1:x2
    elif aspect_ratio < 2.15:
        nick1_img = image[int(height/10+height/80):int(height/10*2-height/40),int(width/15):int(width/15+5*width/10)] # y1:y2,x1:x2
    else:
        nick1_img = image[int(height/11+height/80):int(height/11*2-height/60),int(width/15):int(width/15+5*width/10)] # y1:y2,x1:x2
    # find colors within the specified boundaries
    nick1_gray = cv2.inRange(nick1_img, lower, upper)
    nick1_gray = 255 - nick1_gray
    # Find boundaries and clean small artifacts
    cim, contours, chier = cv2.findContours(nick1_gray, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w*h > 15:
            continue
        # draw a white rectangle to mask the unwanted artifact
        cv2.rectangle(nick1_gray, (x, y), (x+w, y+h), (255, 255, 255), -1)
    # Do the OCR
    cv2.imwrite(tmpfilename, nick1_gray)
    text = pytesseract.image_to_string(Image.open(tmpfilename))
    if inspect:
        print("Originally recognized text: %s" % text)
    trainer_name = re.sub(r'\n+.*$','',text)
    trainer_name = trainer_name.replace(" ","").replace("|","l").replace("ﬁ","ri").replace("ﬂ","ri")
    pokemon_name = re.sub(r'^.*\n+([^ ]+)[ ]?','',text).replace(" ","")
    if pokemon_name == "":
        # Alternative pokemon name parsing
        pokemon_name = re.sub(r'^.*\n+(et|&|y|e)[ ]*','',text)
    if inspect:
        cv2.imwrite(inspectdir + "/%s_names_img.png" % inspectFilename, nick1_img)
        cv2.imwrite(inspectdir + "/%s_names_gray.png" % inspectFilename, nick1_gray)
    logging.debug("supportmethods:parse_profile_image: Trainer name: %s" % trainer_name)
    logging.debug("supportmethods:parse_profile_image: Pokemon name: %s" % pokemon_name)

    # Extract and OCR level
    if aspect_ratio < 1.81:
        level1_img = image[int(height/2+2*height/13):int(height-height/4-height/22),int(width/2):int(width/2+width/7)] # y1:y2,x1:x2
    elif aspect_ratio < 1.88:
        level1_img = image[int(height/2+height/8):int(height-height/4-height/16),int(width/2):int(width/2+width/7)] # y1:y2,x1:x2
    elif aspect_ratio < 2.15:
        level1_img = image[int(height/2+height/16):int(height-height/3-height/18),int(width/2):int(width/2+width/7)] # y1:y2,x1:x2
    else:
        level1_img = image[int(height/2+height/32):int(height-height/3-height/12),int(width/2):int(width/2+width/7)] # y1:y2,x1:x2
    # find colors within the specified boundaries
    level1_gray = cv2.inRange(level1_img, lower, upper)
    level1_gray = 255 - level1_gray
    # Do the OCR
    cv2.imwrite(tmpfilename, level1_gray)
    level = pytesseract.image_to_string(Image.open(tmpfilename), config="-psm 6")
    level = re.sub('O','0',level)
    numbers = re.findall(r'\d+', level)
    if len(numbers)>0:
        level = numbers[0]
    logging.debug("supportmethods:parse_profile_image: Level: %s" % level)
    try:
        if int(level)<5 or int(level)>40:
            level = None
    except:
        level = None
    if inspect:
        cv2.imwrite(inspectdir + "/%s_level_img.png" % inspectFilename, level1_img)
        cv2.imwrite(inspectdir + "/%s_level_gray.png" % inspectFilename, level1_gray)

    # Extract Pokemon
    if aspect_ratio < 1.81:
        pokemon_img = image[int(height/3):int(height-height/3),int(width/8):int(width/2)] # y1:y2,x1:x2
    elif aspect_ratio < 1.88:
        pokemon_img = image[int(height/3-height/42):int(height-height/3-height/42),int(width/8):int(width/2)] # y1:y2,x1:x2
    elif aspect_ratio < 2.15:
        pokemon_img = image[int(height/3-height/20):int(height-height/3-height/12),int(width/8):int(width/2)] # y1:y2,x1:x2
    else:
        pokemon_img = image[int(height/3-height/20):int(height-height/3-height/8),int(width/8):int(width/2)] # y1:y2,x1:x2
    pokemon_gray = cv2.cvtColor(pokemon_img, cv2.COLOR_BGR2GRAY)
    pokemon_gray = cv2.resize(pokemon_gray, (60,60))

    # Test extracted pokemon against possible pokemons
    chosen_pokemon = None
    chosen_similarity = 0.0
    if desired_pokemon is not None:
        for pokemon_model in pokemon["models"]:
            pokemon["similarity"] = ssim(pokemon_model, pokemon_gray)
            logging.debug("supportmethods:parse_profile_image: Similarity with %s: %.2f" % (desired_pokemon,pokemon["similarity"]))
            if pokemon["similarity"] > 0.7 and \
               (chosen_pokemon is None or chosen_similarity < pokemon["similarity"]):
               chosen_pokemon = desired_pokemon
               chosen_similarity = pokemon["similarity"]
               if pokemon["similarity"] > 0.9:
                   break
    else:
        chosen_pokemon = None

    if inspect:
        cv2.imwrite(inspectdir + "/%s_pokemon_img.png" % inspectFilename, pokemon_img)
        cv2.imwrite(inspectdir + "/%s_pokemon_gray.png" % inspectFilename, pokemon_gray)
    logging.debug("supportmethods:parse_profile_image: Chosen Pokemon: %s" % chosen_pokemon)

    # Cleanup and return
    os.remove(tmpfilename)
    return (trainer_name, level, chosen_color, chosen_pokemon, pokemon_name, chosen_profile)

locations_sent = []
def already_sent_location(user_id, location_id):
    logging.debug("supportmethods:already_sent_location")
    global locations_sent
    k = str(user_id)+"+"+str(location_id)
    if k in locations_sent:
        return True
    else:
        locations_sent.append(k)
        return False
