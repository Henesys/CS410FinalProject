import dash
from dash import Dash, dcc, html, Input, Output, callback
from lyricsgenius import Genius
from PIL import Image
import requests
from io import BytesIO

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

def process_lyrics(lyrics):
    lyrics_lines = lyrics.splitlines()

    return lyrics_lines

@callback(
    Output("query_artist_img", "src"),
    Input("query_artist", "value"),
    Input("submit_artist", "n_clicks"),
)
def get_image(query_artist, n_clicks):
    if n_clicks == 0:
        return None

    n_clicks = 0
    genius = Genius("irpjON-Z1GSt9nz-xhFe-wtKAuFnjrYZ4jP1-9uK6yOQ1dafktyUZzZIQmuGPVkD")
    artist = genius.search_artist(query_artist, max_songs=1) #max_songs set for testing efficiency
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
    genius = Genius("irpjON-Z1GSt9nz-xhFe-wtKAuFnjrYZ4jP1-9uK6yOQ1dafktyUZzZIQmuGPVkD")
    artist = genius.search_artist(query_artist, max_songs=2) #max_songs set for testing efficiency
    song_list = artist.songs

    song_titles = []
    song_lyrics = []
    for song in song_list:
        song_titles.append(song.title)

        lyrics = process_lyrics(song.lyrics)
        song_lyrics.append(lyrics)

    songs = dict(zip(song_titles, song_lyrics))
    print(songs)
    #artist.save_lyrics()
    return song.lyrics

if __name__ == '__main__':
    app.run_server(debug=True)
