#!/usr/bin/env python

import os
import sys
from os.path import expanduser, join

path = os.environ.get('XDG_CONFIG_HOME')
if not path:
    path = expanduser("~/.config")
else:
    path = expanduser(path)

fnnp = join(path, 'pianobar', 'nowplaying')
fnevent = join(path, 'pianobar', 'event')

info = sys.stdin.readlines()
event = sys.argv[1]

if event == 'songstart':
    with open(fnnp, 'w') as f:
        f.write("".join(info))
	f.close()

with open(fnevent, 'w') as f:
	f.write(event)
	f.close()