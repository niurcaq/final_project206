# web scrape billboard top 100
from bs4 import BeautifulSoup
import requests
import sqlite3

# might need to place this function in a different file because if we call this file four times, it will restart the list every time
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

# this creates a database called music and fills a table with artists from top billboard
def artist_table(artists):
    # set up conn
    conn = sqlite3.connect('music.db')
    # set up cur
    cur = conn.cursor()
    # iterate through list until nothing is left
    for i in range(0,25):
        name = artists[i]
        # insert artist name into database
        cur.execute(
            "INSERT OR IGNORE INTO artists (name) VALUES (?)", (name, )
        )
    # commit changes
    conn.commit()
    # delete first 25 (to allow for 100 in total but at a rate of 25)
    del artists[:25]
    # close connection
    conn.close()
