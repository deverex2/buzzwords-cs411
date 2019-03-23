


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


def get_populate_artists_query(a_id, name):
	query = '''
			INSERT INTO Artists (a_id, name)
			VALUES ({0}, '{1}')
		'''.format(a_id, name)
	return query

def get_populate_songs_query(s_id, title, year, popularity_rating, a_id, full_lyrics):
	query = '''
			INSERT INTO Songs
			VALUES ({0}, '{1}', {2}, {3}, {4}, '{5}')
		'''.format(s_id, title, year, popularity_rating, a_id, full_lyrics)
	return query

def get_populate_genre_query(s_id, genre):
	query = '''
			INSERT INTO Genre
			VALUES ({0}, '{1}')
		'''.format(s_id, genre)
	return query

def get_populate_phrase_query(words):
	populate_phrases = '''
					INSERT INTO Phrase(words, count)
					VALUES ('{0}', 1)
					ON DUPLICATE KEY 
					UPDATE count = count + 1
				'''.format(words)
	return populate_phrases

def get_populate_vocabulary_query(a_id, words):
	query = '''
				INSERT into Vocabulary
				values ({0}, '{1}', 1)
				on duplicate key 
				update v_freq = v_freq+1
				'''.format(a_id, words)
	return query

def get_populate_lyrics_query(s_id, words):
	query = '''
			INSERT into Lyrics
			values ({0}, '{1}', 1)
			on duplicate key 
			update l_freq = l_freq+1
			'''.format(s_id, words)
	return query