# itunes api data collecting

import requests

# this func returns the range of items we will be traversing
def check_database_entries(cur, table):
    # find total data entries in database for the table
    cur.execute(
        f"SELECT COUNT(*) FROM {table}"
    )
    count = cur.fetchone()[0]
    # return the range 
    if count == 0:
        return (0,25)
    elif count == 25:
        return (25,50)
    elif count == 50:
        return (50,75)
    elif count == 75:
        return (75,100)
    else:
        # already 100 items in database
        return None


# this func returns data on the artist
def gather_itunes_artist_info(cur, artists):
    # list will hold data
    l = []
    # check the range of the database
    r = check_database_entries(cur, 'itunes_artists')
    # if not none(not 100 values in database)
    if r != None:
        # iterate the range
        for i in range(r[0], r[1]):
            artist = artists[i]
            # search for artist name
            url = f"https://itunes.apple.com/search?term={artist}&entity=musicArtist&limit=1"
            res = requests.get(url)
            data = res.json()
            # get the itunes id & genre
            it_id = data['results'][0]['artistId']
            gen = data['results'][0]['primaryGenreName']
            # add to list
            l.append((it_id, gen))
    # return the list
    return l


# this func returns song info
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
                # set duration of song
                dur = d['trackTimeMillis']
                # add it to the list
                l.append(dur)
                # exit because we are only getting the first song
                break
    # return the list of songs durations
    return l


# this func populates the database
def itunes_tables(cur, conn, artists_info, table):
    # populating the artists table
    if table == 'itunes_artists':
        # iterate through list until nothing is left
        for artist in artists_info:
            it_id = artist[0]
            gen = artist[1]
            # insert artist name into database
            cur.execute(
                "INSERT OR IGNORE INTO itunes_artists (itunes_id, genre) VALUES (?, ?)", (it_id, gen)
            )
    # populating the songs table
    else:
        for dur in artists_info:
            # insert dur into database
            cur.execute(
                "INSERT OR IGNORE INTO itunes_songs (length) VALUES (?)", (dur, )
            )
    # commit changes
    conn.commit()
