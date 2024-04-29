# itunes api data collecting

import requests
import sqlite3

def gather_itunes_artist_info(artists):
    l = []
    for artist in artists:
        url = f"https://itunes.apple.com/search?term={artist}&entity=musicArtist&limit=1"
        res = requests.get(url)
        if res.ok:
            data = res.json()
            it_id = data['results'][0]['artistId']
            gen = data['results'][0]['primaryGenreName']
            l.append((it_id, gen))
            print("was appended successfully")
        else:
            print(f"res:{res} for {artist}")
            l.append((None, None))
    return l

# gather_itunes_artist_info(['Stray Kids', 'Beyonce'])

def gather_itunes_songs(artists_info):
    for artist in artists_info:
        url = f"https://itunes.apple.com/search?term={artist[0]}&entity=song"
        res = requests.get(url)
        data = res.json()
        print(data['results'][0])

# gather_itunes_songs([()])

def itunes_tables(artists_info, art_table):
    # set up conn
    conn = sqlite3.connect('music.db')
    # set up cur
    cur = conn.cursor()
    if art_table:
        # iterate through list until nothing is left
        for i in range(0,25):
            it_id = artists_info[i][0]
            gen = artists_info[i][1]
            # insert artist name into database
            cur.execute(
                "INSERT OR IGNORE INTO itunes_artists (itunes_id, genre) VALUES (?, ?)", (it_id, gen)
            )
    else:
        for i in range(0, 25):
            name = artists_info[i][0]
            dur = artists_info[i][1]
            # insert song info into database
            cur.execute(
                "INSERT OR IGNORE INTO itunes_songs (name, length) VALUES (?, ?)", (name, dur)
            )
    # commit changes
    conn.commit()
    # delete first 25 (to allow for 100 in total but at a rate of 25)
    del artists_info[:25]
    # close connection
    conn.close()
