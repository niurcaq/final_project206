# spotify api data collecting

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
# spotipy client
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

# this func gets the shortest genre so we avoid stuff like "modern Kentucky country rap"
def shortest_genre(genres):
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
    # return min genre
    return minG

# this func calls spotify api to get data on artists
def gather_spotify_artist_info(artists):
    # this list will include tuples of info for every artist
    l = []
    # go through the list of artists
    for artist in artists:
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

        # # check if results exist
        # if len(res['artists']['items']) != 0:
        #     # iterate the search results to find corect artist
        #     for d in res['artists']['items']:
        #         # if the name matches the artist name continue to retreive data
        #         if d['name'] == artist:
        #             # set variables to data pieces we need
        #             s_id = d['id']
        #             print(artist)
        #             genre = shortest_genre(d['genres'])
        #             pop = d['popularity']
        #             name = d['name']
        #             # set exists to  True
        #             exists = True
        #             # add the tuples of data to the list
        #             l.append((name, s_id, genre, pop))
        #             break
        #     if exists == False:
        #         # no results exist
        #         print(f'No {artist} in results')
        #         s_id = None
        #         genre = None
        #         pop = None
        #         name = artist
        #         # add tuple of data that has null data
        #         l.append((name, s_id, genre, pop))
        # # results don't exist
        # else:
        #     print(f"No results for {artist}")
        #     # set data to null
        #     s_id = None
        #     genre = None
        #     pop = None
        #     name = artist
        #     # add tuple of data that has null data
        #     l.append((name, s_id, genre, pop))


def gather_spotify_songs(artists_info):
    l = []
    for artist in artists_info:
        art = f'spotify:artist:{artist[0]}'
        res = sp.artist_top_tracks(art)
        name = res['tracks'][0]['name']
        dur = res['tracks'][0]['duration_ms']
        l.append((name, dur))
    return l

# this func populates the database
def spotify_tables(artists_info, art_table):
    # set up conn
    conn = sqlite3.connect('music.db')
    # set up cur
    cur = conn.cursor()
    if art_table:
        # iterate through list until nothing is left
        for i in range(0,25):
            s_id = artists_info[i][0]
            gen = artists_info[i][1]
            pop = artists_info[i][2]
            # insert artist info into database
            cur.execute(
                "INSERT OR IGNORE INTO spotify_artists (spotify_id, genre, popularity) VALUES (?, ?, ?)", (s_id, gen, pop)
            )
    else:
        #iterate through list until nothing is left
        for i in range(0, 25):
            name = artists_info[i][0]
            dur = artists_info[i][1]
            # insert song info into database
            cur.execute(
                "INSERT OR IGNORE INTO spotify_songs (name, length) VALUES (?, ?)", (name, dur)
            )
    # commit changes
    conn.commit()
    # delete first 25 (to allow for 100 in total but at a rate of 25)
    del artists_info[:25]
    # close connection
    conn.close()
