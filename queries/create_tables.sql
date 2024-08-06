-- Таблица для хранения информации о странах
create table if not exists olympics_country (
    noc varchar(5) primary key, -- Национальный олимпийский комитет (NOC) код
    country varchar(100) not null -- Название страны
);

-- Таблица для хранения биографической информации об олимпийских спортсменах
create table if not exists olympic_athlete_bio (
    athlete_id integer primary key, -- Уникальный идентификатор спортсмена
    name varchar(80) not null, -- Имя спортсмена
    sex varchar(7), -- Пол спортсмена
    born varchar(30), -- Дата рождения спортсмена
    height integer, -- Рост спортсмена
    weight varchar(10), -- Вес спортсмена
    country varchar(50) not null, -- Страна спортсмена
    country_noc varchar(10) not null, -- NOC код страны спортсмена
    foreign key (country_noc) references olympics_country(noc) -- Внешний ключ на таблицу olympics_country
);

-- Таблица для хранения информации об олимпийских играх
create table if not exists olympics_games (
    edition varchar(100) not null, -- Издание Олимпийских игр (например, Летние или Зимние)
    edition_id integer primary key, -- Уникальный идентификатор издания Олимпийских игр
    year integer not null, -- Год проведения Олимпийских игр
    city varchar(80) not null, -- Город проведения Олимпийских игр
    country_noc varchar(5) not null, -- NOC код страны проведения Олимпийских игр
    start_date varchar(30), -- Дата начала Олимпийских игр
    end_date varchar(30), -- Дата окончания Олимпийских игр
    competition_date varchar(60), -- Даты проведения соревнований
    isHeld varchar(50), -- Статус проведения Олимпийских игр (например, "Проведены" или "Отменены")
    foreign key (country_noc) references olympics_country(noc) -- Внешний ключ на таблицу olympics_country
);

-- Таблица для хранения результатов событий олимпийских спортсменов
create table if not exists olympic_athlete_event_results (
    edition varchar(80) not null, -- Издание Олимпийских игр
    edition_id integer not null, -- Уникальный идентификатор издания Олимпийских игр
    country_noc varchar(5) not null, -- NOC код страны спортсмена
    sport varchar(50) not null, -- Вид спорта
    event text not null, -- Событие (дисциплина)
    result_id integer, -- Уникальный идентификатор результата
    athlete varchar(100) not null, -- Имя спортсмена
    athlete_id integer not null, -- Уникальный идентификатор спортсмена
    pos varchar(50), -- Позиция (место)
    medal varchar(20), -- Тип медали (золото, серебро, бронза)
    isTeamSport boolean not null, -- Командный спорт или индивидуальный (true или false)
    foreign key (country_noc) references olympics_country(noc), -- Внешний ключ на таблицу olympics_country
    foreign key (athlete_id) references olympic_athlete_bio(athlete_id), -- Внешний ключ на таблицу olympic_athlete_bio
    foreign key (edition_id) references olympics_games(edition_id) -- Внешний ключ на таблицу olympics_games
);

-- Таблица для хранения медального зачета по изданиям Олимпийских игр
create table if not exists olympic_games_medal_tally (
    edition varchar(100) not null, -- Издание Олимпийских игр
    edition_id integer not null, -- Уникальный идентификатор издания Олимпийских игр
    year integer not null, -- Год проведения Олимпийских игр
    country varchar(100) not null, -- Страна
    country_noc varchar(5) not null, -- NOC код страны
    gold integer not null, -- Количество золотых медалей
    silver integer not null, -- Количество серебряных медалей
    bronze integer not null, -- Количество бронзовых медалей
    total integer not null, -- Общее количество медалей
    foreign key (country_noc) references olympics_country(noc), -- Внешний ключ на таблицу olympics_country
    foreign key (edition_id) references olympics_games(edition_id) -- Внешний ключ на таблицу olympics_games
);
