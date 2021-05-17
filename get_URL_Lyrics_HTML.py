import requests
import re
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def make_url(subject):
    '''
    - takes subject and returns wiki url for that subject. \n
    - that subject must be extracted from the link. \n
    - e.g. : "https://www.lyrics.com/artist/Beyonc%C3%A9/349078" -> "Beyonc%C3%A9/349078" must be written as parameter. \n
    '''
    return f'https://www.lyrics.com/artist/{subject}'


def get_content(url, headers):
    '''
    - gets url's content
    '''
    response = requests.get(url, headers=headers)
    return response.text


def get_main_content(response, artist_name):
    '''
    - downloads main page of artist. \n
    - it creates automatically 'data' folder where all HTML will be downloaded. \n
    - 'artist_name' parameter allows you to create a folder where the content will be downloaded. \n
    - it will stop if those folders already exist.
    '''
    path = "/data"
    try:
        os.mkdir(path)
        os.mkdir(f'./data/{artist_name}')
    except OSError:
        print("Creation of the directory failed / it might already exists")
        return

    with open(f'./data/{artist_name}/{artist_name}.html', mode='w') as file:
        file.write(response)


def artist_page(artist):
    '''
    - finds the main page for searched Artist
    '''
    input_url = make_url(artist)
    input_page = get_content(input_url, headers)
    exctraction = re.findall('"artist\/(.+?)"', input_page)
    # print(exctraction)
    print("Is this artist the right one which you are searching?:",
          exctraction[0])
    reply = input('please enter "y" or "n":')
    if reply == 'y':
        url = url_generator(exctraction, 'a')
    else:
        artist_page()
    return url[0]


def find_songs_url(response):
    '''
    - finds all texts that includes url part in main content page for every songs of artist \n
    - returns into a list of HTML \n
    '''
    exctraction = re.findall('"\/lyric\/(.+?)"', response)
    return list(exctraction)


def url_generator(songs_list, selector):
    '''
    - takes the list of songs' urls as input \n
    - produces a list of URLs that help get their content \n
    - it takes selector 'l' for lyrics. 'a' for artist
    '''
    url = []
    for i in range(len(songs_list)):
        if selector == 'l':
            temp = 'https://www.lyrics.com/lyric/' + str(songs_list[i])
        elif selector == 'a':
            temp = 'https://www.lyrics.com/artist/' + str(songs_list[i])
        url.append(temp)
    return url


def download_song(lyrics_urls, artist_name):
    '''
    - downloads HTML files for every songs of artist. \n
    - it will stop if the songs' folder are already exist.
    '''
    path = f'/data/{artist_name}/lyrics'
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory failed / it might already exists")
        return
    a = 0
    for i in range(len(lyrics_urls)):
        # time.sleep(0.01)
        a = a + 1
        print(a, 'song is downloading')
        page = get_content(lyrics_urls[i], headers)
        with open(f'./data/{artist_name}/lyrics/{i}.html', mode='w') as file:
            file.write(page)
