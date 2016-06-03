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
		self.updateBooks()

	def existsBook(self,rfid):
		with self.con:
			cur = self.con.cursor()
			cur.execute('SELECT Id FROM Books WHERE Rfid = "{rf}"'.format(rf=rfid))
			data = cur.fetchone()
			if data is None:
				print "%s not found in DB" %rfid
				return False
			else:
				print "%s found in DB" %rfid
				return True

	def number_books_db(self):
		with self.con:
			cur = self.con.cursor()
			cur.execute("SELECT COUNT(*) FROM Books")
			num_books = cur.fetchone()[0]
			print "NUmber of books %d" %num_books

	def updateBooks(self):
		print "Updating..."

		##

		music_directories = [name for name in os.listdir(self.path_music) if os.path.isdir(os.path.join(self.path_music,name))]
		g = open('playlists.lst','w')
		for directory in music_directories:
		    path_tmp = self.path_music + '/' + directory
		    music_files = [name for name in os.listdir(path_tmp) if os.path.isfile(os.path.join(path_tmp,name))]
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
		    f = open(name_playlist,'w')
		    num_tracks = 0
		    rfid_id =''
		    for line in music_files:
		        extension = os.path.splitext(line)[1]
		        # write only music files
		        if extension in ['.mp3','.m4a','.wav','.aac','.mp4','.maa']:
		            f.write(directory + '/' + line)
		            f.write('\n')
		            num_tracks +=1
		        # detect rfid     
		        elif extension == '.id':
		            id_file = self.path_music+'/'+directory+'/'+line
		            with open(id_file,'r') as rfile:
		            	rfid_id = rfile.read().rstrip()
		            	print rfid_id
		            	print 'RFID %s FOUND in %s' % (rfid_id,id_file)


		        else:
		            print "Unknown File format!\n"
		    f.close()
		    g.write(directory+'\n')
		    print "Found %d music files" %num_tracks

		    # check if book exists
		    if self.existsBook(rfid_id):
		    	print "Book already in DB, updating tracks"
		    else:
		    	print "Book not in DB, have to add it"
		    	print '-'*5
		    	print "Have to add:"
		    	print rfid_id
		    	print num_tracks
		    	print directory
		    	print '-'*5
		    	newId = self.number_books_db() + 1
		    	with self.con:
		    		cur = self.con.cursor()
		    		cur.execute("INSERT INTO Books Values")
		g.close()

		print "Done!"

if __name__ == '__main__':
	books_db = Ajb_Books()
	print "in Main Books"
	print "check DB exist"
	bookEx = books_db.existsBook("121 111 111")
	books_db.number_books_db()