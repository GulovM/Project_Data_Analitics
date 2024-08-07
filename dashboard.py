import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
from etl import extract_data, transform_data


# Извлечение и трансформация данных
athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = extract_data()
athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = transform_data(athlete_medals, country_medal_tally, yearly_medal_count, top_athletes)

# Определение минимальных и максимальных годов для Yearly Medal Count
min_date_ymc = yearly_medal_count['year'].min()
max_date_ymc = yearly_medal_count['year'].max()
years_ymc = yearly_medal_count.sort_values(by='year')['year'].unique().tolist()

app = dash.Dash(__name__)
server = app.server
# Layout приложения
app.layout = html.Div([
    html.H1("Olympic Dashboard"),

    # Секция для графика и таблицы Athlete Medals
    html.Div([
        html.H2("Athlete Medals"),
        html.Label('Select Sport'),
        dcc.Dropdown(
            id='sport-dropdown',
            options=[{'label': sport, 'value': sport} for sport in athlete_medals['sport'].unique()],
            placeholder='Select a sport'
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
        dcc.Graph(id='athlete-medals-graph'),  # График для отображения медалей спортсменов
        html.H2("Athlete Medals Table"),
        dash_table.DataTable(
            id='athlete-medals-table',
            columns=[{'name': i, 'id': i} for i in athlete_medals.columns],
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}  # Таблица для отображения медалей спортсменов
        ),
    ]),

    # Секция для графика и таблицы Country Medal Tally
    html.Div([
        html.H2("Country Medal Tally"),
        html.Label('Select Country'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in country_medal_tally['country'].unique()],
            placeholder='Select a country'
        ),
        dcc.Graph(id='country-medal-tally-graph'),  # График для отображения медального зачета по странам
        html.H2("Country Medal Tally Table"),
        dash_table.DataTable(
            id='country-medal-tally-table',
            columns=[{'name': i, 'id': i} for i in country_medal_tally.columns],
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}  # Таблица для отображения медального зачета по странам
        ),
    ]),

    # Секция для графика и компоненты Yearly Medal Count
    html.Div([
        html.H2("Yearly Medal Count"),
        html.Label('Select Year'),
        dcc.RangeSlider(
            id='year-slider',
            min=min_date_ymc,
            max=max_date_ymc,
            step=1,
            value=[min_date_ymc, max_date_ymc],
            marks={y: str(y) for y in years_ymc}  # Слайдер для выбора диапазона годов
        ),
        dcc.Graph(id='yearly-medal-count-graph'),  # График для отображения ежегодного медального зачета
        html.H2("Yearly Medal Count"),
        dash_table.DataTable(
            id='yearly-medal-count-table',
            columns=[{'name': i, 'id': i} for i in yearly_medal_count.columns],
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}  # Таблица для отображения ежегодного медального зачета
        ),
    ]),
    
    # Новая секция для графика и таблицы Top Athletes
    html.Div([
        html.H2("Top Athletes"),
        html.Label('Select Sport'),
        dcc.Dropdown(
            id='top-athletes-sport-dropdown',
            options=[{'label': sport, 'value': sport} for sport in top_athletes['sport'].unique()],
            placeholder='Select a sport'
        ),
        dcc.Graph(id='top-athletes-graph'),  # График для отображения топовых спортсменов
        html.H2("Top Athletes Table"),
        dash_table.DataTable(
            id='top-athletes-table',
            columns=[{'name': i, 'id': i} for i in top_athletes.columns],
            page_size=10,
            style_table={'height': '300px', 'overflowY': 'auto'}  # Таблица для отображения топовых спортсменов
        ),
    ])
])

