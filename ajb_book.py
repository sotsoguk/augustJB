"""
ajb_book.py

Ajb_Book manages all books
- creates playlist from files
- manages playlists
- manages progress
"""

import os
from os import listdir
from os.path import isfile, join

class Ajb_Book(object):

	def __init__(self):
		self._tag_id = [0,0,0,0]
		self._name = ""
		self._num_tracks = 0
		self._progress = [0,0]

	# def __init__(self,tag_id,name):
	# 	self._tag_id = tag_id
	# 	self._name = name
	# 	self._num_tracks = 0
	# 	self._progress = [0,0]


	# getter / setter
	def getTagId(self):
		return self._tag_id

	def setTagId(self,tag_id):
		self._tag_id = tag_id

	def getName(self):
		return self._name

	def setName(self,name):
		self._name = name

	def getNumTrack(self):
		return self._num_tracks

	def setNumTracks(self,num_tracks):
		self._num_tracks = num_tracks

	def getProgress(self):
		return self._progress[0],self._progress[1]

	def setProgress(self,track,secs):
		self._progress[0] = track
		self._progress[1] = secs


# Testroutine
if __name__ =='__main__':
	test_book = Ajb_Book([136,4,101,44],'Revolver')
	print test_book.getName()
	test_book.setProgress(2,12)
	track, sec = test_book.getProgress()
	print "(%d,%d)"%(track,sec)