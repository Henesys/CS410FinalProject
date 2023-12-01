import os

# API Code
import genius
import spotify

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
import base64
import time
import requests

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

app = Dash(external_stylesheets=[dbc.themes.MINTY])
default_color = default_color = "rgb(121, 41, 82)"
spt_img = Image.open(os.path.join(dir, "./Figures/spotify.png"))

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

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("artist image here? / maybe songs list considered if relevant", className="card-text"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
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
                    dbc.Col(
                        [
                            html.Center(html.H2([dbc.Badge("Common Topics", className="ms-1", color="info")])),
                            html.H4(html.Div(id="themes")),
                            html.Br(),
                            html.H1("filler filler filler")
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
                                        style={"textAlign": "center", "border-right":"2px solid", "border-right-color":"#e3e6e4"},
                                        className="h-25",
                                        width=4,
                                    ),
                                    dbc.Col(
                                        
                                        [
                                            html.H3("idk"),
                                            html.Br(),
                                            html.H3("maybe an explanation?"),
                                            html.Br(),
                                        ],
                                        style={"textAlign": "center"},
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
                                        style={"textAlign": "center", "border-right":"2px solid", "border-right-color":"#e3e6e4"},
                                        className="h-25",
                                        width=4,
                                    ),
                                    dbc.Col(
                                        
                                        [
                                            html.H3("idk"),
                                            html.Br(),
                                            html.H3("maybe an explanation?"),
                                            html.Br(),
                                        ],
                                        style={"textAlign": "center"},
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

tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 4!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

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
    ],
    style={"padding": 50},
)

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
                dbc.Tab(tab4_content, label="Musicality: (placeholder)"),
            ]
        ),
    ],
    style={"padding": 50},
)


app.layout = html.Div([
    # represents the browser address bar and doesn't render anything
    dcc.Location(id='url', refresh=False),

    # content will be rendered in this element
    html.Div(id='page-content')
])

@callback(
        Output('page-content', 'children'), 
        Input('url', 'pathname')
        )
def display_page(pathname):
    if pathname == "/result":
        return layout_result
    else:
        return layout_search

@callback(
    [
        Output("artist", "children"),
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
def display_page(pathname):
    if pathname == "/result":
        themes = []
        polarity_verdict = 'o'
        subjectivity_rating = '1.0'
        artist = 'Search'

        with open(os.path.join(dir, './Figures/artist.txt'), encoding='utf-8') as f:
            artist = f.read().rstrip()

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

        return artist, dbc.ListGroup([dbc.ListGroupItem(x) for x in themes], className="mb-2",), word_cloud, polarities_dist, subjectivities_dist, subjectivity_rating, polarity_verdict#, {"display": "block"}
    return 'Going Back...', None, None, None, None, None, None#, {"display": "none"}


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

    return (
        "Showing Results...",
        None,
        "/result"
    )

if __name__ == "__main__":
    app.run_server(debug=True)
