# calculations will be done here 

def avg_time_per_genre_spotify(cur):
    # this func joins the two spotify tables to find the avg length in min of each genre
    cur.execute(
        "SELECT A.genre, AVG(S.length) FROM spotify_songs AS S JOIN spotify_artists AS A WHERE S.artist_id=A.artist_id GROUP BY A.genre ORDER BY AVG(S.length) DESC"
    )
    rows = cur.fetchall()
    # we write to a text file with headers specified 
    with open('spotify_data.txt', 'w', encoding='utf-8-sig') as f:
        f.write("Genre,Avg Length of Songs(min)\n")
        for r in rows:
            f.write(f'{r[0]},{round(r[1]/60000,2)}\n')

def avg_time_per_genre_itunes(cur):
    # this func joins the two itunes tables to find the avg length in min of each genre
    cur.execute(
        "SELECT A.genre, AVG(S.length) FROM itunes_songs AS S JOIN itunes_artists AS A WHERE S.artist_id=A.artist_id GROUP BY A.genre ORDER BY AVG(S.length) DESC"
    )
    rows = cur.fetchall()
    # we write the data to a text file w/ headers
    with open('itunes_data.txt', 'w', encoding='utf-8-sig') as f:
        f.write("Genre,Avg Length of Songs(min)\n")
        for r in rows:
            f.write(f'{r[0]},{round(r[1]/60000,2)}\n')

def genre_percentages_spotify(cur):
    # percentage in each genre for spotify
    cur.execute(
        "SELECT A.genre, COUNT(*) FROM spotify_artists AS A GROUP BY A.genre ORDER BY COUNT(*) DESC"
    )
    rows = cur.fetchall()
    # write data into text file
    with open("percentage_of_genres_spotify.txt", "w", encoding='utf-8-sig') as f:
        f.write("Genre,Percentage\n")
        for r in rows:
            f.write(f"{r[0]},{r[1]}\n")

def genre_percentages_itunes(cur):
    # percentage of each genre for itunes
    cur.execute(
        "SELECT A.genre, COUNT(*) FROM itunes_artists AS A GROUP BY A.genre ORDER BY COUNT(*) DESC"
    )
    rows = cur.fetchall()
    # write data into text file
    with open("percentage_of_genres_itunes.txt", "w", encoding='utf-8-sig') as f:
        f.write("Genre,Percentage\n")
        for r in rows:
            f.write(f"{r[0]},{r[1]}\n")