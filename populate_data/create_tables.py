import MySQLdb as mysql

'''
Artists(a_id, name, image_url)
Songs(s_id, title, year, popularity_rating, a_id, full_lyrics)
Genre(s_id, genre)
Phrases(words, count)
Vocabulary(a_id, words, v_freq)
Lyrics(s_id, words, l_freq)
'''

'''
a_id - name, image_url
s_id - title, genre, year, popularity_rating, a_id, full_lyrics
words - count
a_id, words - v_freq
s_id, words - l_freq
'''


def execute_query(query):
	try:
		db = mysql.connect(host="localhost",user="root",passwd="", db="Project")
		cursor = db.cursor()
		cursor.execute(query)
		db.close()
	except Exception as e:
		print "Error: ", e
	


artist_table = '''
                CREATE TABLE Artists(
					a_id int,
					name varchar(255),
					image_url TEXT DEFAULT NULL,
					PRIMARY KEY (a_id)
				)
				'''

song_table = '''
                CREATE TABLE Songs(
					s_id int,
					title varchar(255),
					year varchar(255),
					popularity_rating int,
					a_id int,
					full_lyrics TEXT,
					PRIMARY KEY (s_id)
				)
				'''

genre_table ='''
				CREATE TABLE Genre(
					s_id int,
					genre varchar(255),
					PRIMARY KEY(s_id)
				)
			'''

phrase_table ='''
				CREATE TABLE Phrase(
					words varchar(255),
					count int,
					PRIMARY KEY(words)
				)
			'''

vocabulary_table ='''
				CREATE TABLE Vocabulary(
					a_id int,
					words varchar(255),
					v_freq int,
					PRIMARY KEY(a_id, words)
				)
			'''

lyrics_table ='''
				CREATE TABLE Lyrics(
					s_id int,
					words varchar,
					l_freq int,
					PRIMARY KEY(s_id, words)
				)
			'''


execute_query(artist_table)
execute_query(song_table)
execute_query(genre_table)
execute_query(phrase_table)
execute_query(vocabulary_table)
execute_query(lyrics_table)