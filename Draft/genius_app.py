import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import search_artist
from PIL import Image

"""
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(dcc.Input(id='query_artist', type='text', placeholder="Insert Artist Name", debounce=True, minLength=1)),
        html.Button('Submit', id='submit_artist', n_clicks=0),
        html.Br(),
        html.Div(id="polarity_verdict"),
        html.Img(id="word_cloud"),
        html.Img(id="polarities_dist"),
        html.Img(id="subjectivities_dist"),
        html.Div(id="query_artist_lyrics"),
    ]
)
"""
app = Dash(external_stylesheets=[dbc.themes.UNITED])
default_color = default_color = 'rgb(121, 41, 82)'
spt_img = Image.open("spotify.png")

app.layout = html.Div([
    dbc.Card(dbc.Row([html.Img(src=spt_img, style={'height':'7%', 'width':'7%'}), dbc.Col(html.H1(children='Spotify Dashboard', style={'textAlign':'center', 'color': 'green'})),  html.Img(src=spt_img, style={'height':'7%', 'width':'7%'})])),
    html.Br(),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                html.Div([
                    #Search Artist's name
    
                    html.H4(children="Enter Artist's name Below"),
                    dbc.Row([
                        html.Div([html.Img(src=spt_img, style={'height':'7%', 'width':'7%'}), "Name: ", dcc.Input(id='query_artist', type='text', placeholder="Insert Artist Name", debounce=True, minLength=1), html.Button('Submit', id='submit_artist', n_clicks=0)])
                    ], align='right'),
                    html.Br(),
                    html.H4(children="wordcloud"),
                    html.Img(src="word_cloud"),
                    html.Div(id="polarity_verdict"),
                    html.Div(id="themes"),
                    html.Img(id="word_cloud"),
                    html.Img(id="polarities_dist"),
                    html.Img(id="subjectivities_dist"),
                    html.Div(id="subjectivity_rating"),
                    html.Div(id="query_artist_lyrics"),
                    html.Br(),
                    dash_table.DataTable(id='table',
                                columns = [{'name':'Artist Image','id':'image'}, 
                                        {'name':'analysis','id':'any'}],
                                fixed_rows={'headers': True},
                                style_table={'overflowY':'auto'},
                                style_data={'height':'auto','minWidth':'140px','width':'140px','maxWidth':'200px',
                                            'color':default_color,'border':'1px solid {}'.format(default_color)},
                                style_cell_conditional=[{'if': {'column_id':'uname'}, 'width':'150%'}],
                                style_header={'backgroundColor':default_color,'color':'green'}
                    )
                ])
            ])
        ])
    )
], style={'padding': 100, 'border': 'solid'})


@callback([
    Output("query_artist_lyrics", "children"),  # 'lyrics lyrics lyrics'
    Output("themes", "children"),               # ['reputation', 'dream', 'problem']
    Output("word_cloud", "src"),                # PIL image
    Output("polarities_dist", "src"),           # PIL image
    Output("subjectivities_dist", "src"),       # PIL image
    Output("subjectivity_rating", "children"),  # 3.5 (one decimal)
    Output("polarity_verdict", "children")      # '---', '--', '-', 'o', '+', '++', '+++'
    ],
    [Input("query_artist", "value"),
    Input("submit_artist", "n_clicks")]
)
def process(query_artist, n_clicks):
    if n_clicks == 0:
        return None, None, None, None, None, None, None

    n_clicks = 0

    # generates word_cloud.png, polarities_dist.png, subjectivities_dist.png
    all_songs, themes, img_wordcloud, img_polarities, img_subjectivities, subjectivity_rating, polarity_verdict = search_artist.process_artist_lyrics(query_artist)

    return all_songs, themes, img_wordcloud, img_polarities, img_subjectivities, subjectivity_rating, polarity_verdict

if __name__ == '__main__':
    app.run_server(debug=True)
