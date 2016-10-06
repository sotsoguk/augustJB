#!/usr/bin/env python

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
import argparse
# import sqlite3
# import rfid

# Just a small function to read & print out the UID of a new RFID chip

def readKey():
     
    MIFAREReader = MFRC522.MFRC522()
    print "Waiting for RFID tags ..."
    print "Exit with Ctrl + C"
    while True:
       (status, TagType) = MIFAREReader.MFRC522_Request(
            MIFAREReader.PICC_REQIDL) 
       if status == MIFAREReader.MI_OK:
            print "Card detected"
            # Get the UID of card
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            # Check for UID (otherwise skip)
            if status == MIFAREReader.MI_OK:
                print "UID\t"+ str(uid[0])+","+ str(uid[1])+","+str(uid[2])+","+str(uid[3])

class Ajb(object):

   
    def uid2str(self,uid):
        return str(uid[0])+","+ str(uid[1])+","+str(uid[2])+","+str(uid[3]);

    def __init__(self):

        # Startup: What has to be done

        self.activeUidKey = [0,0,0,0]
        #self.active_book = Ajb_Book()
        
        # DB loading
        self.books_db = Ajb_Books()
        self.books_db.updateBooks()
        if self.books_db.number_books_db() == 0:
            print "No Books in Database."
            sys.exit(0)
        if self.books_db.checkForActiveBook() == False:
            self.books_db.setFirstBookActive()


        GPIO.setwarnings(False)
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
        ## self.player.loadPL("Please Please Me")
        self.active_book = self.books_db.getActiveBook()
        # self.player.book_db = self.books_db 
        self.player.loadPL(self.active_book._name)

        print "Loaded PL "+self.active_book._name
        self.player.set_progress(self.active_book._progress)
        self.player.pause()
        ## load active book

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
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
            if self.player.justStopped == True:
                print "Just Stopped"
                [te,se] = self.player.get_progress()
                print str(te)+","+str(se)
                self.books_db.updateProgressActiveBook([te,se])
                self.player.justStopped = False
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
                   
                        
                    if self.uid2str(uid) == self.active_book._tag_id:
                        print "Book already playing"
                    else:
                        print "New UID => Change book"
                        print "Update DB"
			self.books_db.updateBooks()
                        self.player.update()
			# self.activeUidKey = uid
                        print "HERE UPDATE BOOK STATUS"
                        [te,se] = self.player.get_progress()
                        print str(te)+","+str(se)
                        self.books_db.updateProgressActiveBook([te,se])
                        if (self.books_db.existsBook(self.uid2str(uid))):
                            
                            self.books_db.setActiveBook(self.uid2str(uid))
                            self.active_book = self.books_db.getActiveBook()
                            self.player.loadPL(self.active_book._name)
                            print "Loaded PL "+self.active_book._name
                            self.player.set_progress(self.active_book._progress)

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
        self.books_db.updateProgressActiveBook([te,se])
        # TODO Update progress


if __name__ == '__main__':
    # Argument handling
    parser = argparse.ArgumentParser(description="august's JukeBox")
    parser.add_argument('--readKey', action ='store_true', default = False, 
                        dest = 'readKey',
                        help='Read out RFID keys')
    parser.add_argument('--showDB', action = 'store_true', default = False,
                        dest = 'showDB',
                        help = 'Print book database')
    parser.add_argument('--resetDB', action = 'store_true', default = False,
                        dest = 'resetDB',
                        help = 'delete DB & rescan')
    parser.add_argument('--resetProgress', action='store_true', default = False,
                        dest = 'resetProgress',
                        help = 'reset progress of all books')
    results = parser.parse_args()

    ## Read UID & print
    if results.readKey:
        readKey()
       
    elif results.showDB:
        books_db = Ajb_Books()
        books_db.printDB()
    elif results.resetDB:
        books_db = Ajb_Books()
        books_db.deleteDB()
        books_db.updateBooks()
    elif results.resetProgress:
        books_db = Ajb_Books()
        books_db.resetProgressDB()
    else:
        reader = Ajb()
        reader.loop()
