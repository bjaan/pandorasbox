# pandorasbox - Pandora Music player

A Pandora Player remote control application that allows control via a Web Browser.

It sends commands (keypresses through a fifo-command file) in an [ExpressJS](https://expressjs.com/) Node.js web application to control a local instance of [Pianobar](https://github.com/PromyLOPh/pianobar) that is playing music from Pandora.com, while it displays the title information and cover art of the currently playing song.

Intended to be used on Raspian for the Raspberry Pi

![pandorasbox - playing a song in the web browser](https://raw.githubusercontent.com/bjaan/pandorasbox/main/pandorasbox-playing.png)
![pandorasbox - showing the available channels on Pandora.com which can be switched to](https://raw.githubusercontent.com/bjaan/pandorasbox/main/pandorasbox-channellist.png)

# pandorasbox features

Once configured:

* Automatically starts with the Raspberry Pi and starts playing music
* You can navigate to the local port 8888 on the Raspberry Pi, the link will look like http://pandorasbox.local:8888
* The currently playing song title, artist, and album is shown with the cover art is shown, and is updated seconds after starting the next song
* Pause, like or dislike, skip songs
* Create new stations based of an artist's style or a keyword, or switch to another station, or delete a station.

# Required software

* Raspbian GNU/Linux 10 (buster) - I installed a new Raspberry Pi image with the `ampi` hostname and connected it to the Internet
* Node.js 10.x for running the service - installed from the Raspbian repository using `sudo apt-get install npm nodejs`
* Pianobar - installed from the Raspbian repository using `sudo apt-get install pianobar`, and set-up the service, see below
* Python - already installed on the Raspbian by default (needed for the `eventcmd.py` used by Pianobar)

# Configuration changes

* Pianobar service file `/etc/systemd/system/pianobar.service` to set-up a service for Pianobar, called `pianobar` - and installed the service following these [instructions](https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/)

```ini
[Unit]
Description=pianobar
After=network.target

[Service]
ExecStartPre=/bin/sleep 30
ExecStart=/usr/bin/pianobar
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

* Pianobar configuration file at `/home/pi/.config/pianobar`

set `autostart_station = 123456` to an existing station id on your Pandora.com account, when you want the music to play automatically from something else as than the QuickMix channel

```sh
# This is an example configuration file for pianobar. You may remove the # from
# lines you need and copy/move this file to ~/.config/pianobar/config
# See manpage for a description of the config keys
#

# User (your Pandora.com account)
user = your-pandora@your-domain.com
password = password
# or
#password_command = gpg --decrypt ~/password

# Proxy (for those who are not living in the USA)
#control_proxy = socks5://127.0.0.1:4444/
#bind_to = if!tun0

# Keybindings
#act_help = ?
#act_songlove = +
#act_songban = -
act_stationaddmusic = A
#act_stationcreate = c
#act_stationdelete = d
#act_songexplain = e
#act_stationaddbygenre = g
#act_songinfo = i
#act_addshared = j
#act_songmove = m
#act_songnext = n
#act_songpause = S
#act_songpausetoggle = p
#act_songpausetoggle2 =  
#act_songplay = P
#act_quit = q
#act_stationrename = r
#act_stationchange = s
#act_stationcreatefromsong = v
act_songtired = T
#act_upcoming = u
#act_stationselectquickmix = x
#act_voldown = (
#act_volup = )
#act_volreset = ^

# Misc
audio_quality = high
autostart_station = 123456
event_command = /home/pi/.config/pianobar/eventcmd.py
fifo = /home/pi/.config/pianobar/ctl
sort = quickmix_10_name_az
volume = 0
ca_bundle = /etc/ssl/certs/ca-certificates.crt
#gain_mul = 1.0
#sample_rate = 48000
#audio_pipe = /tmp/mypipe

# Format strings
#format_nowplaying_song = [32m%t[0m by [34m%a[0m on %l[31m%r[0m%@%s
#format_nowplaying_song = [32m%t[0m by [34m%a[0m on %l%r%@%s
#ban_icon =  [32m</3[0m
#love_icon =  [31m<3[0m
#tired_icon =  [33mzZ[0m
#format_nowplaying_station = Station [35m%n[0m
#format_list_song = %i) %a - %t%r (%d)%@%s

#rpc_host = internal-tuner.pandora.com
partner_password = AC7IBG09A3DTSYM4R41UJWL07VLN8JI7
partner_user = android
device = android-generic
decrypt_password = R=U!LH$O2B#
encrypt_password = 6#26FRL$ZWD
```

* Pianobar event Python script `/home/pi/.config/pianobar/eventcmd.py`, needed by Pianobar to communicate when playback events happen

This file is available in this repository

* Pianobar command file (control fifo) `/home/pi/.config/pianobar/ctl`, needed by Pianobar to communicate commands

Execute `mkfifo /home/pi/.config/pianobar/ctl` to create the file
