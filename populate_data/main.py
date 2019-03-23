import csv
# import MySQLdb as mysql
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
	db = mysql.connect(host="localhost",user="root",passwd="", db="Project")
	cursor = db.cursor()
	cursor.execute(query)
	db.close()

def get_song_row_data(row):
	return {
		's_id':row[0],
		'full_lyrics':row[1],
		'url':row[2],
		'release_date':row[3],
		'artist_name':row[4],
		'billboard_rank':row[5],
		'a_id':row[6],
		'song_name':row[7]
	}

def get_year(date):
	return date.split('-')[0]

def get_song_row_data(row):
	return {
		's_id':row[0],
		'genre':row[1],
	}

def populate_song(data):
	execute_query(pt.get_populate_artists_query(data['a_id'],data['artist_name']))
	execute_query(pt.get_populate_songs_query(data['s_id'], data['title'], get_year(data['release_date']), data['billboard_rank'], data['a_id'], data['full_lyrics']))
	for gram in xrange(1,5):
		populate_word_grams(gram, data)
	return True

def populate_word_grams(gram, data):
	lyrics = data['full_lyrics'].split()
	for i in xrange(0,len(lyrics), gram):
		words=' '.join(lyrics[i:i+gram]).lower()
		execute_query(pt.get_populate_phrases_query(words))
		execute_query(pt.get_populate_vocabulary_query(data['a_id'], words))
		execute_query(pt.get_populate_lyrics_query(data['s_id'], words))
	return True
	

def populate_genre():
	execute_query(pt.get_populate_genre_query(data['s_id'], data['genre']))
	return True


with open('./songs.csv') as f:
    reader = csv.reader(f)
    for row in reader:
    	data = get_song_row_data(row)
    	populate_song(data)

print "***Populated songs***"

with open('./song_genre.csv') as f:
    reader = csv.reader(f)
    for row in reader:
    	data = get_genre_row_data(row)
    	populate_genre(data)

print "***Populated song genres***"
