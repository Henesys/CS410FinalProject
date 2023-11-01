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
import numpy as np

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

"""
Generates Song Subjectivity Distribution
"""
def get_song_subjectivity(subjectivities):
    values, counts = np.unique(subjectivities, return_counts=True)
    # Draw dot plot with appropriate figure size, marker size and y-axis limits
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['#00BFFF', '#3591FF', '#6964FF', '#9E36FF', '#D208FF']

    for value, count in zip(values, counts):
        ax.plot([value]*count, list(range(count)), 'co', c=colors[value - 1], ms=int(200 / max(counts)), linestyle='')

    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)

    ax.yaxis.set_visible(False)
    ax.set_ylim(-0.75, max(counts))
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels(['Mostly Objective', '', 'Somewhat Subjective', '', 'Very Subjective'])
    ax.tick_params(axis='x', length=0, pad=8, labelsize=18)
    ax.set_title('Song Subjectivity Distribution', fontsize=18)

    plt.savefig('subjectivities_dist.png')

    img_subjectivities  = Image.open('subjectivities_dist.png')

    return img_subjectivities

"""
Generates Song Polarity Distribution
"""
def get_song_polarity(polarities):
    values, counts = np.unique(polarities, return_counts=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['#FF0000', '#E32A01', '#C65502', '#AA8004', '#8EAA05', '#71D506', '#55FF07']

    for value, count in zip(values, counts):
        ax.plot([value]*count, list(range(count)), 'co', c=colors[value + 3], ms=int(200 / max(counts)), linestyle='')

    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)

    ax.yaxis.set_visible(False)
    ax.set_ylim(-0.75, max(counts))
    ax.set_xticks(range(-3, 4))
    ax.set_xticklabels(['---', '--', '-', 'o', '+', '++', '+++'])
    ax.tick_params(axis='x', length=0, pad=8, labelsize=18)
    ax.set_title('Song Polarity Distribution', fontsize=18)

    plt.savefig('polarities_dist.png')

    img_polarities  = Image.open('polarities_dist.png')

    polarity_value = sum(values * counts)
    polarity_verdict = 'are Neutral'

    if polarity_value < -15:
        polarity_verdict = 'are Negative'
    elif polarity_value < 0:
        polarity_verdict = 'lean Negative'
    elif polarity_value > 15:
        polarity_verdict = 'are Positive'
    elif polarity_value > 0:
        polarity_verdict = 'lean Positive'

    print("This artist's song lyrics " + polarity_verdict + ".")

    return img_polarities

"""
Generates Song Sentiment Distribution
"""
def get_song_sentiments(all_songs):
    polarities = []
    subjectivities = []
    for song in all_songs:
        blob = TextBlob(song)
        song_polarity = blob.sentiment.polarity
        song_subjectivity = blob.sentiment.subjectivity
        #polarities.append(song_polarity)
        #print(blob.tags)
        #print(blob.noun_phrases)
        #print(blob.sentiment)

        if song_polarity < -0.50:
            polarities.append(-3)
        elif song_polarity < -0.25:
            polarities.append(-2)
        elif song_polarity < -0.05:
            polarities.append(-1)
        elif song_polarity <  0.05:
            polarities.append(0)
        elif song_polarity <  0.25:
            polarities.append(1)
        elif song_polarity <  0.50:
            polarities.append(2)
        else:
            polarities.append(3)

        if song_subjectivity < 0.3:
            subjectivities.append(1)
        elif song_subjectivity < 0.4:
            subjectivities.append(2)
        elif song_subjectivity < 0.6:
            subjectivities.append(3)
        elif song_subjectivity <  0.7:
            subjectivities.append(4)
        else:
            subjectivities.append(5)

    return get_song_polarity(polarities), get_song_subjectivity(subjectivities)

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

            #if len(song_lyrics) >= 15:
            #    break

    all_songs = [' '.join(lyric) for lyric in song_lyrics]
    all_lyrics = ' '.join(all_songs)

    print(all_songs)
    print(all_lyrics)

    img_wordcloud = word_cloud(all_lyrics)

    img_polarities, img_subjectivities = get_song_sentiments(all_songs)

    return img_subjectivities

if __name__ == '__main__':
    app.run_server(debug=True)
