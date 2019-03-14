from bs4 import BeautifulSoup
import urllib2
import requests
import csv
import re
import os.path

##########
# PART 1 - Fetch the list of songs to retrieve from Genius API using 13 years of year-end Billboard 100 charts
##########
def fetch_song_list(urls):
    print "Retrieving songs to query..."
    hdr = {'User-Agent': 'Mozilla/5.0'}

    song_list = []

    for url in urls:
        req = urllib2.Request(url, headers=hdr)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page, features="html.parser")
        song_divs = soup.findAll("div", {"class": "ye-chart-item__text"})

        rank = 1
        for div in song_divs:
            title = div.findAll("div", {"class": "ye-chart-item__title"})[0]
            artist = div.findAll("div", {"class": "ye-chart-item__artist"})[0]
            song_list.append(
                {"title": title.text.strip().encode("utf-8"),
                 "artist": artist.text.strip().split(' Featuring')[0].encode("utf-8"),
                 "rank": rank})
            rank += 1

    print "Successfully retrieved %d songs." % len(song_list)
    return song_list

##########
# PART 2 - Retrieve song data from Geinus API
##########
def fetch_song_data(song_list):
    print "Retrieving song data..."
    headers = {"Authorization": "Bearer mHBOtD-hkvT5zUqQm41cgHUbYsMaBM6PqPCT33SS10uz7ocXC4QA922oG1z1mE_B"}

    songs = []
    song_genres = []

    for s in song_list:
        # search for song
        query = s['title']+" "+s['artist']
        search_query = urllib2.quote(query)
        try:
            search_url = "http://api.genius.com/search?q=" + search_query
            r = requests.get(search_url, headers=headers)
            song_id = r.json()['response']['hits'][0]['result']['id']
        except:
            print 'could not find result for %s.' % query
            continue

        # retrieve song data
        try:
            song_url = "http://api.genius.com/songs/" + str(song_id)
            r2 = requests.get(song_url, headers=headers)
            r2json = r2.json()['response']['song']
            song = {}
            song['song_name'] = r2json['title'].encode("utf-8")
            song['song_id'] = r2json['id']
            song['artist_name'] = r2json['primary_artist']['name'].encode("utf-8")
            song['artist_id'] = r2json['primary_artist']['id']
            song['release_date'] = r2json['release_date'].encode("utf-8")
            song['url'] = r2json['url'].encode("utf-8")
        except:
            print 'could not fetch song data for %s.' % query
            continue

        # retrieve song lyrics
        try:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib2.Request(song['url'], headers=hdr)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page, features="html.parser")

            lyrics = soup.find('div', {"class": "lyrics"}).get_text()
            song['lyrics'] = re.sub("\[[^\]]*\]", " ",
                                    lyrics.strip().replace('\n', ' ').replace(',', ' ').encode("utf-8"))

            tags = soup.findAll('img', {"height": "0"})
            genres = urllib2.unquote(tags[0]['src']
                                     .split('page-genres=')[1]
                                     .split('&')[0]
                                     .replace('+Genius', '')
                                     .replace('+', ' ')
                                     .encode("utf-8")).split(',')
            for genre in genres:
                song_genres.append([song['song_id'], genre])
        except:
            print 'could not fetch song lyrics for %s.' % query
            continue

        song['billboard_rank'] = s['rank']
        songs.append(song)
        print 'Saved %s successfully.' % query

    print 'Fetched data for %d songs.' % len(songs)
    return songs, song_genres

##########
# PART 3 - Write song data to CSV
##########
def write_to_csv(songs, song_genres, overwrite):
    print "Writing to csv..."
    csv_name = "songs.csv"
    csv_name2 = "song_genres.csv"
    if os.path.isfile(csv_name) and not overwrite:
        keys = songs[0].keys()
        with open(csv_name, 'a') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writerows(songs)
        with open(csv_name2, 'a') as output_file2:
            writer = csv.writer(output_file2)
            writer.writerows([["song_id", "genre"]])
            writer.writerows(song_genres)
    else:
        keys = songs[0].keys()
        with open(csv_name, 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(songs)
        with open(csv_name2, 'wb') as output_file2:
            writer = csv.writer(output_file2)
            writer.writerows([["song_id", "genre"]])
            writer.writerows(song_genres)
    print "Wrote to csv successfully."



if __name__ == "__main__":
    urls = ["https://www.billboard.com/charts/year-end/2006/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2007/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2008/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2009/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2010/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2011/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2012/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2013/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2014/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2015/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2016/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2017/hot-100-songs",
            "https://www.billboard.com/charts/year-end/2018/hot-100-songs"]

    song_list = fetch_song_list(urls)

    songs, song_genres = fetch_song_data(song_list)

    write_to_csv(songs, song_genres, True)