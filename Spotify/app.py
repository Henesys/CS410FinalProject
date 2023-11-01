#!/usr/bin/env python

import os

# Credentials
import credentials

client_id = credentials.CLIENT_ID
client_secret = credentials.CLIENT_SECRET

# Dash
import dash
from dash import Dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64

# Spotify
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

# Analysis/ NLP
import colorama
from colorama import Fore
import textblob
from textblob import TextBlob

# Visualization/ Output
from tabulate import tabulate
import csv
import requests
from PIL import Image
from io import BytesIO

# Initialize Spotify API
# Credentials | localhost:8888/callback
# Might need to export + echo @ bash

# CLIENT_SECRET HAS BEEN ROTATED, STORE @ GITIGNORE
# CLIENT_ID = "X"
# CLIENT_SECRET = "X"

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app = dash.Dash(__name__)

# Dash App Layout
app.layout = html.Div(
    [
        dcc.Input(id="artist-name", type="text", placeholder="Enter an artist's name"),
        html.Button("Search", id="search-button"),
        html.Div(id="output"),
        html.Div(id="image-output"),
        dcc.Download(id="download-csv"),
    ]
)


# Dash App Callback
@app.callback(
    [Output("output", "children"), Output("image-output", "children")],
    [Input("search-button", "n_clicks")],
    [State("artist-name", "value")],
)


# Modify get_artist_info_csv + get_artist_face @ song_data.ipynb
def get_artist_song_info(n_clicks, artist_name):
    if n_clicks and artist_name:
        # Enter artist's name
        results = sp.search(q="artist:" + artist_name, type="artist")

        if results["artists"]["items"]:
            artist = results["artists"]["items"][0]

            # Face
            if artist["images"]:
                image_url = artist["images"][0]["url"]
                response = requests.get(image_url)

                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    image.save(f"{artist_name}_image.jpg")

                    # Face @ base64 read into file
                    encoded_image = base64.b64encode(
                        open(f"{artist_name}_image.jpg", "rb").read()
                    )

                    image_output = html.Img(
                        src=f"data:image/jpeg;base64,{encoded_image.decode()}",
                        width=300,
                    )

                    top_tracks = sp.artist_top_tracks(artist["id"])

                    # Spotify Artist Info into CSV
                    with open(f"{artist_name}_info.csv", "w", newline="") as csvfile:
                        fieldnames = [
                            "Track Name",
                            "Acousticness",
                            "Danceability",
                            "Duration",
                            "Energy",
                            "Instrumentalness",
                            "Loudness",
                            "Speechiness",
                            "Tempo",
                            "Valence",
                        ]
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()

                        for track in top_tracks["tracks"]:
                            audio_features = sp.audio_features(track["id"])[0]
                            writer.writerow(
                                {
                                    "Track Name": track["name"],
                                    "Acousticness": audio_features["acousticness"],
                                    "Danceability": audio_features["danceability"],
                                    "Duration": audio_features["duration_ms"],
                                    "Energy": audio_features["energy"],
                                    "Instrumentalness": audio_features[
                                        "instrumentalness"
                                    ],
                                    "Loudness": audio_features["loudness"],
                                    "Speechiness": audio_features["speechiness"],
                                    "Tempo": audio_features["tempo"],
                                    "Valence": audio_features["valence"],
                                }
                            )

                    # CSV Download Link
                    download_link = dcc.Link(
                        "Download CSV",
                        id="download-link",
                        href=f"/{artist_name}_info.csv",
                    )

                    return [
                        f'Artist: {artist["name"]}\nPopularity: {artist["popularity"]}',
                        image_output,
                    ]

        return ["Artist not found.", None]


if __name__ == "__main__":
    app.run_server(debug=True)
