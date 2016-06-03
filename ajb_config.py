"""
ajb_config.py

Configuration file for augustJukeBox

TODO

RFID serial connection
DB for storing progress """

import os

dirs = {"path_music": '/var/lib/mpd/music',"path_playlists": '/var/lib/mpd/playlists'}
db_conn = {"db_name":"books.db"}
mpd_conn = { "host" : "localhost", "port" : 6600}
btn_pins = [
    { 'pin' : 18, 'callback' : 'toggle', 'bouncetime' : 200},
    { 'pin' : 16, 'callback' : 'rewind', 'bouncetime' : 200},
    { 'pin' : 20, 'callback' : 'ffw', 'bouncetime' : 200},
    { 'pin' : 21, 'callback' : 'stop', 'bouncetime' : 200}
]
status_led_pin = 26
