import re
import csv
import collections
import numpy
import string
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from scipy.stats import hypergeom

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
                	if artistName.lower() == firstArtist.lower():
                        	firstArtistLyricsList.append(lyrics)
			if artistName.lower() == secondArtist.lower():
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

def getNumTypes(tokens):
	return len(set(tokens))

def getNumTokens(tokens):
	return len(tokens)

def getTTR(tokens):
	numTypes = getNumTypes(tokens)
	numTokens = getNumTokens(tokens)
	ttr = float(numTypes) / numTokens
	return round(ttr, 2)

def getRTTR(tokens):
	numTypes = getNumTypes(tokens)
	numTokens = getNumTokens(tokens)
	rttr = float(numTypes) / numpy.sqrt(numTokens)
	return round(rttr, 2)

def getCTTR(tokens):
	numTypes = getNumTypes(tokens)
	numTokens = getNumTokens(tokens)
	cttr = float(numTypes) / numpy.sqrt(2 * numTokens)
	return round(cttr, 2)

def getMATTR(tokens, window_size):
	freqs = collections.Counter()
	ttrs = []
	text_size = len(tokens)

	window_tokens = tokens[:window_size]
	for token in window_tokens:
		token_count = window_tokens.count(token) 
		freqs[token] = token_count 
	window_ttr = len(freqs) / window_size 
	ttrs.append(window_ttr)

	for window_position in range(1, text_size - window_size + 1 ):
		leaving_token = tokens[window_position - 1]
		freqs[leaving_token] -= 1
		if freqs[leaving_token] == 0:
			del freqs[leaving_token]

		entering_token = tokens[window_position + window_size - 1]
		freqs[entering_token] += 1

		window_ttr = float(len(freqs)) / window_size
		ttrs.append(window_ttr)

	mattr = numpy.mean(ttrs)
	return round(mattr, 2)

def getMSTTR(tokens, segment_window):
	freqs = collections.Counter()
	ttrs = []
	text_size = len(tokens)

	numSegments = text_size / segment_window
	numRemainingTokens = text_size % segment_window

	window_ttrs = []
	segment_index = 0
	for segment in range(numSegments):
		window_tokens = tokens[segment_index:segment_index + segment_window]			
		window_ttr = getTTR(window_tokens)
		ttrs.append(window_ttr)
		segment_index += segment_window	

	if numRemainingTokens > 0:
		remainingTokens = tokens[segment_index:]
		remainingTTR = getTTR(remainingTokens)
		ttrs.append(remainingTTR)

	msttr = numpy.mean(ttrs)
	return round(msttr, 2)

def getMTLD(tokens, threshold):
	types = set()
	numSequentialTokens = 0
	factorCount = 0

	for token in tokens:
		numSequentialTokens += 1
		types.add(token)
		ttr = len(types) / numSequentialTokens

		if ttr <= threshold:
			numSequentialTokens = 0
			types = set()
			factorCount += 1

	if numSequentialTokens > 0:
		factorCount += (1 - ttr) / (1 - threshold)

	if factorCount == 0:
		ttr = getTTR(tokens)
		if ttr == 1:
			factorCount += 1
		else:
			factorCount += (1 - ttr) / (1 - threshold)

	mtld = len(tokens) / factorCount
	return round(mtld, 2)

def getHDD(tokens, numDraws):
	freqs = collections.Counter(tokens)
	contributions = []
	numTokens = getNumTokens(tokens)
	for term, freq in freqs.items():
		contribution = (1 - hypergeom.pmf(0, numTokens, freq, numDraws)) / numDraws
		contributions.append(contribution)
	return round(sum(contributions), 2)

def getPolarity(contentLyrics):
	blob = TextBlob(contentLyrics)
	tokens = blob.words
	lyricSentiment = round(blob.sentiment.polarity, 2)
	if lyricSentiment > 0:
		lyricSentiment = ('positive ' + '(' + str(lyricSentiment) + ')')
	elif lyricSentiment < 0:
		lyricSentiment = ('negative ' + '(' + str(lyricSentiment) + ')')
	else:
		lyricSentiment = ('neutral ' + '(' + str(lyricSentiment) + ')')
	return lyricSentiment

def getMostUsedWord(contentLyricsList):
	counter = collections.Counter(contentLyricsList)
        mostUsedWord = counter.most_common(1)[0][0]
        mostUsedWordFreq = counter.most_common(1)[0][1]
	return (mostUsedWord + ' (' + str(mostUsedWordFreq) + ')')

def preprocess(text):
	text = re.sub(r'[^\x00-\x7F]+',' ', text)
	text = re.sub(r'[0-9]+', '', text.lower())
	text = text.replace('-', '')

	for p in list(string.punctuation):
		text = text.replace(p, ' ')

	return text

def tokenize(text):
	return text.split()

def removeStopwords(text):
	stops = stopwords.words('english')
	stops = [stop.lower().strip() for stop in stops]
	stops.append('oh')
	stops.append('yah')
	stops.append('uh')
	stops.append('huh')
	stops.append('yeah')
	stops.append('ooh')
	stops.append('oooh')
	stops.append('ooooh')
	stops.append('get')
	stops.append('got')
	stops.append('hol')
	stops.append('like')
	stops.append('want')
	stops.append('eh')
	stops.append('i\'m')

	tokens = tokenize(text)
	contentLyricsList = [lyric for lyric in tokens if lyric not in stops]
	contentLyrics = lyricsListToString(contentLyricsList)

	return contentLyrics

def getStats(artist, lyricsList):
	stats = {
		'artist': artist,
		'song-count': len(lyricsList),
	}

	allLyrics = lyricsListToString(lyricsList)
	allLyrics = preprocess(allLyrics)
	tokens = tokenize(allLyrics)

	assert (len(tokens) > 0), 'No lyrics were found for {}.'.format(artist)

	stats['lyric-count'] = getNumTokens(tokens)
	stats['vocab-size'] = getNumTypes(tokens)
	stats['TTR'] =  getTTR(tokens)
	stats['RTTR'] = getRTTR(tokens)
	stats['CTTR'] = getCTTR(tokens)
	stats['MSTTR'] = getMSTTR(tokens, 25)
	stats['MATTR'] = getMATTR(tokens, 25)
	stats['MTLD'] = getMTLD(tokens, 0.72)
	stats['HD-D'] = getHDD(tokens, 42)

	contentLyrics = removeStopwords(allLyrics)
	stats['polarity'] = getPolarity(contentLyrics)
	stats['most-used-word'] = getMostUsedWord(tokenize(contentLyrics))	
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
