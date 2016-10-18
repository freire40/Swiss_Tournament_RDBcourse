#!/usr/bin/env python
# 
# tournament_tmt.py 
#   implementation of multi-tournament cpability
#
# in this module:
#   def newTournament()
#   def saveAsNewTournament()
#   def listTournaments()
#   def retrieveTournament()
#   def currentTournament()
#   def saveTournament()    - not available in this version
#


import psycopg2
from tabulate import tabulate
from tournament import deleteMatches, deletePlayers 


def connect():
    """Connect to the PostgreSQL database.  
    Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def newTournament(name):
    """creates a new tournament.
  
    Args:
        name: the tournament's designation (need not be unique).

    Returns:
        id of the new tournament, unique
    """
    db = connect()
    c = db.cursor()
    c.execute('insert into tournament (name) values (%s) returning id;', (name,))
    id = c.fetchall()[0][0]
    db.commit()
    c.execute('select * from tournament where id = %s;', (id,))
    rows = c.fetchall()
    print 'New tournament: ID:', rows[0][0], ', Name:', rows[0][1], 'Saved at: ', rows[0][2]
    db.commit()
    db.close()
    return id


def currentTournament():
    """Retunrs the current tournament id and name. 
    A current tournament is defined after being retrieved or saved.
  
    Returns:
        a tuple (id, name):
            id: of the current tournament. -1 if no tournament selected
            name: of the current tournament
    """
    db = connect()
    c = db.cursor()
    c.execute('''select current_tournament.id, tournament.name 
        from current_tournament, tournament 
        where current_tournament.id = tournament.id;''')
    rows = c.fetchall()
    if len(rows) == 0:
        # print 'No tournament selected'
        return (-1, '')
    id = rows[0][0]
    name = rows[0][1]
    # print 'Current tournament: ID:', id, ', Name:', name
    db.close()
    return (id, name)


def listTournaments():
    """Lists existing tournaments.
    Different saves of the same tournament are attributed different id's and 
    different save dates. The user has the option of maintaining the same name at save time.
  
    Returns:
        a list of tuples with: 
            id: tournament unique identifier
            name: tournament designation
            savedate: timestamp date when the tournament was saved
    """
    db = connect()
    c = db.cursor()
    c.execute('select * from tournament order by name, save_date;')
    rows = c.fetchall()
    # print '\nList of tournaments:'
    # print tabulate (rows, tablefmt='simple', headers=('id', 'designation', 'saved as'))
    db.commit()
    db.close()
    return rows


def saveAsNewTournament(name):
    """saves current tournament data.
    Different saves of the same tournament are attributed different id's and 
    different save dates. The user has the option of maintaining the same name at save time.
  
    Args:
        name: name of the current tournament, need not be unique
    Returns:
        id: a new tournament unique identifier
    """

    # copies current players and matches into tournament repository tables

    id = newTournament(name)
    db = connect()
    c = db.cursor()
    c.execute('''
        insert into players_repo 
            select %s as tourn_id, id as player_id, name from players;''', (id,))
    c.execute('''
        insert into matches_repo 
            select %s as tourn_id, id as match_id, player_id, result, bye from matches;''', (id,))
    c.execute('delete from current_tournament;')
    c.execute('insert into current_tournament (id) values (%s);', (id,))
    db.commit()
    db.close()
    return id


def retriveTournament(id):
    """retrieves a saved tournament data.
    
    Args:
        id: a saved tournament unique identifier
    """

    # deletes current players and matches
    # and copies from tournament repository tables the saved tournament players and matches

    deleteMatches()
    deletePlayers()
    db = connect()
    c = db.cursor()
    c.execute('alter sequence matches_id_seq restart;')
    c.execute('alter sequence players_id_seq restart;')
    
    c.execute('''
        insert into players 
            select player_id as id, name 
                from players_repo where tourn_id = %s;''', (id,))
    c.execute('''
        insert into matches 
            select match_id as id, player_id, result, bye 
                from matches_repo where tourn_id = %s;''', (id,))

    c.execute('delete from current_tournament;')
    c.execute('insert into current_tournament (id) values (%s);', (id,))

    db.commit()
    db.close()



