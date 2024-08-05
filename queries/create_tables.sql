create table if not exists olympics_country (
    noc varchar(5) primary key,
    country varchar(100) not null
);

create table if not exists olympic_athlete_bio (
    athlete_id integer primary key,
    name varchar(80) not null,
    sex varchar(7),
    born varchar(30),
    height integer,
    weight varchar(10),
    country varchar(50) not null,
    country_noc varchar(10) not null,
    foreign key (country_noc) references olympics_country(noc)
);

create table if not exists olympics_games (
    edition varchar(100) not null,
    edition_id integer primary key,
    year integer not null,
    city varchar(80) not null,
    country_noc varchar(5) not null,
    start_date varchar(30),
    end_date varchar(30),
    competition_date varchar(60),
    isHeld varchar(50),
    foreign key (country_noc) references olympics_country(noc)
);

create table if not exists olympic_athlete_event_results (
    edition varchar(80) not null,
    edition_id integer not null,
    country_noc varchar(5) not null,
    sport varchar(50) not null,
    event text not null,
    result_id integer,
    athlete varchar(100) not null,
    athlete_id integer not null,
    pos varchar(50),
    medal varchar(20),
    isTeamSport boolean not null,
    foreign key (country_noc) references olympics_country(noc),
    foreign key (athlete_id) references olympic_athlete_bio(athlete_id),
    foreign key (edition_id) references olympics_games(edition_id)
);

create table if not exists olympic_games_medal_tally (
    edition varchar(100) not null,
    edition_id integer not null,
    year integer not null,
    country varchar(100) not null,
    country_noc varchar(5) not null,
    gold integer not null,
    silver integer not null,
    bronze integer not null,
    total integer not null,
    foreign key (country_noc) references olympics_country(noc),
    foreign key (edition_id) references olympics_games(edition_id)
);
