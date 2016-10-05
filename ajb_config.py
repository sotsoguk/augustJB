"""
ajb_config.py

Configuration file for augustJukeBox

TODO

RFID serial connection
DB for storing progress """

import os

dirs = {"path_music": '/home/pi/Music',"path_playlists": '/var/lib/mpd/playlists'}
db_conn = {"db_name":"books.db"}
mpd_conn = { "host" : "localhost", "port" : 6600}
# BOARD Numbering
btn_pins = [
     { 'pin' : 7, 'callback' : 'toggle', 'bouncetime' : 200},
     { 'pin' : 11, 'callback' : 'rewind', 'bouncetime' : 200},
     { 'pin' : 13, 'callback' : 'ffw', 'bouncetime' : 200},
     { 'pin' : 15, 'callback' : 'stop', 'bouncetime' : 200}
]
status_led_pin = 15


# Board Numbering
#btn_pins = [
#    { 'pin' : 12, 'callback' : 'toggle', 'bouncetime' : 400},
#    { 'pin' : 36, 'callback' : 'rewind', 'bouncetime' : 400},
#    { 'pin' : 38, 'callback' : 'ffw', 'bouncetime' : 400},
#    { 'pin' : 40, 'callback' : 'stop', 'bouncetime' : 400}
# ]
# status_led_pin = 37
 

