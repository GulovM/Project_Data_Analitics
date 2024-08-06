create view if not exists athlete_medals as
select
    a.name,
    a.sex,
    a.born,
    e.sport,
    t.year,
    e.event,
    e.medal,
    count(*) over (partition by e.medal) as medal_count
from olympic_athlete_bio a
join olympic_athlete_event_results e on a.athlete_id = e.athlete_id
join olympic_games_medal_tally t on t.edition_id = e.edition_id
where e.medal is not null;

create view if not exists country_medal_tally as
select
    c.country,
    sum(case when t.medal = 'Gold' then 1 else 0 end) as gold,
    sum(case when t.medal = 'Silver' then 1 else 0 end) as silver,
    sum(case when t.medal = 'Bronze' then 1 else 0 end) as bronze,
    sum(case when t.medal is not null then 1 else 0 end) as total_medals
from olympics_country c
join olympic_athlete_event_results t on c.noc = t.country_noc
group by c.country;

create view if not exists yearly_medal_count as
select
    year,
    count(*) as total_medals
from olympic_games_medal_tally t
group by year
order by year;

create view if not exists top_athletes as
select
    name,
    sex,
    sport,
    total_medals
from (
    select
        a.name,
        a.sex,
        e.sport,
        count(*) as total_medals,
        row_number() over (partition by e.sport order by count(*) desc) as rank
    from olympic_athlete_bio a
    join olympic_athlete_event_results e on a.athlete_id = e.athlete_id
    where e.medal is not null
    group by a.name, a.sex, e.sport
) subquery
where rank <= 3;
