import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

#app = dash.Dash(__name__)
app = Dash(external_stylesheets=[dbc.themes.UNITED])
#default_color = default_color = 'rgb(121, 41, 82)'

app.layout = html.Div([
    dbc.Card(dbc.Row(html.H1(children='Spotify Dashboard', style={'textAlign':'center', 'color': 'green'})), body=True),
    html.Br(),

    #Widget 1: Searching artist name
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                html.Div([
                    html.H4(children= "Enter Artist's name Below"),
                    dbc.Row([
                        html.Div(["Name: ", dcc.Input(id='Artist_name', value='Taylor Swift', type='text')])
                    ], align='right'),
                    html.Br(),
                ])
            ])
        ])
    )
], style={'padding': 100, 'border': 'solid'})

if __name__ == '__main__':
    app.run_server(debug=True)
