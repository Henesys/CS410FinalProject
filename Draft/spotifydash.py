#connecting genius & spotify
#from Draft.search_artist import * #from Marcia

#Dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import os
from PIL import Image
from textblob import TextBlob


import app

app = Dash(external_stylesheets=[dbc.themes.UNITED])
default_color = default_color = 'rgb(121, 41, 82)'


image_path = r'C:\changhun\UIUC\CS410\CS410FinalProject\Draft'

app.layout = html.Div([
    dbc.Card(dbc.Row(html.H1(children='Spotify Dashboard', style={'textAlign':'center', 'color': 'green'})), body=True),
    html.Br(),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                html.Div([
                    #Search Artist's name
                    html.H4(children= "Enter Artist's name Below"),
                    dbc.Row([
                        html.Div(["Name: ", dcc.Input(id='query_artist', value='Enter Here', type='text'), html.Button('Submit', id='submit_artist', n_clicks=0)])
                    ], align='right'),
                    html.Br(),

                    html.Img(src=image_path),
                    html.Br(),
                    html.H4(children ="wordcloud"),
                    dash_table.DataTable(
                                columns = [{'name':'Artist Image','id':'image'}, {'name':'song','id':'sname'}, 
                                        {'name':'analysis','id':'any'}],
                                id='faculty_university_table',
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

""""
@callback(
    #Output
    #input(artist_name)
)



def update_table(input_keyword, n_result):
    if not input_keyword:
        return dash.no_update
    result = #analysis result
    return result
"""

if __name__ == '__main__':
    app.run_server(debug=True)
