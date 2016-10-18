-- Table definitions for the tournament project.
-- To be run from the psql prompt
--
-- List of tables and views in this file:
--         tables
--              players
--              matches
--         views
--              player_standings    - players ranks without OMW
--              player_standings_omw    - players ranks OMW
--              AMPP                - all mathes per player
--              AMOPP               - all matches and opponents per player
--              matches_n           - matches with players names
--              OMW                 - sum opponents' wins per player
--              player_standings_wins
--              player_matches


-- Create Database 'tournament' and connect to it
drop database if exists tournament;
CREATE DATABASE tournament;
\c tournament

-- in re-runs from PSQL with connection active, database won't be droped
-- for this case:
DROP TABLE if exists Players cascade;
drop table if exists Matches cascade;


CREATE TABLE Players (
    id serial PRIMARY KEY,
    name TEXT
    );


CREATE TABLE Matches (
    -- A match is a two-row entry, one for each player
    -- with a common match id
    id serial,
    player_id INT REFERENCES Players(id),
    result TEXT,
    bye TEXT default '',
    PRIMARY KEY (id, player_id)
    );


-- aux to PlayerStandings: counts wins and byes per player
create view player_standings_wins as 
    select 
        Players.id, 
        name as player, 
        count(matches_winners.result) as num_wins,
        coalesce(matches_byes.num_byes,0) as num_byes
    from Players 
        left join (select * from Matches where result = 'winner') as matches_winners
            on matches_winners.player_id = Players.id
        left join 
            (select player_id, count(player_id) as num_byes 
                from Matches 
                where bye = 'bye' 
                group by player_id) as matches_byes
            on matches_byes.player_id = Players.id      
    group by players.id, player, num_byes
    order by num_wins desc;


create view player_matches as 
    select players.id as id, count(player_id) as num_matches 
    from players left join matches 
    on players.id = matches.player_id
    group by players.id, player_id;


create view player_standings as 
    select 
        player_standings_wins.id, 
        player, 
        num_wins, 
        num_matches,
        num_byes
    from player_standings_wins left join player_matches
    on player_standings_wins.id = player_matches.id
    order by num_wins desc;


-- all matches per player (AMPP)
create view AMPP as 
    select 
        players.id, 
        name, 
        result, 
        matches.id as match
    from players, matches 
    where players.id = matches.player_id
    order by name asc;


-- matches with players' names
create view matches_n as 
    select 
        matches.id as id, 
        player_id, 
        name as player_name, 
        result, 
        bye
    from matches, players
    where players.id = matches.player_id;


-- all matches and opponents per player (AMOPP)
create view AMOPP as 
    select 
        AMPP.id, 
        AMPP.name, 
        AMPP.result, 
        match, 
        matches_n.player_id as o_id, 
        matches_n.player_name as opponent,
        matches_n.result as o_result, bye
    from AMPP join matches_n
    on match = matches_n.id
    where AMPP.id != matches_n.player_id
    order by AMPP.name;


-- OMW, sum opponents' wins per player
create view OMW as 
    select 
        AMOPP.id, 
        AMOPP.name, 
        sum (num_wins) as OMW
    from AMOPP join player_standings as PS
    on AMOPP.o_id = PS.id
    group by AMOPP.id, name
    order by name;


-- Player Standings with OMW
create view player_standings_omw as 
    select 
        PS.id, 
        PS.player, 
        cast(num_wins as int), 
        cast(num_matches as int), 
        cast (coalesce(OMW.OMW, 0) as int) as OMW,
        num_byes
    from player_standings as PS left join OMW 
    on PS.id = OMW.id
    order by num_wins desc, OMW desc;

