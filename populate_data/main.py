import csv
import MySQLdb as mysql
import populate_tables as pt


#song_id,lyrics,url,release_date,artist_name,billboard_rank,artist_id,song_name

#song_id,genre

'''
Artists(a_id, name, image_url)
Songs(s_id, title, year, popularity_rating, a_id, full_lyrics)
Genre(s_id, genre)
Phrases(words, count)
Vocabulary(a_id, words, v_freq)
Lyrics(s_id, words, l_freq)
'''

def execute_query(query):
	try:
		db = mysql.connect(host="localhost",user="root",passwd="", db="Project")
		cursor = db.cursor()
		cursor.execute(query)
		db.commit()
		db.close()
	except Exception as e:
		print "Error: ", e
	

def get_song_row_data(row):
	return {
		's_id':row[0],
		'full_lyrics':row[1].lower().replace("'",""),
		'url':row[2],
		'release_date':row[3],
		'artist_name':row[4].replace("'",""),
		'billboard_rank':row[5],
		'a_id':row[6],
		'title':row[7].replace("'","")
	}

def get_year(date):
	return date.split('-')[0]

def get_genre_row_data(row):
	return {
		's_id':row[0],
		'genre':row[1],
	}

def populate_song(data):
	execute_query(pt.get_populate_artists_query(data['a_id'],data['artist_name']))
	# print "populated artist"
	execute_query(pt.get_populate_songs_query(data['s_id'], data['title'], get_year(data['release_date']), data['billboard_rank'], data['a_id'], data['full_lyrics']))
	# print "populated song"
	for gram in xrange(1,2):
		populate_word_grams(gram, data)
	return True

def populate_word_grams(gram, data):
	lyrics = data['full_lyrics'].split()
	for i in xrange(0,len(lyrics)):
		words=' '.join(lyrics[i:i+gram])
		execute_query(pt.get_populate_phrase_query(words))
		# print "populated phrase"
		execute_query(pt.get_populate_vocabulary_query(data['a_id'], words))
		# print "populated vocab"
		execute_query(pt.get_populate_lyrics_query(data['s_id'], words))
		# print "populated lyrics"
	return True
	

def populate_genre():
	execute_query(pt.get_populate_genre_query(data['s_id'], data['genre']))
	print "populated genre"
	return True


with open('./songs.csv') as f:
    reader = csv.reader(f)
    for row in reader:
    	data = get_song_row_data(row)
    	populate_song(data)
    	print "populate song: ", data['title']

print "***Populated songs***"

with open('./song_genres.csv') as f:
    reader = csv.reader(f)
    for row in reader:
    	data = get_genre_row_data(row)
    	populate_genre(data)

print "***Populated song genres***"
