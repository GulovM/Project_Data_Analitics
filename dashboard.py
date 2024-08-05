import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from etl import extract_data, transform_data

# Извлечение и трансформация данных
athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = extract_data()
athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = transform_data(athlete_medals, country_medal_tally, yearly_medal_count, top_athletes)

# Создание графиков
fig1 = px.histogram(athlete_medals, x='sport', color='medal', title='Medals by Sport')
fig2 = px.bar(country_medal_tally, x='country', y=['gold', 'silver', 'bronze'], title='Country Medal Tally')
fig3 = px.line(yearly_medal_count, x='year', y='total_medals', title='Yearly Medal Count')
fig4 = px.scatter(top_athletes, x='sport', y='total_medals', color='name', title='Top Athletes by Sport')

# Создание дашборда
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Olympics Dashboard'),
    dcc.Graph(
        id='medals-by-sport',
        figure=fig1
    ),
    dcc.Graph(
        id='country-medal-tally',
        figure=fig2
    ),
    dcc.Graph(
        id='yearly-medal-count',
        figure=fig3
    ),
    dcc.Graph(
        id='top-athletes',
        figure=fig4
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
