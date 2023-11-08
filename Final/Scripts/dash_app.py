import os

# Dash
import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Import Modules
import base64
import genius
from PIL import Image
import time

dir = os.path.dirname(__file__)

# Text Formatting
text_style = {"text-align": "center"}
image_style = {"height": "auto", "width": "100%"}

app = app = Dash(external_stylesheets=[dbc.themes.MINTY])
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
        dbc.Spinner(
            html.Div(id="loading_output"),
            color="success",
            spinner_style={"width": "3rem", "height": "3rem"},
        ),
    ],
    className="mb-3",
)

form = dbc.Form([artist_input])

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
                                        html.H3("Overall Polarity"),
                                        html.Br(),
                                        html.H1(id="polarity_verdict"),
                                        html.Br(),
                                    ],
                                    style={"textAlign": "center"},
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.H3("Common Topics"),
                                        html.Br(),
                                        html.Div(id="themes"),
                                        html.Br(),
                                    ],
                                    style={"textAlign": "center"},
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.H3("Subjectivity Rating"),
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
                                        html.H3("Word Cloud"),
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
                                        html.H3("Lyric Polarity Distribution"),
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
                "This is the content of the second section", title="Musical Analysis"
            ),
        ],
        flush=True,
        id="element-to-hide",
        start_collapsed=True,
    ),
)


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


@callback(
    [
        Output("query_artist_lyrics", "children"),  # 'lyrics lyrics lyrics'
        Output("themes", "children"),  # ['reputation', 'dream', 'problem']
        Output("word_cloud", "src"),  # PIL image
        Output("polarities_dist", "src"),  # PIL image
        Output("subjectivities_dist", "src"),  # PIL image
        Output("subjectivity_rating", "children"),  # 3.5 (one decimal)
        Output(
            "polarity_verdict", "children"
        ),  # '---', '--', '-', 'o', '+', '++', '+++'
        Output("loading_output", "children"),
        Output("element-to-hide", component_property="style"),
    ],
    [State("query_artist", "value"), Input("submit_artist", "n_clicks")],
)
def process(query_artist, n_clicks):
    if n_clicks == 0:
        return None, None, None, None, None, None, None, None, {"display": "none"}

    n_clicks = 0

    # generates word_cloud.png, polarities_dist.png, subjectivities_dist.png
    try:
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
            "Artist Analysis",
            html.Ul([html.H4(x) for x in themes], style={"padding": 0}),
            img_wordcloud,
            img_polarities,
            img_subjectivities,
            subjectivity_rating,
            polarity_verdict,
            None,
            {"display": "block"},
        )

    # Exception for incorrect inputs
    except Exception as e:
        return (
            "Loading...",
            "Error. Please check the artist's name and try again.",
            None,
            None,
            None,
            None,
            None,
            None,
            {"display": "block"},
        )


if __name__ == "__main__":
    app.run_server(debug=True)
