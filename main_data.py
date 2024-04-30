import sqlite3
from top_artists_web import artist_retrieval, artist_table
from spotify_api import gather_spotify_artist_info, gather_spotify_songs, spotify_tables
from itunes_api import gather_itunes_artist_info, gather_itunes_songs, itunes_tables

# this function drops and creates a table with table_name & certain columns
def create(table_name, columns):
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    )

# set up conn
conn = sqlite3.connect('music.db')
# set up cur
cur = conn.cursor()
# create tables
create('artists', 'artist_id INTEGER PRIMARY KEY, name TEXT UNIQUE')
create('spotify_artists', 'artist_id INTEGER PRIMARY KEY, spotify_id TEXT UNIQUE, genre TEXT, popularity INTEGER')
create('spotify_songs', 'artist_id INTEGER PRIMARY KEY, length INTEGER')
create('itunes_artists', 'artist_id INTEGER PRIMARY KEY, itunes_id INTEGER UNIQUE, genre TEXT')
create('itunes_songs', 'artist_id INTEGER PRIMARY KEY, length INTEGER')

# commit changes
conn.commit()

# artists contains 100 artists from top billboard
artists = artist_retrieval()
# get spotify artist info + song info
spotify_artists = gather_spotify_artist_info(cur, artists)
spotify_songs = gather_spotify_songs(spotify_artists)
itunes_artists = gather_itunes_artist_info(cur, artists)
itunes_songs = gather_itunes_songs(itunes_artists)

# populate the database by running this file 4 times
artist_table(cur, conn, artists)
spotify_tables(cur, conn, spotify_artists, 'spotify_artists')
spotify_tables(cur, conn, spotify_songs, 'spotify_songs')
itunes_tables(cur, conn, itunes_artists, 'itunes_artists')
itunes_tables(cur, conn, itunes_songs, 'itunes_songs')
