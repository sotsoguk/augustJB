"""
books
manages all books in ajb
"""

import os
import sqlite3 as lite
import sys
from os import listdir
from os.path import isfile, join
import ajb_config


class Ajb_Books(object):

    def __init__(self):
        self.con = lite.connect(ajb_config.db_conn["db_name"])
        self.path_music = ajb_config.dirs["path_music"]
        self.path_playlists = ajb_config.dirs["path_playlists"]
        # self.updateBooks()

    #
    def checkForActiveBook(self):
        with self.con:
            cur=self.con.cursor()
            cur.execute('SELECT Id FROM Books WHERE Active = 1')
            data = cur.fetchone()
            if data is None:
                print "No active Book!!"
                return False
            else:
                print "Active Book found!"
                return True
    # if no book is active, first book (id = 1) is set active
    def setFirstBookActive(self):
        if self.checkForActiveBook() == False:
            with self.con:
                cur=self.con.cursor()
                cur.execute('UPDATE Books SET Active = 1 WHERE Id = 1')

    def existsBook(self, rfid):
        print "In existsBook" + rfid
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                'SELECT Id FROM Books WHERE Rfid = "{rf}"'.format(rf=rfid))
            data = cur.fetchone()
            if data is None:
                print "%s not found in DB" % rfid
                return False
            else:
                print "%s found in DB" % rfid
                return True

    def getBookByRfid(self, rfid):
        print "In getBookByRfid:"
        bookName =""
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                'SELECT Name, NumTracks, Tracks, Secs FROM Books WHERE Rfid = "{rf}"'.format(rf=rfid))
            for row in cur:
                print row[0]
                print row[1]
                print row[2]
                print row[3]
                bookName = row[0]
        return bookName
        
    def number_books_db(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM Books")
            num_books = cur.fetchone()[0]
            print "NUmber of books %d" % num_books
            return num_books

    # List DB
    def printDB(self):
        print "DB contains "+str(self.number_books_db()) + " books\n\n"
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                'SELECT Id, Rfid, Name, NumTracks, Tracks, Secs, Active FROM Books ')
            for row in cur:
                print str(row[0])+".\t"+str(row[2])+ "\t @("+str(row[4])+","+str(row[5])+") " + str(row[6])
                
    # Resets progress for all books in DB
    def resetProgressDB(self):
        print "Reset progress..."
        with self.con:
            cur = self.con.cursor()
            cur.execute('UPDATE Books SET Tracks=0')
            cur.execute('UPDATE Books SET Secs=0')
    def updateProgressActiveBook(self,progress):
        print "Update Progress of active book"
        with self.con:
            cur = self.con.cursor()
            cur.execute('UPDATE Books SET Tracks=(?) WHERE Active = 1',(progress[0],))
            cur.execute('UPDATE Books SET Secs=(?) WHERE Active = 1',(progress[1],))
    def setActiveBook(self,rfid):
        print "Set active book"
        with self.con:
            cur = self.con.cursor()
            cur.execute('UPDATE Books SET Active=0 WHERE Active = 1')
            cur.execute('UPDATE Books SET Active=1 WHERE Rfid = (?)',(rfid,))

    def getActiveBook(self):
        print "Get active book"
        
    def deleteDB(self):
        print "deleteDB"
        with self.con:
            cur = self.con.cursor()
            cur.execute('DELETE FROM Books')

    # Scans for new books and adds them to DB. Does NOT delete orphan entries from DB
    def updateBooks(self):
        print "Updating..."

        ##

        music_directories = [name for name in os.listdir(
            self.path_music) if os.path.isdir(os.path.join(self.path_music, name))]
        g = open('playlists.lst', 'w')
        for directory in music_directories:
            path_tmp = self.path_music + '/' + directory
            music_files = [name for name in os.listdir(
                path_tmp) if os.path.isfile(os.path.join(path_tmp, name))]
            music_files.sort()
            name_playlist = self.path_playlists + '/' + directory + '.m3u'
            print path_tmp
            print name_playlist
            # check if book already in DB
            for line in music_files:
                extension = os.path.splitext(line)[1]
                if extension == '.id':
                    print "Fancy ID Found"
                else:
                    pass
            f = open(name_playlist, 'w')
            num_tracks = 0
            rfid_id = ''
            for line in music_files:
                extension = os.path.splitext(line)[1]
                # write only music files
                if extension in ['.mp3', '.m4a', '.wav', '.aac', '.mp4', '.maa']:
                    f.write(directory + '/' + line)
                    f.write('\n')
                    num_tracks += 1
                # detect rfid
                elif extension == '.id':
                    id_file = self.path_music+'/'+directory+'/'+line
                    with open(id_file, 'r') as rfile:
                        rfid_id = rfile.read().rstrip()
                        print rfid_id
                        print 'RFID %s FOUND in %s' % (rfid_id, id_file)

                else:
                    print "Unknown File format!\n"
            f.close()
            g.write(directory+'\n')
            print "Found %d music files" % num_tracks

            # check if book exists
            if self.existsBook(rfid_id):
                print "Book already in DB, updating tracks"
            else:
                print "Book not in DB, have to add it"
                print '-'*5
                print "Have too add:"
                print rfid_id
                print num_tracks
                print directory
                print '-'*5
                newId = self.number_books_db() + 1
                toInsert = (newId, rfid_id, directory, num_tracks, 0, 0,0)
                with self.con:
                    cur = self.con.cursor()
                    cur.execute("INSERT INTO Books VALUES (?,?,?,?,?,?,?)", toInsert)
        g.close()

        print "Done!"

if __name__ == '__main__':
    books_db = Ajb_Books()
    books_db.checkForActiveBook()
    books_db.setFirstBookActive()
    books_db.checkForActiveBook()
    #books_db.resetProgressDB();
    books_db.deleteDB()
    books_db.updateBooks()
    books_db.printDB()
    books_db.setActiveBook("229,67,7,109")
    books_db.checkForActiveBook()
    books_db.setActiveBook("136,4,101,44")
    books_db.printDB()
    #books_db.updateBooks()
    #print "in Main Books"
    #print "check DB exist"
    #bookEx = books_db.existsBook("121 111 111")
    #books_db.number_books_db()
