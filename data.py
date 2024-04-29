import sqlite3
from top_artists_web import artist_retrieval, artist_table
from spotify_api import gather_spotify_artist_info, gather_spotify_songs, spotify_tables
from itunes_api import gather_itunes_artist_info, gather_itunes_songs, itunes_tables

def drop_and_create(table_name, columns):
    cur.execute(
        f"DROP TABLE IF EXISTS {table_name}"
    )
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    )

# set up conn
conn = sqlite3.connect('music.db')
# set up cur
cur = conn.cursor()
# drop any previous tables + create new ones
drop_and_create('artists', 'artist_id INTEGER PRIMARY KEY, name TEXT UNIQUE')
drop_and_create('spotify_artists', 'artist_id INTEGER PRIMARY KEY, spotify_id TEXT UNIQUE, genre TEXT, popularity INTEGER')
drop_and_create('spotify_songs', 'artist_id INTEGER PRIMARY KEY, name TEXT, length INTEGER')
drop_and_create('itunes_artists', 'artist_id INTEGER PRIMARY KEY, itunes_id INTEGER, genre TEXT')
drop_and_create('itunes_songs', 'artist_id INTEGER PRIMARY KEY, name TEXT, length INTEGER')

# commit changes
conn.commit()

# artists contains 100 artists from top billboard
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

