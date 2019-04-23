import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pandas as pd
from collections import defaultdict

data = pd.read_csv('./data.csv', usecols=['genre', 'lyrics', 'release_date'])

print data

# song_dict[genre][year] will return all lyrics for that genre in that year
song_dict = defaultdict(lambda: defaultdict(str))

for _, row in data.iterrows():
	year = row['release_date'].split('-')[0]
	song_dict[row['genre']][year] += "\t"+row['lyrics'].decode().encode('utf-8')

print song_dict