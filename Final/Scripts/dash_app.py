import os

# API Code
import genius
from spotify import *

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Dash
import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Data Visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests

# Images (get_artist_face)
from io import BytesIO

# Import Modules
import base64
import genius
from PIL import Image, ImageFile
from io import BytesIO
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Fix matplotlib to work in a non-interactive mode
plt.switch_backend("Agg")

dir = os.path.dirname(__file__)

# Text Formatting
text_style = {"text-align": "center"}
image_style = {"height": "auto", "width": "100%"}

# Loading Base Features/Images of Webapp
app = Dash(external_stylesheets=[dbc.themes.MINTY])
default_color = default_color = "rgb(121, 41, 82)"
spt_img = Image.open(os.path.join(dir, "./Figures/spotify.png"))
gns_img = Image.open(os.path.join(dir, "./Figures/genius.png"))

"""
Search Bar Input/Functionality
"""
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
        html.Br(),
        dbc.Spinner(
            html.Div(id="loading_output"),
            color="success",
            spinner_style={"width": "3rem", "height": "3rem"},
        ),
    ],
    className="mb-3",
)

form = dbc.Form([artist_input])


"""
'Artist' Tab Content
"""
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Img(
                                id="artist_img",
                                style={"height": "auto", "width": "100%"},
                            ),
                        ],
                        style={"textAlign": "center"},
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Center(html.H1([dbc.Badge("Who's That Artist?", className="ms-1", color="danger")])),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader("Providing Search Results for:"),
                                            dbc.CardBody(
                                                [
                                                    html.H1(id="artist1", className="card-title"),
                                                ]
                                            ),
                                        ],
                                        style={"textAlign": "center", "width": "75%"},
                                    ),
                                ],
                                justify="center",
                            ),
                            html.Br(),
                            html.Br(),
                            html.H3("CS410 Course Project"),
                            html.H3("Fall 2023"),
                        ],
                        align="center",
                        style={"textAlign": "center"},
                        width=6,
                    ),
                ]
            )
        ]
    ),
    className="mt-3",
)

"""
'Lyrics: Word Usage' Tab Content
"""
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Center(html.H2([dbc.Badge("Lyrics Considered", className="ms-1", color="danger")])),
                            html.H4(html.Div(id="artist_titles")),
                            html.Br(),
                        ],
                        style={"textAlign": "center"},
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Center(html.H2([dbc.Badge("Common Themes", className="ms-1", color="info")])),
                            html.H4(html.Div(id="themes")),
                            html.Br(),
                            html.Center(html.H2([dbc.Badge("Word Cloud", className="ms-1", color="info")])),
                            html.Img(
                                id="word_cloud",
                                style={"height": "auto", "width": "90%"},
                            ),
                            html.Br(),
                        ],
                        style={"textAlign": "center"},
                        width=6,
                    ),
                ]
            )
        ]
    ),
    className="mt-3",
)

