import requests
import re
import time
import os
import pandas as pd
from bs4 import BeautifulSoup


def lyrics_extracting(artist_name):
    '''
    - as parameter it takes the folder name which includes HTML files of songs.\n
    - get HTML files for each song.\n
    - extracts lyrics and saves into a list.\n
    - returns if lyrics are already extracted. 
    '''
    lyrics_text = []
    i = 0
    for fn in os.listdir(f'./data/{artist_name}/lyrics/'):

        try:
            html_file = open(f'./data/{artist_name}/lyrics/{fn}').read()
        except OSError:
            print("Lyrics directory not created or folder of this artist doesn't exist")
            return
        soup = BeautifulSoup(html_file, 'html.parser')
        print(f'number {i} lyric is extracting!')
        i = i + 1
        try:
            text = soup.find('pre').get_text().replace("\n", " ").strip()
        except AttributeError:
            continue
        lyrics_text.append(text)
    return lyrics_text


def create_save_dataframe(list_of_lyrics, artist_name):
    '''
    - takes the list which includes the lyrics and name of the artist.\n
    - creates csv file.
    '''
    lyrics_artist = pd.DataFrame({
        'artist': f"{artist_name}",
        'lyrics': list_of_lyrics
    })
    try:
        os.mkdir(f'./data/dataframes')
    except OSError:
        print("Creation of the dataframes directory failed")

    lyrics_artist.to_csv(
        f'./data/dataframes/{artist_name}_lyrics.csv', index=False)
