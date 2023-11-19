# Dash
import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Mini Spotify --> Change to Spotify Later
from mini_spotify import get_artist_info_csv, get_artist_face

# Images (get_artist_face)
from PIL import Image
import requests
from io import BytesIO

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Spotify Artist Info"),
        html.Label("Enter Artist's Name:"),
        dcc.Input(id="artist-input", type="text", value=""),
        html.Button("Submit", id="submit-button"),
        html.Div(id="output-message"),
        html.Img(id="artist-image", src=""),
    ]
)


@app.callback(
    [Output("output-message", "children"), Output("artist-image", "src")],
    [Input("submit-button", "n_clicks")],
    [State("artist-input", "value")],
)
def update_output(n_clicks, artist_name):
    if n_clicks is not None:
        try:
            get_artist_info_csv(artist_name)
            get_artist_face(artist_name)

            image_path = f"Final/Scripts/test/{artist_name}_image.jpg"
            return f"Info saved @ {artist_name}_info.csv", image_path if os.path.exists(image_path) else ""
        except Exception as e:
            return f"Error: {str(e)}", ""

    return "", ""


if __name__ == "__main__":
    app.run_server(debug=True)
