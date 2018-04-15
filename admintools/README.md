# Detective YellowCopyrightedRat Admin Tools

This is an optional website directed towards administrators, to gather useful ifnormation.

## Requirements

Requires Python 3.4+, the main bot dependencies, and some additional Python dependencies.

To install the additional Python dependencies, just run this from the `admintools` directory:

```bash
sudo pip3 install -r requirements.txt
```
Backend is served in port 8044 and frontend in port 8045. A reverse proxy must be configured so the frontend is served in `/` and the backend is served in `/data/`. [Nginx](http://nginx.org/) is recommended for this. There is an example Nginx configuration file called `nginx-conf` available.

[Cerbot](https://certbot.eff.org/) is recommended to serve the website through HTTPS with a proper certificate.

## Configuration

Before running it, you must add a configuration section to `~/.config/detectivepikachu/config.ini` with these variables:

```
[admintools]
apiid=000000
apihash=ffeefe000000000000000000000000dd
recaptchasecret=xXXXXXXXXXXXXXXXXXXXXXXXXXXx-xXXXXXXXXXXXX
```

Get the `apiid` and `apihash` from Telegram [following these instructions](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id).

Obtain a recaptcha v2 secret [from the reCAPTCHA admin site](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id).
Also, set the proper site key in the file `frontend/index.html`. Look for `data-sitekey` to find it.

## License

Copyright (C) 2017 Jorge Suárez de Lis <hey@gentakojima.me>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
