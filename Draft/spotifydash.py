#connecting genius & spotify
#from search_artist.py import process_artist_lyrics

#Dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
from PIL import Image
from textblob import TextBlob
from os import path
import app
spt_img = Image.open("Draft\\spotify.png")

lines_list = open("ArtistLyrics//artists.txt" ).read().splitlines()

app = Dash(external_stylesheets=[dbc.themes.UNITED])
default_color = default_color = 'rgb(121, 41, 82)'

app.layout = html.Div([
    dbc.Card(dbc.Row([html.Img(src=spt_img, style={'height':'7%', 'width':'7%'}), dbc.Col(html.H1(children='Spotify Dashboard', style={'textAlign':'center', 'color': 'green'})),  html.Img(src=spt_img, style={'height':'7%', 'width':'7%'})])),
    html.Br(),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                html.Div([
                    #Search Artist's name

                    html.H4(children= "Enter Artist's name Below"),
                    dbc.Row([
                        html.Div(["Name: ", dcc.Input(id='query_artist', value= "Taylor Swift", type='text'), html.Button('Submit', id='submit_artist', n_clicks=0)])
                    ], align='right'),
                    html.H4(children ="Artist"),
                    #html.Img(src = Image.open("Draft//taylorswift_image.png")),
                    html.Img(id='image',style={'height':'=50%', 'width':'20%'}),
                    html.Br(),
                    html.H4(children ="wordcloud"),
                    html.Img(id='word_cloud',style={'height':'=50%', 'width':'50%'}),
                    html.Br(),
                    html.H4(children ="Analysis"),
                    dcc.Textarea(id='analysis', value='artist analysis', style={'width': '100%', 'height': 300})
                ])
            ])
        ])
    )
], style={'padding': 100, 'border': 'solid'})



@callback(
    Output("image", "src"), #artist image
    Output("word_cloud", "src"), #word cloud
    #Output("Analysis", value), 
    Input("submit_artist", "n_clicks"),
    State("query_artist", "value")
)
def get_results(n_clicks, query_artist):
    artist = query_artist.lower().replace(" ", "")
    if n_clicks == 0:
        return None
    if artist in lines_list:
        return Image.open("ArtistLyrics//" + artist + "_image" + "." + "jpg"),  Image.open("ArtistLyrics//" + artist + "_wordCloud" + "." + "png")
    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)

'''
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
'''

'''
def get_results(query_artist,  n_clicks):
    if n_clicks == 0:
        return None
    artist = query_artist.lower().replace(" ", "")
    if artist in lines_list:
        Artist_image = "ArtistLyrics//" + artist + "_image" + "." + "jpg"
    return Image.open(Artist_image)
'''