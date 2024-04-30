# visuals will be created here

import matplotlib as plt

# def read_spotify_percentages():
genres = []
percentages = []
with open("percentage_of_genres_spotify.txt", 'r', encoding='utf-8-sig') as f:
    # get rid of headers
    f.readline()
    # lines contains all lines of code
    lines = f.readlines()
    for line in lines:
        genres.append(line.split(',')[0])
        percentages.append(line.split(',')[1])

plt.pie(percentages, labels=genres)