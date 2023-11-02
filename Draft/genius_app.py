import dash
from dash import Dash, dcc, html, Input, Output, callback
import search_artist
from PIL import Image

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

@callback([
    Output("query_artist_lyrics", "children"),
    Output("word_cloud", "src"),
    Output("polarities_dist", "src"),
    Output("subjectivities_dist", "src"),
    Output("polarity_verdict", "children")
    ],
    [Input("query_artist", "value"),
    Input("submit_artist", "n_clicks")]
)
def get_lyrics(query_artist, n_clicks):
    if n_clicks == 0:
        return None, None, None, None, None

    n_clicks = 0

    # generates word_cloud.png, polarities_dist.png, subjectivities_dist.png
    all_songs, img_wordcloud, img_polarities, img_subjectivities, polarity_verdict = search_artist.get_lyrics(query_artist)

    return all_songs, img_wordcloud, img_polarities, img_subjectivities, polarity_verdict

if __name__ == '__main__':
    app.run_server(debug=True)
