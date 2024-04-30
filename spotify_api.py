# spotify api data collecting

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# spotipy client
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

# this func gets the shortest genre so we avoid stuff like "modern Kentucky country rap"
def shortest_genre(genres):
    l = ['country', 'r&b', 'pop', 'indie', 'rock', 'rap']
    # if no genres exist for the artist set genre to null by returning none
    if len(genres) == 0:
        return None
    # set first genre as min
    minG = genres[0]
    # iterate genres
    for genre in genres:
        # if current genre is less than current min, set min to current genre
        if len(genre) < len(minG):
            minG = genre
    # get the words to split
    for w in minG.split(' '):
        # if the first word is in the list then set it as the genre
        if w in l:
            minG = w
            break

    return minG


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


# this func calls spotify api to get data on artists
def gather_spotify_artist_info(cur, artists):
    # this list will include tuples of info for every artist
    l = []

    # r represents range we will be traversing
    r = check_database_entries(cur, 'spotify_artists')
    # if the range is not None (not 100 data entries in database)
    if r != None:
        # iterate the range
        for i in range(r[0], r[1]):
            artist = artists[i]
            # res contains search results for the artist's name
            res = sp.search(q='artist:' + artist, type="artist", limit=1)
            # check if results exist
            if len(res['artists']['items']) != 0:
                # get first result 
                art = res['artists']['items'][0]
                # set variables to data pieces we need
                s_id = art['id']
                genre = shortest_genre(art['genres'])
                pop = art['popularity']
                # add the tuples of data to the list
                l.append((s_id, genre, pop))

            else:
                # results did not show up for this search
                # set data to null
                s_id = None
                genre = None
                pop = None
                # add tuple of data that has null data
                l.append((s_id, genre, pop))
    # return the tuples of data
    return l


# this func returns songs info
def gather_spotify_songs(artists_info):
    # list will hold tuples of songs
    l = []
    # iterate artist tuple info
    for artist in artists_info:
        # get artist spotify_id
        art = f'spotify:artist:{artist[0]}'
        # find top_tracks
        res = sp.artist_top_tracks(art)
        dur = res['tracks'][0]['duration_ms']
        # add top song duration to list
        l.append(dur)
    # return list of tuples
    return l


# this func populates the database
def spotify_tables(cur, conn, artists_info, table):
    # we are populating artists here
    if table == 'spotify_artists':
        # set tuple data to vars
        for artist in artists_info:
            s_id = artist[0]
            gen = artist[1]
            pop = artist[2]
            # insert artist info into database
            cur.execute(
                f"INSERT OR IGNORE INTO {table} (spotify_id, genre, popularity) VALUES (?, ?, ?)", (s_id, gen, pop)
            )
    # we are populating songs here
    else:
        # iterate duration of songs
        for dur in artists_info:
            # insert song len into database
            cur.execute(
                f"INSERT OR IGNORE INTO {table} (length) VALUES (?)", (dur, )
            )

    # commit changes
    conn.commit()
