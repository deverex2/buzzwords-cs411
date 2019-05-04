from nltk.corpus import stopwords
from textblob import TextBlob
from lexicalrichness import LexicalRichness
import nltk
import re
import csv

def getLyrics(artists):
	firstArtist = artists[0]
	secondArtist = artists[1]
	lyricsIndex = 1
	artistIndex = 4
	firstArtistLyricsList = []
	secondArtistLyricsList = []	
	with open('populate_data/songs.csv') as csvFile:
        	csvReader = csv.reader(csvFile)
        	for song in csvReader:
                	lyrics = song[lyricsIndex].strip()
                	artistName = song[artistIndex]
                	if artistName == firstArtist:
                        	firstArtistLyricsList.append(lyrics)
			if artistName == secondArtist:
				secondArtistLyricsList.append(lyrics)
	return [firstArtistLyricsList, secondArtistLyricsList]

def lyricsListToString(lyricsList):
	return ', '.join(lyricsList).lower() 


def getTextActivity(tokenList):
	verbCount = 0
	adjCount = 0

	posTags = nltk.pos_tag(tokenList)
	for tag in posTags:
		if 'VB' in tag[1]:
			verbCount += 1
		if 'JJ' in tag[1]:
			adjCount += 1
	q = float(verbCount) / (verbCount + adjCount)
	return round(q, 2)

def getStats(artist, lyricsList):
	stats = {
		'artist': artist,
		'song-count': len(lyricsList),
	}
	allLyrics = lyricsListToString(lyricsList)
	allLyrics = re.sub(r'[^\x00-\x7F]+',' ', allLyrics)

	lex = LexicalRichness(allLyrics)
	stats['lyric-count'] = lex.words
	stats['vocab-size'] = lex.terms 
	stats['TTR'] =  round(lex.ttr, 2)
	stats['RTTR'] = round(lex.rttr, 2)
	stats['CTTR'] = round(lex.cttr, 2)
	stats['MSTTR'] = round(lex.msttr(segment_window=25))
	stats['MATTR'] = round(lex.mattr(window_size = 25), 2)
	stats['MTLD'] = round(lex.mtld(threshold=0.72), 2)
	stats['HD-D'] = round(lex.hdd(draws=42))

	stops = stopwords.words('english')
	stops = [stop.lower().strip() for stop in stops]
	contentLyricsList = [lyric for lyric in allLyrics.split() if lyric not in stops]

	blob = TextBlob(' '.join(contentLyricsList))
        tokens = blob.words
	lyricSentiment = round(blob.sentiment.polarity, 2)
	if lyricSentiment > 0:
		lyricSentiment = ('positive ' + '(' + str(lyricSentiment) + ')') 
	elif lyricSentiment < 0:
                lyricSentiment = ('negative ' + '(' + str(lyricSentiment) + ')')
	else:
		lyricSentiment = ('neutral ' + '(' + str(lyricSentiment) + ')')
	stats['polarity'] = lyricSentiment
	
	mostUsedWord = max(blob.word_counts, key=blob.word_counts.get)
	mostUsedWordFreq = blob.word_counts[mostUsedWord]
	stats['most-used-word'] = (mostUsedWord + ' (' + str(mostUsedWordFreq) + ')')

	stats['text-activity'] = getTextActivity(tokens)

	return stats

def printArtistLyricsToCompare(artists, artistLyricsToCompare):
	for i in range(len(artists)):
		artist = artists[i]
		artistIndex = i
		artistLyricsList = artistLyricsToCompare[artistIndex]
		artistStats = getStats(artist, artistLyricsList)
		for key,value in sorted(artistStats.items()):
			print key + ':', value
		print '\n'	

def compareArtists(firstArtist, secondArtist):
        artistLyricsToCompare = getLyrics([firstArtist, secondArtist])
        firstArtistLyrics = artistLyricsToCompare[0]
        firstArtistStats = getStats(firstArtist, firstArtistLyrics)
        secondArtistLyrics = artistLyricsToCompare[1]
        secondArtistStats = getStats(secondArtist, secondArtistLyrics)
	return {firstArtist: firstArtistStats, secondArtist: secondArtistStats}

