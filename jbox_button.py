import RPi.GPIO as GPIO
import time
import os
import threading
from subprocess import Popen, PIPE

active_playlist = 0
playlists =[]

##Loads the list of audiobooks / albums listed in
##
##'playlists.lst'
##
##in the main directory

def mpc_formatinfo(output):
    info_lines = output.split('\n')
    
def infoThread():
    threading.Timer(1.0, infoThread).start()
    cmd = "mpc -f \%album\%"
    p = Popen(["mpc","-f","%album%"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    info_lines = stdout.split('\n')
    info_status = info_lines[1].split(' ')

    print info_status[0] + " " + info_lines[0] + "\n" + info_status[1] + " " + info_status[4]
    
    
    
    
def loadPlaylists():
    f = open('playlists.lst','r')
    playlists =[]
    for line in f:
        playlists.append(line.rstrip())
    return playlists
    
def mpc_toggle(channel):
    print('Button pressed %s' %channel)
    os.system("mpc -q toggle")

def mpc_next(channel):
    print('Button pressed %s' %channel)
    os.system("mpc -q next")

def mpc_prev(channel):
    print('Button pressed %s' %channel)
    os.system("mpc -q prev")

def mpc_next_playlist(channel):
    global active_playlist, playlists
    
    print("INSIDE")
    print playlists
    print("playlist active %d" %active_playlist)
    num_playlists = len(playlists)
    active_playlist = (active_playlist + 1) % num_playlists
    print active_playlist
    os.system("mpc -q clear")
    cmdstr = "mpc -q load \""+playlists[active_playlist]+"\""
    print cmdstr
    os.system(cmdstr)
    os.system("mpc -q play")
    
def main():
    global playlists
    playlists = loadPlaylists()
    print playlists
    ajb_button1 = 18
    ajb_button2 = 16
    ajb_button3 = 20
    ajb_button4 = 21
    # setup pins
    # pins
    # 16
    # 18
    # 20
    # 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ajb_button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ajb_button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ajb_button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ajb_button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    

    
        
##    while True:
##        input_state = GPIO.input(
##        if input_state == False:
##            print('Button pressed')
##            playPause()
##            time.sleep(0.2)
    GPIO.add_event_detect(ajb_button1, GPIO.RISING, bouncetime=200)
    GPIO.add_event_detect(ajb_button2, GPIO.RISING, bouncetime=200)
    GPIO.add_event_detect(ajb_button3, GPIO.RISING, bouncetime=200)
    GPIO.add_event_detect(ajb_button4, GPIO.RISING, bouncetime=200)
    GPIO.add_event_callback(ajb_button1, mpc_toggle)
    GPIO.add_event_callback(ajb_button2, mpc_prev)
    GPIO.add_event_callback(ajb_button3, mpc_next)
    GPIO.add_event_callback(ajb_button4, mpc_next_playlist)
    infoThread()
    try:
        
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()

    
if __name__ == "__main__":
    main()
