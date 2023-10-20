from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.UNITED])

app.layout = html.Div([
    html.H1(children = 'SPOTIFY DASHBOARD',style={'textAlign': 'center', 'fontFamily': 'fantasy', 'fontSize': 50, 'color': 'blue'}),
    html.Div(dcc.Input(type='text')),
    html.Button('Enter'),
], style={'padding': 100, 'border': 'solid'})

if __name__ == '__main__':
    app.run_server(debug=True)