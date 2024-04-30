from calculations import avg_time_per_genre_itunes, avg_time_per_genre_spotify, genre_percentages_itunes, genre_percentages_spotify, spotify_popularity
from visuals import read_spotify_data, read_itunes_data, read_itunes_percentages, read_spotify_percentages, read_spotify_pop
import sqlite3

# set up conn
conn = sqlite3.connect('music.db')
# set up cur
cur = conn.cursor()

# do calculations & print to a file
avg_time_per_genre_spotify(cur)
avg_time_per_genre_itunes(cur)
genre_percentages_spotify(cur)
genre_percentages_itunes(cur)
spotify_popularity(cur)

#close conn
conn.close()

# create visuals
read_spotify_data()
read_itunes_data()
read_itunes_percentages()
read_spotify_percentages()
read_spotify_pop()