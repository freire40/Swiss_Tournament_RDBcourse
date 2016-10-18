# Swiss Tournament Planner 

###Purpose:
This module provides a set of python functions that fully support a swiss style tournament. Win-lose matches only.
Functions keep track of players and matches, generate game pairings for each round, and allow for multi-tournament. 
Database is implemented in PSQL/ psycopg2.
Developed for the Udacity Relational Database course, fulfills base specification and all extra credit except draw games.

###Functional specifications:

####In-tournament functions:
* `registerPlayer()`
* `reportMatch()` - win-lose
* `playerStandings()` - ranks players by number of wins and OMW (Oponnents Match Wins)
* `swissPairings()` - pairs players for next round
for a blank new tournament, initialize it by:
* `delete matches()`
* `delete players()`

Pairing is done: 
* randomly within the same number of wins rank (see spec text) or nearly that;
* rematches are avoided
* if odd number of players, the last one in the standings receives a bye, assuring no one players gets more than a bye per tournament.

####Multi-tournament functions:
Multiple tournaments are run one at a time.
* `saveAsNewTournament()` - saves current tournament data, without overwriting previous save versions. A savedate timestamp is provided.
* `retrieveTournament()` - retrieves tournament data from previous save
Multiple tournaments can be run concurrently, one at a time, as long as (improve text)

Further tournament information can be queried directly into the database tables:
* players
* matches
* tournaments

A complete list and description of functions and schema can be found within each module file and sql script.

**Final note on the specifications and test functions provided by Udacity:**
Implementation of the multi-tournament support was designed so that all functions should comply with the base specification. A change, however, was introduced to playerStandigs(). The number of values returned now include OMW and Byes granted. Testing module provided was changed accordingly. This change can easily be reversed if to provide full compliance.


### setup and installation:

Uses Python 2.7 and PostgreSQL (psycopg2).

Database creation script: 
From psql prompt run: 
* `\i tournament.sql` 		- base tournament schema
* `\i tournament_tmt.sql` 	- multi-tournament schema

Python packages: 
Install python package `tabulate` for improved print layout of stangings and pairings tables [https://pypi.python.org/pypi/tabulate].

Python module functions:
Import python modules: 
* `tournament.py`		- in or single tournament functions
* `tournament_tmt.py`	- multi tournament support


###Testing examples
Besides the supplyed testing function `tournament_test.py`, additional 
testing scenarios and examples are provided. Simply run them from command line `python <test_file_name>`. Tournament data can then be inspected from psql prompt.

* `tournament_test.py` 	- the original Udacity test file, adapted to the new players_standings() spec
* `test_lv.py`			- 8-player pairing example
* `test_jkr9.py` 		- 9-player pairing example
* `test_jkr15.py` 		- 15-player pairing example
* `test_tmt.py` 		- run the previous tests in sequence, saves them, and retrieves the first one.


### Future developments
* allow for draws, as an option - scoring function would have to modified. Suggestion: use flag in tournament definition, when tournament is created. Ranking function would check this flag. As a result, the existing interfaces and functions could be kept as unchanged.
* allow save to overwrite an previously saved tournament. Currently, each save creates a new tournament id and timestamp.  



