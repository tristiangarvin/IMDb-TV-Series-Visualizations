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

df_show = pd.read_csv('show_overall.csv')

#df_show['Total_Rating'] = df_show.agg('{0[Title]}: {0[Rating_O]}'.format, axis=1)

df = df.join(df_show.set_index('Title'), on='Title')

df['Episodes'] = df.groupby(['Title']).cumcount() + 1

dropdown_show = dcc.Dropdown(
    id="dropdown-show",
    options=[{"label": show, "value": show}
             for show in df.Title.unique()],
    multi=False,
    value='Breaking Bad',
    clearable=False,
)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Top 250 TV Series Ratings on IMDB', className='pt-5 pb-2'),
            dropdown_show,
            dcc.Graph(id='ratings-chart', figure={},  className="pt-5", responsive=True, style={'min-height': '500px'}),
        ], lg=12)
    ],),
    dbc.Row([
        dbc.Col([
            html.H2(id='show-title'),
            html.P(id='avg-rating'),
            html.P(id='show-difference'),
        ], lg=6, ),
        dbc.Col([

        ],),
    ],),
],)

@app.callback(
    [
            Output('ratings-chart','figure'),
            Output('show-title','children'),
            Output('show-difference','children'),
    ],
    [
            Input('dropdown-show', 'value'),
    ]
    )
def update_layout(show):
    df2 = df[df['Title'] == show]
    show_title = df2['Title'].iloc[0] # first item in PD series
    show_rating = df2['Rating_Overall'].iloc[0] # first item in PD series
    

    fig = px.line(df2, x='Episodes', y='Rating', markers=True, line_shape='spline', title="IMDb Rating by Episode",)
    fig.update_yaxes(range=[0,10], dtick=1, showgrid=False, zeroline=True, ticksuffix = "  ")
    fig.update_xaxes(showgrid=False, zeroline=True, rangemode="tozero")
    fig.update_traces(textposition="bottom center", line_color='#F5C518')


    high = df2[df2.Rating == df2.Rating.max()]
    low = df2[df2.Rating == df2.Rating.min()]

    highscore = high['Rating'].iloc[0].item()
    lowscore = low['Rating'].iloc[0].item()

    difference = highscore - lowscore
    difference = round(difference, 1)

    selected_show = f'{show_title}: {show_rating}'
    rating_difference = f'Difference between highest and lowest rated episodes: {difference}'

    fig.add_annotation(text='Highest Rated Ep: ' + str(highscore), y=high.iloc[-1]['Rating'], x=high.iloc[-1]['Episodes'], arrowcolor='white')
    fig.add_annotation(text='Lowest Rated Ep: ' + str(lowscore), y=low.iloc[0]['Rating'], x=low.iloc[0]['Episodes'], arrowcolor='white', font=dict(color="#E85669"), ay=30, ax=5)

    fig.update_layout(
            {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            },
            showlegend=False,
            autosize=False,
            margin={'t':60, 'l': 20, 'b': 20, 'r': 20},
            font_color="white",
            hovermode="x",
        )


    return fig, selected_show, rating_difference

server = app.server

if __name__ == "__main__":
    while True:
        app.run_server(debug=True)