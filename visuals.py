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

def read_spotify_data():
    genres = []
    lengths = []

    with open("spotify_data.txt", 'r', encoding='utf-8-sig') as f:
        # get rid of headers
        f.readline()
        # lines contains all lines of code
        lines = f.readlines()
        for line in lines:
            genres.append(line.split(',')[0])
            lengths.append(line.split(',')[1])

    colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf','#ff9896','#aec7e8','#ffbb78','#98df8a','#ff9896','#c5b0d5','#c49c94']
    
    plt.figure(figsize=(20, 10))
    plt.barh(genres, lengths, color=colors)

    plt.xlabel("Average Length of Top Song (min)")
    plt.ylabel("Genres")
    plt.title("Average Length of Genre's Top Song of Top 100 Artists on Spotify")
    plt.show()


def read_itunes_data():
    genres = []
    lengths = []

    with open("itunes_data.txt", 'r', encoding='utf-8-sig') as f:
        # get rid of headers
        f.readline()
        # lines contains all lines of code
        lines = f.readlines()
        for line in lines:
            genres.append(line.split(',')[0])
            lengths.append(line.split(',')[1])
    
    colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf','#ff9896','#aec7e8','#ffbb78','#98df8a','#ff9896','#c5b0d5','#c49c94']

    plt.figure(figsize=(20, 10))
    plt.barh(genres, lengths, color=colors)

    plt.xlabel("Average Length of Top Song (min)")
    plt.ylabel("Genres")
    plt.title("Average Length of Genre's Top Song of Top 100 Artists on iTunes")
    plt.show()