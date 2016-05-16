# test playlist creation

import os
from os import listdir
from os.path import isfile, join

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
    f = open(name_playlist,'w')
    for line in music_files:
        f.write(directory + '/' + line)
        f.write('\n')
    f.close()
    g.write(directory+'\n')

g.close()
