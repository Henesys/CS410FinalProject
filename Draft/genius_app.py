import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import search_artist
from PIL import Image
import time

app = app = Dash(external_stylesheets=[dbc.themes.MINTY])
default_color = default_color = 'rgb(121, 41, 82)'
spt_img = Image.open("spotify.png")

artist_input = html.Div(
    [
        dbc.Label("Enter Artist's Name Below", html_for="query_artist"),
        dbc.Input(type="text", id="query_artist", placeholder="Enter Artist Name", style={"width": "50%", "text-align":"center"}),
        dbc.Col(dbc.Button("Search", color="primary", id='submit_artist', n_clicks=0, style={"width": "50%"}), width="auto"),
        html.Br(),
        dbc.Spinner(html.Div(id="loading_output"), color="success", spinner_style={"width": "3rem", "height": "3rem"}),
    ],
    className="mb-3",
)

form = dbc.Form([artist_input])

accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Card([
                html.Div(id="polarity_verdict"),
                html.Div(id="themes"),
                html.Div(id="subjectivity_rating"),
                html.Img(id="word_cloud", style={'height':'auto', 'width':'50%'}),
                html.Img(id="polarities_dist"),
                html.Img(id="subjectivities_dist")
                ]), title="Lyrical Analysis"
            ),
            dbc.AccordionItem(
                "This is the content of the second section", 
                title="Musical Analysis"
            ),
        ],
        flush=True,
        id='element-to-hide',
        start_collapsed=True,
    ),
)


app.layout = html.Div(
    [
        dbc.Card(dbc.Row([html.Img(src=spt_img, style={'height':'64px', 'width':'auto'}), 
                        dbc.Col(html.H1(children='Artist Dashboard', style={'textAlign':'center', 'color': "green", 'vertical-align':'center'})),  
                        html.Img(src=spt_img, style={'height':'64px', 'width':'auto'})])),
        html.Br(),
        html.Center(form),
        html.H2(id="query_artist_lyrics", style={'textAlign':'center', 'vertical-align':'center'}),
        html.Br(),
        html.Center(accordion),
    ]
    , style={'padding': 50}
)


@callback([
    Output("query_artist_lyrics", "children"),  # 'lyrics lyrics lyrics'
    Output("themes", "children"),               # ['reputation', 'dream', 'problem']
    Output("word_cloud", "src"),                # PIL image
    Output("polarities_dist", "src"),           # PIL image
    Output("subjectivities_dist", "src"),       # PIL image
    Output("subjectivity_rating", "children"),  # 3.5 (one decimal)
    Output("polarity_verdict", "children"),      # '---', '--', '-', 'o', '+', '++', '+++'
    Output("loading_output", "children"),
    Output("element-to-hide", component_property='style')
    ],
    [Input("query_artist", "value"),
    Input("submit_artist", "n_clicks")]
)
def process(query_artist, n_clicks):
    if n_clicks == 0:
        return None, None, None, None, None, None, None, None, {'display': 'none'}

    n_clicks = 0

    # generates word_cloud.png, polarities_dist.png, subjectivities_dist.png
    all_songs, themes, img_wordcloud, img_polarities, img_subjectivities, subjectivity_rating, polarity_verdict = search_artist.process_artist_lyrics(query_artist)

    return "Artist Analysis Breakdown", themes, img_wordcloud, img_polarities, img_subjectivities, subjectivity_rating, polarity_verdict, None, {'display': 'block'}


if __name__ == '__main__':
    app.run_server(debug=True)
