import re
import requests
from io import BytesIO

import dash
from dash import Dash, dcc, html, Input, Output, callback

from lyricsgenius import Genius
from PIL import Image
from textblob import TextBlob

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
import contractions
from autocorrect import Speller

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

spell = Speller(lang='en')
#genius = Genius(ACCESS_TOKEN)
genius.remove_section_headers = True
top_song_num = 10
stop_words = set(stopwords.words('english'))

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(dcc.Input(id='query_artist', type='text', placeholder="Insert Artist Name", debounce=True, minLength=1)),
        html.Button('Submit', id='submit_artist', n_clicks=0),
        html.Br(),
        html.Img(id="query_artist_lyrics"),
    ]
)

"""
Checks if Song Name that is about to be added is already in the Song List.
"""
def check_repeat(song_list, new_song_title):
    song_title = re.sub("\(.*?\)|\[.*?\]","", new_song_title).replace('\u200b', '').strip()
    if song_title in song_list:
        return False, song_title

    return True, song_title

"""
Processes Song Lyrics
-- removes stop words
-- removes punctuation
"""
def process_lyrics(lyrics):
    lyrics_lines = lyrics.split("Lyrics", 1)[1].strip()
    if len(lyrics_lines) < 1:
        lyrics_lines = lyrics

    lyrics_lines = re.sub(r'[^\w\d\s\'\-]+', '', lyrics_lines)
    lyric_tokens = lyrics_lines.split()

    filtered_lyrics = []
    for w in lyric_tokens:
        new_w = (contractions.fix(w)).lower()

        # if there are #s in the word, consider it neutral and skip
        if bool(re.search(r'\d', new_w)):
            continue

        # if there is an apostrophe in the word
        if "'" in new_w:
            new_w = new_w.replace("in'", "ing")
            new_w = new_w.replace("'bout", "about")
            new_w = new_w.replace("'til", "until")
            new_w = new_w.replace("'cause", "because")
            new_w = new_w.replace("'s", "")
        else:
            new_w = spell(new_w)

        # if word is a stop_word, skip
        if new_w in stop_words:
            continue

        filtered_lyrics.append(new_w)

    return filtered_lyrics

"""
Generates Word Cloud
"""
def word_cloud(lyrics):
    token_lyrics = word_tokenize(lyrics)
    pos_lyrics = nltk.pos_tag(token_lyrics)

    lyrics_out = ' '.join([word for (word, pos) in pos_lyrics if pos == 'NN'])

    with open('top100common.txt') as f:
        common_words = f.read().split()

    stopwords = set(STOPWORDS).union(set(common_words))

    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    collocations=False,
                    min_font_size = 10).generate(lyrics_out)

    # plot the WordCloud image  
    plt.switch_backend('Agg')                     
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)

    plt.savefig('word_cloud.png')

    im  = Image.open('word_cloud.png')
    return im

@callback(
    Output("query_artist_lyrics", "src"),
    Input("query_artist", "value"),
    Input("submit_artist", "n_clicks"),
)
def get_lyrics(query_artist, n_clicks):
    if n_clicks == 0:
        return None

    n_clicks = 0

    test_count = 0
    while True:
        try:
            artist = genius.search_artist(query_artist, max_songs=20, sort='popularity') #max_songs set for testing efficiency
            break
        except requests.exceptions.Timeout:
            print ("genius execution failed, trying again")
            test_count += 1

            if test_count > 5:
                print ("genius execution failed, please rerun program")
                sys.out(1)

    song_list = artist.songs

    song_titles = []
    song_lyrics = []
    for song in song_list:
        is_new, song_title = check_repeat(song_titles, song.title)
        if is_new:
            song_titles.append(song_title)

            lyrics = process_lyrics(song.lyrics)
            song_lyrics.append(lyrics)

            if len(song_lyrics) >= 10:
                break

    all_songs = [' '.join(lyric) for lyric in song_lyrics]
    all_lyrics = ' '.join(all_songs)

    print(all_lyrics)

    im = word_cloud(all_lyrics)

    for song in all_songs:
        blob = TextBlob(song)
        print(blob.tags)
        print(blob.noun_phrases)
        print(blob.sentiment)

    return im

if __name__ == '__main__':
    app.run_server(debug=True)
