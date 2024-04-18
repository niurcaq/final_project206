# spotify api data collecting

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# auth_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(auth_manager=auth_manager)

# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# web scrape billboard top 100

from bs4 import BeautifulSoup
import requests
import sqlite3
import json
import re
import os
import csv
import unittest

def artist_retrieval():
    # set file to billboard top 100 artists
    html_url = "https://www.billboard.com/charts/artist-100/"
    # set request
    res = requests.get(html_url, verify=False)
    # set soup object
    soup = BeautifulSoup(res.text, 'html.parser')
    # find all h3 tags with this class
    artists = soup.find_all('h3', class_="a-no-trucate")
    #  list to be returned
    artist_list = []
    # for every artist
    for a in artists:
        # add it to the list
        artist_list.append(a.text.strip())
    # return the list of artists
    return artist_list


def artist_db(artists):
    # set up conn
    conn = sqlite3.connect('artists.db')
    # set up cur
    cur = conn.cursor()
    # create table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS artists (artist_id INTEGER PRIMARY KEY, artist_name TEXT UNIQUE)"
    )
    # commit changes
    conn.commit()
    # iterate through list until nothing is left
    for i in range(0,25):
        name = artists[i]
        # insert artist name into database
        cur.execute(
            "INSERT OR IGNORE INTO artists (artist_name) VALUES (?)", (name, )
        )
    # commit changes
    conn.commit()
    # delete first 25 (to allow for 100 in total but at a rate of 25)
    del artists[:25]
    # close connection
    conn.close()
    l = artists
    return l


# artists = artist_retrieval()
# artist_db(artists)
# artist_db(artists)
# artist_db(artists)
# artist_db(artists)