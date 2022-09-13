from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],  # bootstrap theme settings
           meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1.2, minimum-scale=0.5,"}
]
)

df = pd.read_csv('imdb_top_250_series_episode_ratings.csv')
df['Episodes'] = df.groupby(['Title']).cumcount() + 1

df['Average'] = df.groupby('Title')['Rating'].transform('mean')

dropdown_show = dcc.Dropdown(
    id="dropdown-show",
    options=[{"label": show, "value": show}
             for show in sorted(df.Title.unique())],
    multi=False,
    value='Breaking Bad',
    clearable=False,
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('IMDB Ratings'),
            dropdown_show,
            dcc.Graph(id='ratings-chart', figure={})
        ], lg=12)
    ],),
],)

@app.callback(Output('ratings-chart','figure'),
              Input('dropdown-show', 'value'))
def update_layout(show):
    df2 = df[df['Title'] == show]
    fig = px.line(df2, x='Episodes', y='Rating', markers=True, line_shape='spline',)
    fig.update_yaxes(range=[1,10], dtick=1)
    fig.update_traces(textposition="bottom right")

    return fig

server = app.server

if __name__ == "__main__":
    while True:
        app.run_server(debug=True)