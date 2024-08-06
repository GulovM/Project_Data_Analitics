-- Представление для медалей спортсменов
-- Это представление показывает информацию о спортсменах и их медалях, включая общее количество медалей каждого типа
create view if not exists athlete_medals as
select
    a.name, -- Имя спортсмена
    a.sex, -- Пол спортсмена
    a.born, -- Дата рождения спортсмена
    e.sport, -- Вид спорта
    e.event, -- Событие
    e.medal, -- Тип медали (золото, серебро, бронза)
    count(*) over (partition by e.medal) as medal_count -- Общее количество медалей каждого типа
from olympic_athlete_bio a
join olympic_athlete_event_results e on a.athlete_id = e.athlete_id
where e.medal is not null; -- Учитываются только записи, где есть медали

-- Представление для медального зачета по странам
-- Это представление показывает количество медалей каждого типа и общее количество медалей для каждой страны
create view if not exists country_medal_tally as
select
    c.country, -- Страна
    sum(case when t.medal = 'Gold' then 1 else 0 end) as gold, -- Количество золотых медалей
    sum(case when t.medal = 'Silver' then 1 else 0 end) as silver, -- Количество серебряных медалей
    sum(case when t.medal = 'Bronze' then 1 else 0 end) as bronze, -- Количество бронзовых медалей
    sum(case when t.medal is not null then 1 else 0 end) as total_medals -- Общее количество медалей
from olympics_country c
join olympic_athlete_event_results t on c.noc = t.country_noc
group by c.country; -- Группировка по странам

-- Представление для ежегодного медального зачета
-- Это представление показывает общее количество медалей, полученных в каждом году
create view if not exists yearly_medal_count as
select
    year, -- Год
    count(*) as total_medals -- Общее количество медалей
from olympic_games_medal_tally t
group by year -- Группировка по годам
order by year; -- Сортировка по годам

-- Представление для топовых спортсменов
-- Это представление показывает топ-3 спортсменов в каждой спортивной дисциплине по общему количеству медалей
create view if not exists top_athletes as
select
    name, -- Имя спортсмена
    sex, -- Пол спортсмена
    sport, -- Вид спорта
    total_medals -- Общее количество медалей
from (
    select
        a.name, -- Имя спортсмена
        a.sex, -- Пол спортсмена
        e.sport, -- Вид спорта
        count(*) as total_medals, -- Общее количество медалей
        row_number() over (partition by e.sport order by count(*) desc) as rank -- Рейтинг спортсмена в рамках вида спорта
    from olympic_athlete_bio a
    join olympic_athlete_event_results e on a.athlete_id = e.athlete_id
    where e.medal is not null -- Учитываются только записи, где есть медали
    group by a.name, a.sex, e.sport
) subquery
where rank <= 3; -- Учитываются только топ-3 спортсмена в каждом виде спорта
