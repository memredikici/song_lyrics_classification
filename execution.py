import pandas as pd
import re
import sys
import argparse
import pickle

from bs4 import BeautifulSoup
from requests.api import get

from get_URL_Lyrics_HTML import *
from parsing_HTML_creating_csv import *
from ml_bag_of_words import *

first_artist = sys.argv[1]
second_artist = sys.argv[2]

if (first_artist == 'beyonce') & (second_artist == 'coldplay'):
    check = input(
        'Do you want to use already trained model to make a prediction? "y/n":')
    if check == 'y':
        with open('model.pickle', 'rb') as file:
            model = pickle.load(file)
        make_a_prediction(model)

first_artist_page = artist_page(first_artist)
second_artist_page = artist_page(second_artist)

print(first_artist_page)
print(second_artist_page)

get_main_content(get_content(first_artist_page, headers), first_artist)
get_main_content(get_content(second_artist_page, headers), second_artist)

f_artist_songs = find_songs_url(get_content(first_artist_page, headers))
s_artist_songs = find_songs_url(get_content(second_artist_page, headers))

first_lyrics_url = url_generator(f_artist_songs, 'l')
second_lyrics_url = url_generator(s_artist_songs, 'l')

download_song(first_lyrics_url, first_artist)
download_song(second_lyrics_url, second_artist)

first_lyrics_text = lyrics_extracting(first_artist)
second_lyric_texts = lyrics_extracting(second_artist)

create_save_dataframe(first_lyrics_text, first_artist)
create_save_dataframe(second_lyric_texts, second_artist)

print('-+-' * 15)
print('-'*15 + 'MACHINE LEARNING' + '-'*15)

df_first = read_csv(first_artist)
df_second = read_csv(second_artist)

drop_duplicates(df_first)
drop_duplicates(df_second)

lyrics_dataframe = make_one_dataframe(df_first, df_second)

X, y = select_input_output(lyrics_dataframe)
print(X)

model = pipeline()
print(model)
#ngram_range, max_df, min_df, max_iter = input('Enter parameters')
param_grid = get_GridSearch_hyperparameters()

grid_cv = grid_initialise_and_fit(model, param_grid, '1', X, y)

best_model = get_train_test_score(grid_cv)

make_a_prediction(best_model)
