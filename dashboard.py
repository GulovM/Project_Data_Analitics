import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime as dtime
from etl import extract_data, transform_data

# Извлечение и трансформация данных
athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = extract_data()
athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = transform_data(athlete_medals, country_medal_tally, yearly_medal_count, top_athletes)

app = dash.Dash(__name__)

# Устанавливаем минимальные и максимальные даты
min_date = yearly_medal_count['year'].min()
max_date = yearly_medal_count['year'].max()
years = yearly_medal_count['year'].dt.year.unique().tolist()

app.layout = html.Div([
    html.H1("Olympic Dashboard"),

    # Компоненты для athlete_medals
    html.Div([
        html.H2("Athlete Medals"),
        html.Label('Select Sport'),
        dcc.Dropdown(
            id='sport-dropdown',
            options=[{'label': 'All Sports', 'value': 'All Sports'}] + 
                    [{'label': sport, 'value': sport} for sport in athlete_medals['sport'].unique()],
            value='All Sports'
        ),
        html.Label('Select Medal Type'),
        dcc.RadioItems(
            id='medal-radioitems',
            options=[
                {'label': 'Gold', 'value': 'Gold'},
                {'label': 'Silver', 'value': 'Silver'},
                {'label': 'Bronze', 'value': 'Bronze'},
                {'label': 'All', 'value': 'All'}
            ],
            value='All'
        ),
        dcc.Graph(id='athlete-medals-graph'),
        html.H2("Athlete Medals Table"),
        dash_table.DataTable(
            id='athlete-medals-table',
            columns=[{'name': i, 'id': i} for i in athlete_medals.columns],
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}
        ),
    ]),

    # Компоненты для country_medal_tally
    html.Div([
        html.H2("Country Medal Tally"),
        dcc.Graph(id='country-medal-graph'),
        dcc.Graph(id='country-medal-pie'),
        html.H2("Country Medal Tally Table"),
        dash_table.DataTable(
            id='country-medal-tally-table',
            columns=[{'name': i, 'id': i} for i in country_medal_tally.columns],
            data=country_medal_tally.to_dict('records'),
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}
        ),
    ]),

    # Компоненты для yearly_medal_count
    html.Div([
        html.H2("Yearly Medal Count"),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
            display_format='YYYY-MM-DD'
        ),
        dcc.RangeSlider(
            id='year-slider',
            min=years[0],
            max=years[-1],
            step=1,
            value=[years[0], years[-1]],
            marks={y: str(y) for y in years}
        ),
        dcc.Graph(id='year-medal-graph'),
        dcc.Graph(id='year-medal-bar'),
        html.H2("Yearly Medal Count Table"),
        dash_table.DataTable(
            id='yearly-medal-count-table',
            columns=[{'name': i, 'id': i} for i in yearly_medal_count.columns],
            data=yearly_medal_count.to_dict('records'),
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}
        ),
    ]),

    # Компоненты для top_athletes
    html.Div([
        html.H2("Top Athletes"),
        dcc.Graph(id='top-athletes-graph'),
        html.H2("Top Athletes Table"),
        dash_table.DataTable(
            id='top-athletes-table',
            columns=[{'name': i, 'id': i} for i in top_athletes.columns],
            data=top_athletes.to_dict('records'),
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}
        ),
    ]),
])

# Обновление графика athlete_medals в зависимости от выбранного спорта и типа медали
@app.callback(
    Output('athlete-medals-graph', 'figure'),
    [Input('sport-dropdown', 'value'),
     Input('medal-radioitems', 'value')]
)
def update_athlete_medals_graph(selected_sport, selected_medal):
    filtered_df = athlete_medals.copy()
    
    if selected_sport != 'All Sports':
        filtered_df = filtered_df[filtered_df['sport'] == selected_sport]
    
    if selected_medal != 'All':
        filtered_df = filtered_df[filtered_df['medal'] == selected_medal]
    
    medal_counts = filtered_df.groupby(['sport', 'medal']).size().reset_index(name='count')
    
    fig = px.bar(
        data_frame=medal_counts, 
        x='sport', 
        y='count', 
        color='medal', 
        title='Medals by Sport and Medal Type',
        labels={'count': 'Number of Medals'}
    )
    return fig

# Обновление таблицы athlete_medals в зависимости от выбранного спорта и типа медали
@app.callback(
    Output('athlete-medals-table', 'data'),
    [Input('sport-dropdown', 'value'),
     Input('medal-radioitems', 'value')]
)
def update_athlete_medals_table(selected_sport, selected_medal):
    filtered_df = athlete_medals.copy()
    
    if selected_sport != 'All Sports':
        filtered_df = filtered_df[filtered_df['sport'] == selected_sport]
    
    if selected_medal != 'All':
        filtered_df = filtered_df[filtered_df['medal'] == selected_medal]
    
    return filtered_df.to_dict('records')

# Обновление диапазона дат в DatePickerRange в зависимости от RangeSlider
@app.callback(
    [Output('date-picker-range', 'start_date'),
     Output('date-picker-range', 'end_date')],
    Input('year-slider', 'value')
)
def update_date_picker_range(year_range):
    start_date = dtime(year_range[0], 1, 1)
    end_date = dtime(year_range[1], 12, 31)
    return start_date.date(), end_date.date()

# Обновление графиков yearly_medal_count в зависимости от выбранного диапазона дат
@app.callback(
    [Output('year-medal-graph', 'figure'),
     Output('year-medal-bar', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_year_medal_graphs(start_date, end_date):
    filtered_df = yearly_medal_count.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['year'] >= start_date) & (filtered_df['year'] <= end_date)]
    
    yearly_medals = filtered_df.groupby('year').size().reset_index(name='count')
    
    line_fig = px.line(yearly_medals, x='year', y='count', title='Medals by Year')
    bar_fig = px.bar(yearly_medals, x='year', y='count', title='Medals by Year')
    
    return line_fig, bar_fig

# Обновление графика top_athletes в зависимости от выбранного спорта
@app.callback(
    Output('top-athletes-graph', 'figure'),
    Input('sport-dropdown', 'value')
)
def update_top_athletes_graph(selected_sport):
    if selected_sport == 'All Sports':
        filtered_df = top_athletes
    else:
        filtered_df = top_athletes[top_athletes['sport'] == selected_sport]
    
    fig = px.bar(filtered_df, x='name', y='total_medals', color='sex', title=f'Top Athletes in {selected_sport}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
