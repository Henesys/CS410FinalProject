import os

# API Code
import genius
import spotify

# Dash
import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# NLTK
import nltk

nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("stopwords", quiet=True)

# Import Modules
import base64
import genius
from PIL import Image
import time

dir = os.path.dirname(__file__)

# Text Formatting
text_style = {"text-align": "center"}
image_style = {"height": "auto", "width": "100%"}

app = Dash(external_stylesheets=[dbc.themes.MINTY])
default_color = default_color = "rgb(121, 41, 82)"
spt_img = Image.open(os.path.join(dir, "./Figures/spotify.png"))
gen_img = Image.open(os.path.join(dir, "./Figures/genius.png"))

# Search Tab
artist_input = html.Div(
    [
        html.H3("Enter Artist's Name Below:", style=text_style),
        dbc.Input(
            type="text",
            id="query_artist",
            placeholder="Name",
            style={"width": "50%", "text-align": "center"},
        ),
        dbc.Col(
            dbc.Button(
                "Search",
                color="primary",
                id="submit_artist",
                n_clicks=0,
                style={"width": "50%"},
            ),
            width="auto",
        ),
        html.Br(),
        dbc.Spinner(
            html.Div(id="loading_output"),
            color="success",
            spinner_style={"width": "3rem", "height": "3rem"},
        ),
    ],
    className="mb-3",
)

# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/
form = dbc.Form([artist_input])

# Genius + Spotify
accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Card(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H3("Overall Polarity:"),
                                        html.Br(),
                                        html.H1(id="polarity_verdict"),
                                        html.Br(),
                                    ],
                                    style={"textAlign": "center"},
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.H3("Common Topics:"),
                                        html.Br(),
                                        html.Div(id="themes"),
                                        html.Br(),
                                    ],
                                    style={"textAlign": "center"},
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.H3("Subjectivity Rating:"),
                                        html.Br(),
                                        html.H1(id="subjectivity_rating"),
                                        html.Br(),
                                    ],
                                    style={"textAlign": "center"},
                                    width=4,
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H3("Word Cloud:"),
                                        html.Img(
                                            id="word_cloud",
                                            style={"height": "auto", "width": "90%"},
                                        ),
                                    ],
                                    style={"textAlign": "center"},
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        html.H3("Lyric Polarity Distribution:"),
                                        html.Img(
                                            id="polarities_dist",
                                            style={"height": "auto", "width": "90%"},
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.H3("Lyric Subjectivity Distribution"),
                                        html.Img(
                                            id="subjectivities_dist",
                                            style={"height": "auto", "width": "90%"},
                                        ),
                                    ],
                                    style={"textAlign": "center"},
                                    width=6,
                                ),
                            ]
                        ),
                    ],
                    className="border-0 bg-transparent",
                ),
                title="Lyrical Analysis",
            ),
            dbc.AccordionItem(
                [
                    html.H3("Top Spotify Tracks:"),
                    html.Br(),
                    html.Div(id="spotify_tracks"),
                    html.Br(),
                ],
                title="Musical Analysis",
            ),
        ],
        flush=True,
        id="element-to-hide",
        start_collapsed=True,
    ),
)

# App Layout
app.layout = html.Div(
    [
        dbc.Card(
            dbc.Row(
                [
                    html.Img(src=spt_img, style={"height": "64px", "width": "auto"}),
                    dbc.Col(
                        html.H1(
                            children="Who's That Artist?!",
                            style={
                                "textAlign": "center",
                                "color": "green",
                                "vertical-align": "center",
                            },
                        )
                    ),
                    html.Img(src=spt_img, style={"height": "64px", "width": "auto"}),
                ]
            ),
            className="border-0 bg-transparent",
        ),
        html.Br(),
        html.Center(form),
        html.H2(
            id="query_artist_lyrics",
            style={"textAlign": "center", "vertical-align": "center"},
        ),
        html.Br(),
        html.Center(accordion),
    ],
    style={"padding": 50},
)

# Genius Callback
@app.callback(
    [
        Output("query_artist_lyrics", "children"),
        Output("themes", "children"),
        Output("word_cloud", "src"),
        Output("polarities_dist", "src"),
        Output("subjectivities_dist", "src"),
        Output("subjectivity_rating", "children"),
        Output("polarity_verdict", "children"),
        Output("loading_output", "children"),
        Output("element-to-hide", component_property="style"),
    ],
    [State("query_artist", "value"), Input("submit_artist", "n_clicks")],
)
def process(query_artist, n_clicks):
    if n_clicks == 0 or query_artist is None:
        return None, None, None, None, None, None, None, None, {"display": "none"}

    (
        all_songs,
        themes,
        img_wordcloud,
        img_polarities,
        img_subjectivities,
        subjectivity_rating,
        polarity_verdict,
    ) = genius.process_artist_lyrics(query_artist)

    return (
        "Artist Breakdown",
        html.Ul([html.H4(x) for x in themes], style={"padding": 0}),
        img_wordcloud,
        img_polarities,
        img_subjectivities,
        subjectivity_rating,
        polarity_verdict,
        None,
        {"display": "block"},
    )

# Spotify Callback
@app.callback(
    Output("spotify_tracks", "children"),
    [Input("submit_artist", "n_clicks")],
    [State("query_artist", "value")],
)
def get_spotify_tracks(n_clicks, query_artist):
    if n_clicks == 0 or query_artist is None:
        return None

    # Call Spotify functions from spotify.py to get top tracks
    top_tracks = spotipy.get_top_tracks(query_artist)

    # Display top tracks
    return html.Ul([html.Li(track) for track in top_tracks])

if __name__ == "__main__":
    app.run_server(debug=True)
