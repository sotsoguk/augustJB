"""
ajb_player.py
"""

from mpd import MPDClient
from threading import Lock
from ajb_book import Ajb_Book
import ajb_config
import re
from ajb_books import Ajb_Books


class LockableMPDClient(MPDClient):
    def __init__(self, use_unicode=False):
        super(LockableMPDClient, self).__init__()
        self.use_unicode = use_unicode
        self._lock = Lock()

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, type, value, traceback):
        self.release()


class Ajb_Player(object):

    def __init__(self, conn_details, status_led):

        self.status_led = status_led
        # self.book = Ajb_Book()
        self.justStopped = False
        self.mpd_client = LockableMPDClient()
        with self.mpd_client:
            self.mpd_client.connect(**conn_details)

            self.mpd_client.update()
            self.mpd_client.clear()
            ##self.mpd_client.add('Revolver')
            ##self.mpd_client.play()
            # self.mpd_client.setvol(70)

    # toggle play / pause
    def toggle(self, channel):
	print channel
        with self.mpd_client:
            state = self.mpd_client.status()['state']
            if state == 'play':
                self.status_led.action = 'blink_pause'
                self.mpd_client.pause()
            elif state == 'pause':
                self.status_led.action = 'blink'
                self.mpd_client.play()
            elif self.is_playing:
                self.status_led.interrupt('blink_fast', 3)
                print "playing again"
                # self.mpd_client.seek(0, 0)
                self.status_led.action = 'blink'
                self.mpd_client.play()
            new_state = self.mpd_client.status()['state']
            print 'was %s, now  %s' % (state, new_state)

    def update(self):
        with self.mpd_client:
            self.mpd_client.update()

    def ffw(self, channel):
        print channel
	self.status_led.interrupt('blink_fast', 3)
        with self.mpd_client:
            self.mpd_client.next()

    def rewind(self, channel):
        # rewind 20 secs

        self.status_led.interrupt('blink_fast', 3)

        with self.mpd_client:
            self.mpd_client.previous()
# if self.is_playing():
##            song_index = int(self.book.part) -1
##            elapsed = int(self.book.elapsed)
##
# with self.mpd_client:
# if elapsed > 20:
##                    self.mpd_client.seek(song_index, elapsed -20)
# elif song_index >0:
##                    prev_song = self.mpd_client.playlistinfo(song_index -1)[0]
##                    prev_song_len = int(prev_song['time'])
##
# if prev_song_len >0:
##                        self.mpd_client.seek(song_index-1, prev_song_len -20)
# else:
##                        self.mpd_client.seek(song_index-1, 0)
# else:
# self.mpd_client.seek(0,0)

    def volume_up(self, channel):
        volume = int(self.get_status()['volume'])
        self.set_volume(min(volume + 10, 100))

    def volume_down(self, channel):
        volume = int(self.get_status()['volume'])
        self.set_volume(max(volume - 10, 0))

    def set_volume(self, volume):
        self.status_led.interrupt('blink_fast', 3)
        with self.mpd_client:
            self.mpd_client.setvol(volume)
            print "volume now at %d" % volume

    def stop(self, channel):

        
        print "stopping!"
        self.justStopped = True
        self.playing = False
        # self.book.reset()

        self.status_led.action = 'on'

        with self.mpd_client:
            self.mpd_client.stop()
            # self.mpd_client.clear()
            self.mpd_client.seek(0, 0)
            self.mpd_client.stop()

    def play(self):
        # TODO progress, file loading etc
        with self.mpd_client:
            self.mpd_client.play()

        self.status_led.action = 'blink'

    def pause(self):
        # TODO progress, file loading etc
        with self.mpd_client:
            self.mpd_client.pause()

        self.status_led.action = 'blink_pause'

    def is_playing(self):
        return self.get_status()['state'] == 'play'

    def get_status(self):
        with self.mpd_client:
            return self.mpd_client.status()

    def get_file_info(self):
        with self.mpd_client:
            return self.mpd_client.currentsong()
    def get_progress(self):
        with self.mpd_client:
            if (self.mpd_client.status()['state'] == 'play') or (self.mpd_client.status()['state'] == 'pause'):
                track = int(float(self.mpd_client.status()['song']))
                secs = int(float(self.mpd_client.status()['elapsed']))
                return [track, secs]
            else:
                return [0,0]    

    def set_progress(self,progress):
        with self.mpd_client:
            self.mpd_client.seek(progress[0],progress[1])
            
    def close(self):
        self.stop(10)
        self.mpd_client.close()
        self.mpd_client.disconnect()

    def clearPL(self):
        print "Clear Playlist"
        with self.mpd_client:
            self.mpd_client.clear()

    def loadPL(self,namePL):
        print "Load Playlist:"+ namePL
        with self.mpd_client:
            self.mpd_client.clear()
            self.mpd_client.load(namePL)