# Колбэк для обновления графика athlete_medals в зависимости от выбранного спорта и типа медали
@app.callback(
    Output('athlete-medals-graph', 'figure'),
    [Input('sport-dropdown', 'value'),
     Input('medal-radioitems', 'value')]
)
def update_athlete_medals_graph(selected_sport, selected_medal):
    # Фильтрация данных на основе выбранного спорта и типа медали
    filtered_df = athlete_medals.copy(deep=True)
    
    if selected_sport:
        filtered_df = filtered_df[filtered_df['sport'] == selected_sport]
    
    if selected_medal != 'All':
        filtered_df = filtered_df[filtered_df['medal'] == selected_medal]
    
    medal_counts = filtered_df.groupby(['sport', 'medal']).size().reset_index(name='count')
    
    # Создание графика
    fig = px.bar(
        data_frame=medal_counts, 
        x='sport', 
        y='count', 
        color='medal', 
        title='Medals by Sport and Medal Type',
        labels={'count': 'Number of Medals'}
    )
    return fig

# Колбэк для обновления таблицы athlete_medals в зависимости от выбранного спорта и типа медали
@app.callback(
    Output('athlete-medals-table', 'data'),
    [Input('sport-dropdown', 'value'),
     Input('medal-radioitems', 'value')]
)
def update_athlete_medals_table(selected_sport, selected_medal):
    # Фильтрация данных на основе выбранного спорта и типа медали
    filtered_df = athlete_medals.copy(deep=True)
    
    if selected_sport:
        filtered_df = filtered_df[filtered_df['sport'] == selected_sport]
    
    if selected_medal != 'All':
        filtered_df = filtered_df[filtered_df['medal'] == selected_medal]
       
    return filtered_df.to_dict('records')

# Колбэк для обновления графика country_medal_tally в зависимости от выбранной страны
@app.callback(
    Output('country-medal-tally-graph', 'figure'),
    Input('country-dropdown', 'value')
)
def update_country_medal_tally_graph(selected_country):
    # Фильтрация данных на основе выбранной страны
    filtered_df = country_medal_tally.copy(deep=True)
    
    if selected_country:
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    # Создание графика
    fig = px.bar(
        data_frame=filtered_df, 
        x='country', 
        y=['gold', 'silver', 'bronze', 'total_medals'], 
        title='Medal Tally by Country',
        labels={'value': 'Number of Medals', 'variable': 'Medal Type'}
    )
    return fig

# Колбэк для обновления таблицы country_medal_tally в зависимости от выбранной страны
@app.callback(
    Output('country-medal-tally-table', 'data'),
    Input('country-dropdown', 'value')
)
def update_country_medal_tally_table(selected_country):
    # Фильтрация данных на основе выбранной страны
    filtered_df = country_medal_tally.copy(deep=True)
    
    if selected_country:
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    return filtered_df.to_dict('records')

# Колбэк для обновления графика и таблицы yearly_medal_count в зависимости от выбранного диапазона годов
@app.callback(
    [Output('yearly-medal-count-graph', 'figure'),
     Output('yearly-medal-count-table', 'data')],
    [Input('year-slider', 'value')]
)
def update_yearly_medal_count(selected_year_range):
    # Фильтрация данных на основе выбранного диапазона годов
    min_year, max_year = selected_year_range
    filtered_df = yearly_medal_count[(yearly_medal_count['year'] >= min_year) & (yearly_medal_count['year'] <= max_year)]
    
    # Создание графика
    fig = px.line(
        data_frame=filtered_df, 
        x='year', 
        y='total_medals', 
        title='Total Medals by Year',
        labels={'total_medals': 'Total Medals'}
    )
    
    return fig, filtered_df.to_dict('records')

# Колбэк для обновления графика и таблицы top_athletes в зависимости от выбранного вида спорта
@app.callback(
    [Output('top-athletes-graph', 'figure'),
     Output('top-athletes-table', 'data')],
    [Input('top-athletes-sport-dropdown', 'value')]
)
def update_top_athletes(selected_sport):
    # Фильтрация данных на основе выбранного вида спорта
    filtered_df = top_athletes.copy(deep=True)
    
    if selected_sport:
        filtered_df = filtered_df[filtered_df['sport'] == selected_sport]
    
    # Создание графика
    fig = px.bar(
        data_frame=filtered_df, 
        x='name', 
        y='total_medals', 
        color='sex', 
        title='Top Athletes by Sport',
        labels={'total_medals': 'Number of Medals', 'name': 'Athlete Name'}
    )

    return fig, filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)

