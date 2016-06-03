
# test playlist creation

import sqlite3 as lite
import sys
import os
from os import listdir
from os.path import isfile, join

# db stuff
con = lite.connect('test.db')

# for each directory of music files create playlist
path_music = '/var/lib/mpd/music'
path_playlists = '/var/lib/mpd/playlists'
music_directories = [name for name in os.listdir(path_music) if os.path.isdir(os.path.join(path_music,name))]
g = open('playlists.lst','w')
for directory in music_directories:
    path_tmp = path_music + '/' + directory
    music_files = [name for name in os.listdir(path_tmp) if os.path.isfile(os.path.join(path_tmp,name))]
    music_files.sort()
    name_playlist = path_playlists + '/' + directory + '.m3u'
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
    for line in music_files:
        extension = os.path.splitext(line)[1]
        # write only music files
        if extension in ['.mp3','.m4a','.wav','.aac','.mp4','.maa']:
            f.write(directory + '/' + line)
            f.write('\n')
        # detect rfid     
        elif extension == '.id':
            id_file = path_music+'/'+directory+'/'+line
            print 'RFID FOUND in %s' % id_file


        else:
            print "Unknown File format!\n"
    f.close()
    g.write(directory+'\n')

g.close()
