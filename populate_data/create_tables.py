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
a_id → name, image_url
s_id → title, genre, year, popularity_rating, a_id, full_lyrics
words → count
a_id, words → v_freq
s_id, words → l_freq
'''

def execute_query(query):
	db = mysql.connect(host="localhost",user="wajid2",db="")
	cursor = db.cursor()
	cursor.execute(query)
	db.close()


artist_table = '''
                CREATE TABLE Artists(
					a_id int,
					name varchar,
					image_url varchar DEFAULT NULL,
					PRIMARY KEY (a_id)
				)
				'''

song_table = '''
                CREATE TABLE Songs(
					s_id int,
					title varchar,
					year varchar,
					popularity_rating int,
					a_id int,
					full_lyrics varchar,
					PRIMARY KEY (s_id)
				)
				'''

genre_table ='''
				CREATE TABLE Genre(
					s_id int,
					genre varchar,
					PRIMARY KEY(s_id)
				)
			'''

phrase_table ='''
				CREATE TABLE Phrase(
					words varchar,
					count int,
					PRIMARY KEY(words)
				)
			'''

vocabulary_table ='''
				CREATE TABLE Vocabulary(
					a_id int,
					words varchar,
					v_freq varchar,
					PRIMARY KEY(a_id, words)
				)
			'''

lyrics_table ='''
				CREATE TABLE Lyrics(
					s_id int,
					words varchar,
					l_freq varchar,
					PRIMARY KEY(s_id, words)
				)
			'''

