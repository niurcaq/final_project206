# itunes api data collecting

import requests

def gather_itunes_artist_info(artists):
    # list will hold data
    l = []
    # iterate artist names
    for artist in artists:
        # search for artist name
        url = f"https://itunes.apple.com/search?term={artist}&entity=musicArtist&limit=1"
        res = requests.get(url)
        # if the request goes through gather the data
        if res.ok:
            data = res.json()
            # get the itunes id & genre
            it_id = data['results'][0]['artistId']
            gen = data['results'][0]['primaryGenreName']
            l.append((it_id, gen))
        else:
            # if response is error then print error and gather null data
            print(f"res:{res} for {artist}")
            l.append((None, None))
    # return the list
    return l


def gather_itunes_songs(artists_info):
    # empty list
    l = []
    # iterate artist info
    for artist in artists_info:
        # look for artist id
        url = f"https://itunes.apple.com/lookup?id={artist[0]}&entity=song"
        res = requests.get(url)
        data = res.json()
        # go thru results
        for d in data['results']:
            # if the result type is a song and its artist is the same
            if d['wrapperType'] == 'track' and d['artistId'] == artist[0]:
                # set name and duration of song
                name = d['trackName']
                dur = d['trackTimeMillis']
                # add it to the list
                l.append((name, dur))
                # exit because we are only getting the first song
                break
    # return the list of songs and their duration
    return l


def itunes_tables(cur, conn, artists_info, art_table):
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
