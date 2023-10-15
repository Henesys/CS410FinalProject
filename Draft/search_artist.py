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
nltk.download('stopwords')


genius = Genius("irpjON-Z1GSt9nz-xhFe-wtKAuFnjrYZ4jP1-9uK6yOQ1dafktyUZzZIQmuGPVkD")
genius.remove_section_headers = True
top_song_num = 10
stop_words = set(stopwords.words('english'))

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(dcc.Input(id='query_artist', type='text', placeholder="Insert Artist Name", debounce=True, minLength=1)),
        html.Button('Submit', id='submit_artist', n_clicks=0),
        html.Br(),
        html.Img(id="query_artist_img"),
        html.Div(id="query_artist_lyrics"),
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
    lyric_tokens = word_tokenize(lyrics_lines)
    filtered_lyrics = [w.lower() for w in lyric_tokens if not w.lower() in stop_words]

    blob = TextBlob(' '.join(filtered_lyrics))
    print(blob.sentiment)

    return filtered_lyrics


@callback(
    Output("query_artist_img", "src"),
    Input("query_artist", "value"),
    Input("submit_artist", "n_clicks"),
)
def get_image(query_artist, n_clicks):
    if n_clicks == 0 or query_artist == '':
        return None

    n_clicks = 0
    artist = genius.search_artist(query_artist, max_songs=1, sort='popularity') #max_songs set for testing efficiency
    artist_img = artist.header_image_url
    response = requests.get(artist_img)
    img = Image.open(BytesIO(response.content))

    return img


@callback(
    Output("query_artist_lyrics", "children"),
    Input("query_artist", "value"),
    Input("submit_artist", "n_clicks"),
)
def get_lyrics(query_artist, n_clicks):
    if n_clicks == 0:
        return None

    n_clicks = 0
    artist = genius.search_artist(query_artist, max_songs=20, sort='popularity') #max_songs set for testing efficiency
    song_list = artist.songs

    song_titles = []
    song_lyrics = []
    for song in song_list:
        is_new, song_title = check_repeat(song_titles, song.title)
        if is_new:
            song_titles.append(song_title)

            lyrics = process_lyrics(song.lyrics)
            song_lyrics.append(lyrics)

    songs = dict(zip(song_titles[:10], song_lyrics[:10]))
    #artist.save_lyrics()
    return ' '.join(song_lyrics[-1])

if __name__ == '__main__':
    app.run_server(debug=True)
