import RPi.GPIO as GPIO
import time
import os

paused = True

def playPause(channel):
    global paused
    print('Button pressed %s' %channel)
    if paused == True:
        os.system("mpc play")
        paused = False
    else:
        os.system("mpc pause")
        paused = True

def mpc_next(channel):
    print('Button pressed %s' %channel)
    os.system("mpc next")

def mpc_prev(channel):
    print('Button pressed %s' %channel)
    os.system("mpc prev")


def main():
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
    GPIO.add_event_detect(ajb_button1, GPIO.RISING)
    GPIO.add_event_detect(ajb_button2, GPIO.RISING)
    GPIO.add_event_detect(ajb_button3, GPIO.RISING)
    GPIO.add_event_detect(ajb_button4, GPIO.RISING)
    GPIO.add_event_callback(ajb_button1, playPause)
    GPIO.add_event_callback(ajb_button2, mpc_prev)
    GPIO.add_event_callback(ajb_button3, mpc_next)
    #GPIO.add_event_callback(ajb_button1, playPause)
    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()
    
if __name__ == "__main__":
    main()
