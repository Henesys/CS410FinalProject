import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

#app = dash.Dash(__name__)
app = Dash(external_stylesheets=[dbc.themes.UNITED])
default_color = default_color = 'rgb(121, 41, 82)'


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
                        html.Div(["Name: ", dcc.Input(id='Artist_name', value='Taylor Swift', type='text')])
                    ], align='right'),
                    html.Br(),
                    html.Div(["Analysis"]),
                    html.Br(),
                    dash_table.DataTable(
                                columns = [{'name':'Artist Name','id':'name'}, {'name':'song','id':'sname'}, 
                                        {'name':'analysis','id':'any'}],
                                id='faculty_university_table',
                                fixed_rows={'headers': True},
                                style_table={'overflowY':'auto'},
                                style_data={'height':'auto','minWidth':'140px','width':'140px','maxWidth':'200px',
                                            'color':default_color,'border':'1px solid {}'.format(default_color)},
                                style_cell_conditional=[{'if': {'column_id':'uname'}, 'width':'150%'}],
                                style_header={'backgroundColor':default_color,'color':'white'}
                    )
                ])
            ])
        ])
    )
], style={'padding': 100, 'border': 'solid'})

if __name__ == '__main__':
    app.run_server(debug=True)