"""
'Lyrics: Sentiment' Tab Content
"""
tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Center(html.H2([dbc.Badge("Polarity", className="ms-1", color="info")])),
                            #dbc.CardHeader(html.H2("Polarity", className="card-title")),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Center(html.H3([dbc.Badge("Rating", className="ms-1", color="light")])),
                                                    html.Br(),
                                                    html.H1(id="polarity_verdict"),
                                                ]),
                                                className="border-0",
                                            ),
                                        ],
                                        style={"textAlign": "center"},
                                        className="h-25",
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Center(html.H3([dbc.Badge("About", className="ms-1", color="light")])),
                                                    html.H5("Polarity describes the positivity/negativity conveyed by the lyrics."),
                                                    html.H5("Our scale ranges from '---' (very negative) to 'o' (neutral) to '+++' (very positive)."),
                                                ]),
                                                className="border-0",
                                            ),
                                        ],
                                        style={"textAlign": "center", "border-left":"2px solid", "border-left-color":"#e3e6e4"},
                                        width=8,
                                    ),
                                ],
                            ),
                            html.Br(),
                            dbc.Row([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Center(html.H3([dbc.Badge("Song Polarity Distribution", className="ms-1", color="light")])),
                                            html.Img(
                                                id="polarities_dist",
                                                style={"height": "auto", "width": "90%"},
                                            ),
                                        ]),
                                        className="border-0",
                                    ),
                                ],
                                style={"textAlign": "center", "border-top":"2px solid", "border-top-color":"#e3e6e4", "margin-left": "3px", "margin-right": "3px"}
                            ),
                        ],
                        style={"textAlign": "center", "border-right":"2px solid", "border-right-color":"#e3e6e4"},
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Center(html.H2([dbc.Badge("Subjectivity", className="ms-1", color="info")])),
                            #dbc.CardHeader(html.H2("Subjectivity", className="card-title")),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Center(html.H3([dbc.Badge("Rating", className="ms-1", color="light")])),
                                                    html.Br(),
                                                    html.H1(id="subjectivity_rating"),
                                                ]),
                                                className="border-0",
                                            ),
                                        ],
                                        style={"textAlign": "center"},
                                        className="h-25",
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Center(html.H3([dbc.Badge("About", className="ms-1", color="light")])),
                                                    html.H5("Subjectivity describes whether the lyrics are opinionated or factual."),
                                                    html.H5("Our scale ranges from 1 (factual/objective) to 10 (very opinionated/subjective)."),
                                                ]),
                                                className="border-0",
                                            ),
                                        ],
                                        style={"textAlign": "center", "border-left":"2px solid", "border-left-color":"#e3e6e4"},
                                        width=8,
                                    ),
                                ],
                            ),
                            html.Br(),
                            dbc.Row([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.Center(html.H3([dbc.Badge("Song Subjectivity Distribution", className="ms-1", color="light")])),
                                            html.Img(
                                                id="subjectivities_dist",
                                                style={"height": "auto", "width": "90%"},
                                            ),
                                        ]),
                                        className="border-0",
                                    ),
                                ],
                                style={"textAlign": "center", "border-top":"2px solid", "border-top-color":"#e3e6e4", "margin-left": "3px", "margin-right": "3px"}
                            ),
                        ],
                        style={"textAlign": "center"},
                        width=6,
                    ),
                ]
            )
        ]
    ),
    className="mt-3",
)

"""
'Audio Features' Tab Content
"""
tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.Center(html.H3([dbc.Badge("Distributions", className="ms-1", color="info")])),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Center(html.H3([dbc.Badge("Danceability", className="ms-1", color="light")])),
                            html.Img(
                                id="distribution_plot",
                                style={"height": "auto", "width": "100%"},
                            ),
                        ],
                        style={"textAlign": "center"},
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Center(html.H3([dbc.Badge("Energy", className="ms-1", color="light")])),
                            html.Img(
                                id="distribution_plot2",
                                style={"height": "auto", "width": "100%"},
                            ),
                        ],
                        style={"textAlign": "center"},
                        width=6,
                    ),
                ]
            ),

            html.Br(),
            html.Center(html.H3([dbc.Badge("Pair Plots", className="ms-1", color="info")])),
            html.Img(
                id="pair_plot",
                style={"height": "auto", "width": "90%"},
            ),
        ]
    ),
    style={"textAlign": "center"},
    className="mt-3",
)

"""
'Search' Page Layout
"""
layout_search = html.Div(
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
                    html.Img(src=gns_img, style={"height": "64px", "width": "auto"}),
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
    ],
    style={"padding": 50},
)

"""
'Result' Page Layout
"""
layout_result = html.Div(
    [
        dbc.Button("Search", href="/", style={"textAlign": "center"}),
        html.Br(),
        html.Br(),
        #html.H1(id="artist", style={"textAlign": "center"}),
        html.Center(html.H1([dbc.Badge(id="artist", className="ms-1", color="success")])),
        html.Br(),
        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Artist"),
                dbc.Tab(tab2_content, label="Lyrics: Word Usage"),
                dbc.Tab(tab3_content, label="Lyrics: Sentiment"),
                dbc.Tab(tab4_content, label="Audio Features"),
            ]
        ),
    ],
    style={"padding": 50},
)

"""
Main Dash App Page Functionality
"""
app.layout = html.Div([
    # represents the browser address bar and doesn't render anything
    dcc.Location(id='url', refresh=False),

    # content will be rendered in this element
    html.Div(id='page-content')
])


"""
Dash Functions
"""
# determines Dash application page URL
@callback(
        Output('page-content', 'children'), 
        Input('url', 'pathname')
        )
def display_page(pathname):
    if pathname == "/result":
        return layout_result
    else:
        return layout_search

# retrieves information obtained through Spotify API analysis
@callback(
    [
        Output("artist1", "children"),
        Output("artist_img", "src"),
        Output("distribution_plot", "src"),
        Output("distribution_plot2", "src"),
        Output("pair_plot", "src"),
    ],
        [ Input('url', 'pathname'), ]
        )
