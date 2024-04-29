import sqlite3
from top_artists_web import artist_retrieval, artist_table
from spotify_api import gather_spotify_artist_info, gather_spotify_songs, spotify_tables
from itunes_api import gather_itunes_artist_info, gather_itunes_songs, itunes_tables
# from spotify_api import func

# set up conn
conn = sqlite3.connect('music.db')
# set up cur
cur = conn.cursor()
# drop any previous tables
cur.execute(
    "DROP TABLE IF EXISTS artists"
)
# create artists table
cur.execute(
    "CREATE TABLE IF NOT EXISTS artists (artist_id INTEGER PRIMARY KEY, name TEXT UNIQUE)"
)
# drop any previous tables
cur.execute(
    "DROP TABLE IF EXISTS spotify_artists"
)
# create spotify table
cur.execute(
    "CREATE TABLE IF NOT EXISTS spotify_artists (artist_id INTEGER PRIMARY KEY, spotify_id TEXT UNIQUE, genre TEXT, popularity INTEGER)"
)
# drop any previous tables
cur.execute(
    "DROP TABLE IF EXISTS spotify_songs"
)
# create spotify table
cur.execute(
    "CREATE TABLE IF NOT EXISTS spotify_songs (artist_id INTEGER PRIMARY KEY, name TEXT, length INTEGER)"
)
# drop any previous tables
cur.execute(
    "DROP TABLE IF EXISTS itunes_artists"
)
# create spotify table
cur.execute(
    "CREATE TABLE IF NOT EXISTS itunes_artists (artist_id INTEGER PRIMARY KEY, itunes_id INTEGER, genre TEXT)"
)
# drop any previous tables
cur.execute(
    "DROP TABLE IF EXISTS itunes_songs"
)
# create spotify table
cur.execute(
    "CREATE TABLE IF NOT EXISTS itunes_songs (artist_id INTEGER PRIMARY KEY, name TEXT, length INTEGER)"
)
# commit changes
conn.commit()

# artists, artists2, artists3 contains 100 artists from top billboard
artists = artist_retrieval()

# gather data from apis
spotify_artists = gather_spotify_artist_info(artists)
spotify_songs = gather_spotify_songs(spotify_artists)
itunes_artists = gather_itunes_artist_info(artists)
itunes_songs = gather_itunes_songs(itunes_artists)

# populate artists tables by calling the three functions 4 times
for i in range(0,4):
    artist_table(artists)
    spotify_tables(spotify_artists, True)
    spotify_tables(spotify_songs, False)
    itunes_tables(itunes_artists, True)
    itunes_tables(itunes_songs, False)


# get tuples of data from api and save as a list
# spotify_info = gather_spotify_artist_info(artists)

# populate spotify_artists table by calling this func 4 times
# for i in range(0,4):
#     spotify_artists_table(spotify_info)

# itunes_info = gather_itunes_artist_info(artists)
