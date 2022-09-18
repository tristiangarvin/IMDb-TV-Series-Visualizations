from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],  # bootstrap theme settings
           meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1.2, minimum-scale=0.5,"}
]
)

df = pd.read_csv('imdb_top_250_series_episode_ratings.csv')

df['all_low'] = df.groupby(['Title'])['Rating'].transform('min')
df['all_high'] = df.groupby(['Title'])['Rating'].transform('max')
df['diff'] = df['all_high'] - df['all_low']
diff_avg = df['diff'].mean()
diff_avg = round(diff_avg, 2)

diff_max = df['diff'].max()
diff_min = df['diff'].min()
diff_min
df['diff']

diff_min

df.groupby(['Title'])['Rating'].min()

lowest = df.iloc[df['diff'].idxmin()]
lowest = lowest.values[7]
lowest = round(lowest, 2)

lowest_title = df.iloc[df['diff'].idxmin()]
lowest_title = lowest_title.values[4]
lowest_title

highest = df.iloc[df['diff'].idxmax()]
highest = highest.values[7]
highest = round(highest, 2)

highest_title = df.iloc[df['diff'].idxmax()]
highest_title = highest_title.values[4]
highest_title

type(lowest)


df_show = pd.read_csv('show_overall.csv')

show_avg = df_show['Rating_Overall'].mean()

show_avg = round(show_avg, 1)


std_all = df['Rating'].std()
std_all = round(std_all, 2)

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
            html.Img(src='assets/logo.png', className='mx-auto d-block img-fluid pt-2')
        ], lg=2),
        dbc.Col([
            html.H1('Top 250 TV Series Episode Ratings', className='pt-5 pb-2'),
        ], lg=10, className="my-auto")
    ],),
    dbc.Row([
        dbc.Label("Series (Sorted by Overall IMDb Rating)"),
        dropdown_show,
        dcc.Graph(id='ratings-chart', figure={},  className="pt-5", responsive=True, style={'min-height': '500px'}),
    ], className='pb-2'),
    dbc.Row([
        dbc.Col([
            html.H2([f'Ratings Across All Shows: ', html.B(f'{show_avg}', className="text-yellow")]),
            html.P([f'Average difference between highest and lowest rated episodes: ', html.B(f'{diff_avg}', className="text-yellow")]),
            html.P([f'Average Standard Deviation: ', html.B(f'{std_all}', className="text-yellow")]),
            html.P([f'Smallest difference between highest and lowest rated episodes: ', html.B(f'{lowest_title} {lowest}', className="text-yellow")],),
            html.P([f'Largest difference between highest and lowest rated episodes: ', html.B(f'{highest_title} {highest}', className="text-yellow")],),
        ], lg=7,),
        dbc.Col([
            html.H2(id='show-title'),
            html.P(id='show-difference'),
            html.P(id='show-std'),
        ], lg=5, ),
    ],),
],)

@app.callback(
    [
            Output('ratings-chart','figure'),
            Output('show-title','children'),
            Output('show-difference','children'),
            Output('show-std','children'),
    ],
    [
            Input('dropdown-show', 'value'),
    ]
    )
def update_layout(show):
    df2 = df[df['Title'] == show]
    show_title = df2['Title'].iloc[0] # first item in PD series
    show_rating = df2['Rating_Overall'].iloc[0] # first item in PD series

    std = df2['Rating'].std()
    std = round(std, 2)
    deviation = f'Standard Deviation: {std}'
    

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


    return fig, selected_show, rating_difference, deviation

server = app.server

if __name__ == "__main__":
    while True:
        app.run_server(debug=True)