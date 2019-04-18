import MySQLdb as mysql



def get_lyrics(genre, year):
	query = _get_lyrics_query(genre, year)
	try:
		db = mysql.connect(host="localhost",user="root",passwd="", db="Project")
		cursor = db.cursor()
		cursor.execute(query)
		all_lyrics = []
		for row in cursor.fetchall():
			all_lyrics.append(row[0])
		db.close()
		return '    '.join(all_lyrics)
	except Exception as e:
		print "Error: ", e
	

def _get_lyrics_query(genre, year):
	return 	'''
			SELECT full_lyrics 
			FROM genre_lyrics_view 
			WHERE genre='{0}' and year='{1}'
			'''.format(genre, year)


if __name__ == '__main__':

	print get_lyrics('Pop','2006')