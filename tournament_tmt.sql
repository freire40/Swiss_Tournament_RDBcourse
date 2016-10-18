-- Table definitions for the tournament project.
--      adicional specs: multi-tournament support
-- To be run from the psql prompt
--
-- List of tables and views in this file:
--       tables
--             tournament
--             players_repo
--             matches_repo
--             current_tournament


DROP TABLE if exists tournament cascade;
drop table if exists players_repo cascade;
drop table if exists matches_repo cascade;
drop table if exists current_tournament cascade;


create table tournament (
    id serial PRIMARY KEY,
    name TEXT,
    save_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


CREATE TABLE players_repo (
    tourn_id int references tournament(id),
    player_id INT,
    name TEXT,
    PRIMARY KEY (tourn_id, player_id)
    );


CREATE TABLE matches_repo (
    tourn_id int,
    match_id int,
    player_id INT,
    result TEXT,
    bye TEXT,
    PRIMARY KEY (tourn_id, match_id, player_id),
    foreign key (tourn_id, player_id) references players_repo(tourn_id, player_id)
    );


create table current_tournament (
    id int references tournament(id)
    )

