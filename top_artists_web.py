# web scrape billboard top 100
from bs4 import BeautifulSoup
import requests

# might need to place this function in a different file because if we call this file four times, it will restart the list every time
def artist_retrieval():
    # set file to billboard top 100 artists
    html_url = "https://www.billboard.com/charts/artist-100/2024-04-27/"
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
def artist_table(cur, conn, artists):
    cur.execute(
        "SELECT COUNT(*) FROM artists"
    )
    count = cur.fetchone()
    if count[0] == 0:
        # get 0 to 25
        for i in range(0,25):
            name = artists[i]
            # insert artist name into database
            cur.execute(
                "INSERT OR IGNORE INTO artists (name) VALUES (?)", (name, )
            )
    elif count[0] == 25:
        # get 25 to 50
        for i in range(25,50):
            name = artists[i]
            # insert artist name into database
            cur.execute(
                "INSERT OR IGNORE INTO artists (name) VALUES (?)", (name, )
            )
    elif count[0] == 50:
        for i in range(50,75):
            name = artists[i]
            # insert artist name into database
            cur.execute(
                "INSERT OR IGNORE INTO artists (name) VALUES (?)", (name, )
            )
    else:
        for i in range(75,100):
            name = artists[i]
            # insert artist name into database
            cur.execute(
                "INSERT OR IGNORE INTO artists (name) VALUES (?)", (name, )
            )

    # commit changes
    conn.commit()
