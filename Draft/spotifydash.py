#connecting genius & spotify
from search_artist import word_cloud, get_lyrics

#Dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
from PIL import Image
from textblob import TextBlob

import app
spt_img = Image.open("Draft\\spotify.png")
image_path = "Draft\\sample_TaylorSwift_WordCloud.png"
pil_img = Image.open(image_path)

app = Dash(external_stylesheets=[dbc.themes.UNITED])
default_color = default_color = 'rgb(121, 41, 82)'

app.layout = html.Div([
    dbc.Card(dbc.Row(html.H1(children='Spotify Dashboard', style={'textAlign':'center', 'color': 'green'}), html.Img(src=spt_img)), body=True),
    html.Br(),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                html.Div([
                    #Search Artist's name
    
                    html.H4(children= "Enter Artist's name Below"),
                    dbc.Row([
                        html.Div([html.Img(src=pil_img), "Name: ", dcc.Input(id='query_artist', value='Taylor Swift', type='text'), html.Button('Submit', id='submit_artist', n_clicks=0)])
                    ], align='right'),
                    html.Br(),
                    html.H4(children ="wordcloud"),
                    html.Img(src=pil_img),
                    #html.Img(id='word_cloud', src=pil_img),
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
                                #ch
                    )
                ])
            ])
        ])
    )
], style={'padding': 100, 'border': 'solid'})

#Assume search_artist has the function that process the image & analysis.
#

"""
@callback(
    Output("word_cloud", "src"),
    Input("query_artist", "value"),
    Input("submit_artist", "n_clicks"),
)
def get_word_cloud(query_artist,  n_clicks):
    if n_clicks == 0:
        return None
    lyrics = get_lyrics(query_artist)
    img_wordcloud = word_cloud(lyrics)
    return img_wordcloud

#
@callback(
    Output("table", "data"),
    Input("query_artist", "value"),
    Input("submit_artist", "n_clicks"),
)
def update_table(input_keyword, n_clicks):
    if n_clicks == 0:
        return dash.no_update
    result = #analysis result
    return result
"""

if __name__ == '__main__':
    app.run_server(debug=True)


