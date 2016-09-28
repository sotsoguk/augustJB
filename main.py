# MASSIVE CHANGES
import time
import pdb
import signal
import sys
import os
import ajb_config
import RPi.GPIO as GPIO
from ajb_player import Ajb_Player
from ajb_status_led import Ajb_Status_Led
from ajb_books import Ajb_Books
from ajb_book import Ajb_Book
from threading import Thread
import MFRC522
# import sqlite3
# import rfid


class Ajb(object):

   
    def uid2str(self,uid):
        return str(uid[0])+","+ str(uid[1])+","+str(uid[2])+","+str(uid[3]);

    def __init__(self):

        # TODO RFID
        self.activeUidKey = [0,0,0,0]
        #self.active_book = Ajb_Book()
        self.books_db = Ajb_Books();
        GPIO.cleanup()
        # setup sigHandlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        self.status_led = Ajb_Status_Led(ajb_config.status_led_pin)
        thread = Thread(target=self.status_led.start)
        thread.start()
        # self.setup_gpio()
        self.MIFAREReader = MFRC522.MFRC522()
        self.player = Ajb_Player(ajb_config.mpd_conn, self.status_led)
        self.setup_gpio()
        self.player.loadPL("Please Please Me")

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(22, GPIO.OUT)
        # GPIO.output(self.NRSTPD, 1)
        # GPIO.output(self.NRSTPD, 1)
        # input buttons
        for pin in ajb_config.btn_pins:
            GPIO.setup(pin['pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin['pin'], GPIO.FALLING, callback=getattr(
                self.player, pin['callback']), bouncetime=pin['bouncetime'])

    def signal_handler(self, signal, frame):

        self.player.close()
        self.status_led.exit()
        GPIO.cleanup()
        sys.exit(0)

    


    def loop(self):

        while True:
            if self.player.is_playing():
                self.on_playing()
            # TODO Book finished
            # Scan for cards
            (status, TagType) = self.MIFAREReader.MFRC522_Request(
                self.MIFAREReader.PICC_REQIDL)
           # [te,se] = self.player.get_progress()
           # print str(te)+","+str(se)
            # If a card is found
            if status == self.MIFAREReader.MI_OK:
                print "Card detected"
                # Get the UID of card
                (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
                # Check for UID (otherwise skip)
                if status == self.MIFAREReader.MI_OK:
                    print "Card read UID"+ str(uid[0])+","+ str(uid[1])+","+str(uid[2])+","+str(uid[3])
                    print "Now:" + self.uid2str(uid)
                    # check if book exists
                    if (self.books_db.existsBook(self.uid2str(uid))):
                        bookName = self.books_db.getBookByRfid(self.uid2str(uid))
                        self.player.loadPL(bookName)
                        self.player.play()
                    if uid == self.activeUidKey:
                        print "Old uid"
                    else:
                        print "New uid"
                        self.activeUidKey = uid
                time.sleep(0.6)
                #self.player.toggle(10)
            # TODO RFID
            # rfid_placeholder = input("tag")
            # print rfid_placeholder
            # time.sleep(0.5)

    def on_playing(self):
        #status = self.player.get_status()
        [te,se] = self.player.get_progress()
        print str(te)+","+str(se)
        # TODO Update progress


if __name__ == '__main__':
    reader = Ajb()
    reader.loop()
