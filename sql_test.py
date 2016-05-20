import sqlite3 as lite
import sys

# con = None

# try:
# 	con = lite.connect('test.db')
	
# 	cur = con.cursor()
# 	cur.execute('SELECT SQLITE_VERSION()')

# 	data = cur.fetchone()

# 	print "SQLITE3 Version: %s" % data

# except lite.Error, e:
# 	print "Error %s:" % e.args[0]
# 	sys.exit(1)
# finally:
	
# 	if con:
# 		con.close()

con = lite.connect('test.db')

with con:
	cur = con.cursor() 

	cur.execute("CREATE TABLE Books(Id INT, Rfid TEXT, Name TEXT, NumTracks INT, Track INT, Secs INT)")
	cur.execute("INSERT INTO Books Values(1,'111 111 111','Revolver',12,0,0)")
	cur.execute("INSERT INTO Books Values(2,'222 222 222','Rubber Soul',13,0,0)")
	cur.execute("INSERT INTO Books Values(3,'333 333 333','Please Please Me',10,0,0)")
	# cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
	# cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
	# cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
	# cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
	# cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
	# cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
	# cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
	# cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
	# cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")
	# cur.execute('SELECT Id FROM Cars WHERE Id = 9')
	
	#data = cur.fetchone()
	#if data is None:
	#	print "found"
	# else:
		# print "not founds"
		