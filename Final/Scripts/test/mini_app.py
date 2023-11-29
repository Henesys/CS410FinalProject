# Dash
import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Data Visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import base64
import time
import requests

# Mini Spotify --> Change to Spotify Later
from mini_spotify import get_artist_info_csv_smaller, get_artist_face

# Images (get_artist_face)
from PIL import Image
from io import BytesIO

# Fix matplotlib to work in a non-interactive mode
plt.switch_backend("Agg")

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Spotify Artist Info"),
        html.Label("Enter Artist's Name:"),
        dcc.Input(id="artist-input", type="text", value=""),
        html.Button("Submit", id="submit-button"),
        html.Div(id="output-message"),
        html.Img(id="artist-image", src=""),
        html.Img(id="distribution-plot", src=""),
        html.Img(id="pairplot", src=""),
        html.Img(id="heatmap", src=""),
    ]
)


# Visualizations
def create_distribution_plot(df, column, color, title):
    # Error with df?
    if len(df) == 0:
        return "Empty DataFrame"

    plt.figure(figsize=(15, 10))
    plot = sns.histplot(df[column], kde=True, color=color)
    plot.set_title(title)
    img_buf = BytesIO()
    plt.savefig(img_buf, format="png")
    img_buf.seek(0)
    plt.close()  # Close plot to avoid GUI errors
    return f"data:image/png;base64,{base64.b64encode(img_buf.read()).decode()}"


def create_pairplot(df):
    plt.figure(figsize=(20, 10))
    plot = sns.pairplot(df)
    img_buf = BytesIO()
    plt.savefig(img_buf, format="png")
    img_buf.seek(0)
    plt.close()  # Close plot to avoid GUI errors
    return f"data:image/png;base64,{base64.b64encode(img_buf.read()).decode()}"


def create_heatmap(corr_matrix):
    plt.figure(figsize=(20, 10))
    plot = sns.heatmap(corr_matrix, annot=True)
    img_buf = BytesIO()
    plt.savefig(img_buf, format="png")
    img_buf.seek(0)
    plt.close()  # Close plot to avoid GUI errors
    return f"data:image/png;base64,{base64.b64encode(img_buf.read()).decode()}"


@app.callback(
    [
        Output("output-message", "children"),
        Output("artist-image", "src"),
        Output("distribution-plot", "src"),
        Output("pairplot", "src"),
        Output("heatmap", "src"),
    ],
    [Input("submit-button", "n_clicks")],
    [State("artist-input", "value")],
)
def update_output(n_clicks, artist_name):
    if n_clicks is not None:
        try:
            # Trying to avoid 429
            time.sleep(20)

            get_artist_info_csv_smaller(artist_name)
            get_artist_face(artist_name)

            # Load data from CSV
            csv_path = f"Final/Scripts/test/{artist_name}_info.csv"
            df = pd.read_csv(csv_path)

            # Visualizations
            dist_plot = create_distribution_plot(
                df, "Danceability", "blue", "Danceability Distribution"
            )
            pairplot = create_pairplot(df)
            heatmap = create_heatmap(df.corr())

            return (
                f"Artist Info saved @ {artist_name}_info.csv",
                f"Final/Scripts/test/{artist_name}_image.jpg",
                dist_plot,
                pairplot,
                heatmap,
            )

        # https://community.spotify.com/t5/Spotify-for-Developers/Max-retries-reached-too-many-429-error-responses-on-audio/td-p/5656742
        # spotify Error: http status: 429, code:-1 - /v1/audio-features/?ids=4WUepByoeqcedHoYhSNHRt: Max Retries, reason: too many 429 error responses
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                return (
                    "Error: Rate limit exceeded. Please try again later.",
                    "",
                    "",
                    "",
                    "",
                )
            else:
                return f"Error: {str(e)}", "", "", "", ""

        except Exception as e:
            return f"Error: {str(e)}", "", "", "", ""

    return "", "", "", "", ""


if __name__ == "__main__":
    app.run_server(debug=True)