def display_page_spotify(pathname):
    if pathname == "/result":
        with open(os.path.join(dir, './Figures/artist.txt'), encoding='utf-8') as f:
            artist = f.read().rstrip()

        artist_img_path = os.path.join(dir, "../Artists/Images/" + artist + "_image.jpg")
        artist_img = Image.open(artist_img_path)

        dist_plot_path = os.path.join(dir, "../Artists/Figures/" + artist + "_Danceabilityfigure.png")
        dist_plot_img = Image.open(dist_plot_path)

        dist_plot_path2 = os.path.join(dir, "../Artists/Figures/" + artist + "_Energyfigure.png")
        dist_plot_img2 = Image.open(dist_plot_path2)

        pair_plot_path = os.path.join(dir, "../Artists/Figures/" + artist + "_pfigure.png")
        pair_plot_img = Image.open(pair_plot_path)

        return artist, artist_img, dist_plot_img, dist_plot_img2, pair_plot_img
    return 'Waiting...', None, None, None, None

# retrieves information obtained through Genius API analysis
@callback(
    [
        Output("artist", "children"),
        Output("artist_titles", "children"),
        Output("themes", "children"),  # ['reputation', 'dream', 'problem']
        Output("word_cloud", "src"),  # PIL image
        Output("polarities_dist", "src"),  # PIL image
        Output("subjectivities_dist", "src"),  # PIL image
        Output("subjectivity_rating", "children"),  # 3.5 (one decimal)
        Output(
            "polarity_verdict", "children"
        ),  # '---', '--', '-', 'o', '+', '++', '+++'
        #Output("element-to-hide", component_property="style"),
    ],
        [ Input('url', 'pathname'), ]
        )
def display_page_genius(pathname):
    if pathname == "/result":
        themes = []
        polarity_verdict = 'o'
        subjectivity_rating = '1.0'
        artist = 'Search'

        with open(os.path.join(dir, './Figures/artist.txt'), encoding='utf-8') as f:
            artist = f.read().rstrip()

        with open(os.path.join(dir, './Figures/artist_titles.txt'), encoding='utf-8') as f:
            artist_titles = f.read().splitlines()

        with open(os.path.join(dir, './Figures/themes.txt'), encoding='utf-8') as f:
            themes = f.read().splitlines()

        with open(os.path.join(dir, './Figures/polarity_verdict.txt'), encoding='utf-8') as f:
            polarity_verdict = f.read().rstrip()

        with open(os.path.join(dir, './Figures/subjectivity_rating.txt'), encoding='utf-8') as f:
            subjectivity_rating = f.read().rstrip()

        polarities_path = os.path.join(dir, "./Figures/polarities_dist.png")
        polarities_dist  = Image.open(polarities_path)

        wordcloud_path = os.path.join(dir, "./Figures/word_cloud.png")
        word_cloud  = Image.open(wordcloud_path)

        subjectivities_path = os.path.join(dir, "./Figures/subjectivities_dist.png")
        subjectivities_dist  = Image.open(subjectivities_path)

        return artist, dbc.ListGroup([dbc.ListGroupItem(x.title()) for x in artist_titles], className="mb-2",), dbc.ListGroup([dbc.ListGroupItem(x) for x in themes], className="mb-2",), word_cloud, polarities_dist, subjectivities_dist, subjectivity_rating, polarity_verdict
    return 'Going Back...', None, None, None, None, None, None, None

# calls Spotify/Genius API analysis code with queried artist as input
@callback(
    [
        Output("query_artist_lyrics", "children"),  # 'lyrics lyrics lyrics'
        Output("loading_output", "children"),
        Output("url", 'pathname'),
    ],
    [State("query_artist", "value"), Input("submit_artist", "n_clicks")],
)
def process(query_artist, n_clicks):
    if n_clicks == 0:
        return None, None, "/"

    n_clicks = 0

    (
        all_songs,
        themes,
        img_wordcloud,
        img_polarities,
        img_subjectivities,
        subjectivity_rating,
        polarity_verdict,
    ) = genius.process_artist_lyrics(query_artist)

    get_artist_info_csv_smaller(query_artist)
    get_artist_face(query_artist)

    csv_folder = os.path.join(dir, "CSV")
    csv_path = os.path.join(csv_folder, query_artist + "_info.csv")
    df = pd.read_csv(csv_path)

    create_distribution_plot(df, "Danceability", "blue", "Distribution Plot", query_artist)
    create_distribution_plot(df, "Energy", "red", "Distribution Plot", query_artist)
    create_pairplot(df, query_artist)

    return (
        "Showing Results...",
        None,
        "/result"
    )

# main function to run application
if __name__ == "__main__":
    app.run_server(debug=False)
