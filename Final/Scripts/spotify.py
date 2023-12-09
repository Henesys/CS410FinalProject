# Spotify
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

# Analysis/NLP
import colorama
from colorama import Fore

# Data Visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# CSV Pipeline
from tabulate import tabulate
import csv
import requests
from PIL import Image
from io import BytesIO

# Path
import os

dir = os.path.dirname(__file__)

# Credentials
import credentials

client_id = credentials.CLIENT_ID
client_secret = credentials.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""
Creates CSV w/ Artist's Discography Information
"""


def get_artist_info_csv_smaller(artist_name):
    # Enter artist's name
    results = sp.search(q="artist:" + artist_name, type="artist")

    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]

        # Artist's top tracks with an initial limit
        # Dynamically increase to get max amount of tracks for proper data analysis
        # artist_top_tracks only gets 10, couldn't adjust limit

        # Get the artist's albums --> fetch individual tracks
        albums = sp.artist_albums(
            artist["id"], album_type="album", country=None, limit=5
        )

        all_tracks = []

        # Retrieve tracks from each album
        for album in albums["items"]:
            album_tracks = sp.album_tracks(album["id"], limit=5)
            all_tracks.extend(album_tracks["items"])

        # https://www.freecodecamp.org/news/with-open-in-python-with-statement-syntax-example/
        # https://www.geeksforgeeks.org/how-to-open-a-file-using-the-with-statement/
        # https://note.nkmk.me/en/python-file-io-open-with/

        # with open(os.path.join(dir, ""))

        csv_folder = os.path.join(dir, "CSV")
        csv_path = os.path.join(csv_folder, f"{artist_name}_info.csv")

        with open(csv_path, "w", newline="") as csvfile:
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

            # # # https://developer.spotify.com/documentation/web-api/reference/get-audio-features
            for track in all_tracks:
                audio_features = sp.audio_features(track["id"])[0]
                writer.writerow(
                    {
                        "Track Name": track["name"],
                        "Acousticness": audio_features["acousticness"],
                        "Danceability": audio_features["danceability"],
                        "Duration": audio_features["duration_ms"],
                        "Energy": audio_features["energy"],
                        "Instrumentalness": audio_features["instrumentalness"],
                        "Loudness": audio_features["loudness"],
                        "Speechiness": audio_features["speechiness"],
                        "Tempo": audio_features["tempo"],
                        "Valence": audio_features["valence"],
                    }
                )

        print(f'Artist: {artist["name"]}')
        print(f"Info saved @ {artist_name}_info.csv")

    else:
        print(f'Artist "{artist_name}" not found.')


"""
Gets Artist's Face
"""


def get_artist_face(artist_name):
    # Enter artist's name
    results = sp.search(q="artist:" + artist_name, type="artist")

    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]

        # Face
        if artist["images"]:
            image_url = artist["images"][0]["url"]
            response = requests.get(image_url)

            # https://developer.spotify.com/documentation/web-api/reference/get-an-artist
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image.save(f"Final/Artists/Images/{artist_name}_image.jpg")

                print(f'Artist\'s Name: {artist["name"]}')
                print(f"Artist's face saved as {artist_name}_face.jpg")

            else:
                print("Failed to fetch artist's profile image.")

        else:
            print(f'Artist "{artist_name}" does not have an image of their face.')

    else:
        print(f'Artist "{artist_name}" not found.')


# Prompt
# artist_name = input("Enter an artist's name: ")
# get_artist_face(artist_name)

"""
Create Distribution Plot
"""


# Visualizations


# 상
def create_distribution_plot(df, column, color, title, artist_name):
    # Error with df?
    if len(df) == 0:
        return "Empty DataFrame"

    plt.figure(figsize=(15, 10))
    plot = sns.histplot(df[column], kde=True, color=color)
    plot.set_title(title)

    dist_plot_path = os.path.join(dir, "../Artists/Figures/" + artist_name + "_" + column + "figure.png")

    plt.savefig(dist_plot_path)

    im = Image.open(dist_plot_path)

    return im


def create_pairplot(df, artist_name):
    plt.figure(figsize=(20, 10))
    plot = sns.pairplot(df)

    pair_plot_path = os.path.join(dir, "../Artists/Figures/" + artist_name + "_pfigure.png")

    plt.savefig(pair_plot_path)

    im = Image.open(pair_plot_path)

    return im
