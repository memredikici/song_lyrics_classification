# Text Classification on Song Lyrics
Text classification model on song lyrics from [lyrics.com](lyrics.com)

## Table of Contents
- [General info](#general-info)
- [Technologies and Libraries](#technologies-and-libraries)
- [Setup](#setup)
- [Status](#status)

### General info

In this Project, I've built text classification model on song lyrics from [lyrics.com] for two singers and tried to learn methods:
- Web Scraping
- Regular Expressions
- Parsing HTML
- Bag of Words

### Technologies and Libraries

- Python 3.8
- requests
- re
- BeautifulSoup
- pandas
- Scikit Learn
    - CountVectorizer
    - TfidfVectorizer
    - make_pipeline
    - GridSearchCV
    - LogisticRegression
- seaborn
- matplotlib

### Setup
Using **Anaconda** is advised for quick lunch. it consists of all required libraries.  
To make this project user friendly, I've combined each methods in [execution.py](https://github.com/memredikici/song_lyrics_classification/blob/master/execution.py).
1. Firstly for running the program, you need to `cd` into the folder that contains the files.
2. Type on terminal `python execution.py <first Artist> <second Artist> ` 
    - You can use `python execution.py beyonce coldplay` to make a prediction through trained model.
- and follow the instructions...

- Enjoy :) 