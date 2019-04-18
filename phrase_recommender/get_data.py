import MySQLdb as mysql



def get_lyrics(query):
	try:
		db = mysql.connect(host="localhost",user="root",passwd="", db="Project")
		cursor = db.cursor()
		cursor.execute(query)
		for row in curson.fetchall():
			print row
		db.close()
	except Exception as e:
		print "Error: ", e
	

def get_lyrics_query(genre, year):
	return 	'''
			SELECT full_lyrics, year 
			FROM genre_lyrics_view 
			WHERE genre={0} and year={1}
			'''.format(genre, year)


if __name__ == '__main__':
	
	get_lyrics(get_lyrics_query('Pop','2006'))