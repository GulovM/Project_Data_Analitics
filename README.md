# Olympic Data Analytics Dashboard

Этот проект был создан Гуловом Мухсином для анализа данных Олимпийских игр и визуализации различных метрик с использованием Dash и Plotly.

## Используемые инструменты

Проект использует следующие инструменты и библиотеки:
- **Dash**
- **Plotly**
- **Pandas**
- **DuckDB**
- **Gunicorn**

## Структура репозитория

Репозиторий имеет следующую структуру:
Project_Data_Analitics/
- dashboard.py # Основной файл приложения Dash
- etl.py # Файл для извлечения и трансформации данных
- requirements.txt # Файл с зависимостями проекта
- Procfile # Файл для развертывания на Render с Gunicorn
- runtime.txt # Файл для указания версии Python
- queries/
  - create_tables.sql # SQL скрипт для создания таблиц
  - create_views.sql # SQL скрипт для создания представлений
- source/
  - Olympic_Athlete_Bio.xlsx
  - Olympic_Athlete_Event_Results.xlsx
  - Olympic_Games_Medal_Tally.xlsx
  - Olympics_Country.xlsx
  - Olympics_Games.xlsx
- README.md # Файл с описанием репозитория
