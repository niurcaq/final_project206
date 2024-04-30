# calculations will be done here 


# # set up conn
# conn = sqlite3.connect('music.db')
# # set up cur
# cur = conn.cursor()

def avg_time_per_genre_spotify(cur):
    cur.execute(
        "SELECT length FROM spotify_songs JOIN "
    )