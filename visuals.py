# visuals will be created here

import matplotlib as plt

def read_spotify_percentages():
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

    plt.figure(figsize=(20, 10))
    plt.pie(percentages, labels=genres, autopct='%1.f%%', startangle=165)
    plt.axis('equal')
    plt.title('Percentages of Genres on Spotify of Top 100 Artists on Billboard')
    plt.show()

def read_itunes_percentages():
    genres = []
    percentages = []

    with open("percentage_of_genres_itunes.txt", 'r', encoding='utf-8-sig') as f:
        # get rid of headers
        f.readline()
        # lines contains all lines of code
        lines = f.readlines()
        for line in lines:
            genres.append(line.split(',')[0])
            percentages.append(line.split(',')[1])

    plt.figure(figsize=(20, 10))
    plt.pie(percentages, labels=genres, autopct='%1.f%%', startangle=195)
    plt.axis('equal')
    plt.title('Percentages of Genres on iTunes of Top 100 Artists on Billboard')
    plt.show()

