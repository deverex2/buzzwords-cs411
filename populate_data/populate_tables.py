


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
			INSERT INTO Artists
			VALUES ({0}, {1})
		'''.format(a_id, name)
	return query

def get_populate_songs_query(s_id, title, year, popularity_rating, a_id, full_lyrics):
	query = '''
			INSERT INTO Songs
			VALUES ({0}, {1}, {2}, {3}, {4}, {5})
		'''.format(s_id, title, year, popularity_rating, a_id, full_lyrics)
	return query

def get_populate_genre_query(s_id, genre):
	query = '''
			INSERT INTO Genre
			VALUES ({0}, {1})
		'''.format(s_id, genre)
	return query

def get_populate_phrases_query(words):
	populate_phrases = '''
					begin trans
					if exists (select * from Phrases where words = {0})
					begin
					   update Phrases 
					   set count = count + 1
					   where words = {0}
					end
					else
					begin
					   insert into Phrases
					   values ({0}, 1)
					end
					commit trans
				'''.format(words)
	return populate_phrases

def get_populate_vocabulary_query(a_id, words):
	query = '''
					begin trans
					if exists (select * from Vocabulary where a_id = {0} AND words = {1})
					begin
					   update Vocabulary 
					   set v_freq = v_freq + 1
					   where a_id = {0} AND words = {1}
					end
					else
					begin
					   insert into Vocabulary
					   values ({0}, {1}, 1)
					end
					commit trans
				'''.format(a_id, words)
	return query

def get_populate_lyrics_query(s_id, words):
	query = '''
					begin trans
					if exists (select * from Lyrics where a_id = {0} AND words = {1})
					begin
					   update Lyrics 
					   set l_freq = l_freq + 1
					   where a_id = {0} AND words = {1}
					end
					else
					begin
					   insert into Lyrics
					   values ({0}, {1}, 1)
					end
					commit trans
				'''.format(s_id, words)
	return query