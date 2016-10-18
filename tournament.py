#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# in this module, functions and supporting functions:
#   def connect()
#   def deleteMatches()
#   def deletePlayers()
#   def countPlayers()
#   def registerPlayer()
#   def playerStandings()
#   def reportMatch()
#   def swissPairings()
#         def randomize_standings_ranks()
#         def next_player_to_bye()
#         def previous_match()
#         def next_unpaired_player()


import psycopg2
import random
from tabulate import tabulate


def connect():
    """Connect to the PostgreSQL database.  
    Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute('delete from matches;')
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute('delete from players cascade;')
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute('select count(*) from players;')
    rows = c.fetchall()
    np = rows[0][0]
    db.close()
    return np


def registerPlayer(name):
    """Adds a player to the tournament database.

    Args:
        name: the player's full name (need not be unique).

    Returns:
        id: unique id of the new registered player
    """
    db = connect()
    c = db.cursor()
    c.execute('insert into players (name) values (%s) returning id;', (name,))
    pid = c.fetchall()[0][0]
    # print 'new player: ID:', pid, ', Name:', name  
    db.commit()
    db.close()
    return pid


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list is the player in first place, or a player
    tied for first place if there is currently a tie.

    *change to the original specification: 

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches, omw):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
        omw: opponents' matches wins
        num_byes: number of byes a player has received, 1 or 0 
    """
    db = connect()
    c = db.cursor()
    c.execute('select * from player_standings_omw')
    rows = c.fetchall()
    db.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    All matches must have a winner.
    If a bye is granted to a player, counts as a won match.

    Args:
        winner:  the id number of the player who won
        loser:  the id number of the player who lost
        In case of a bye, have winner = loser
    """
    db = connect()
    c = db.cursor()
    if winner == loser: 
        # it's a bye
        c.execute('insert into Matches (player_id, result, bye) VALUES (%s, %s, %s) returning id;', (winner,'winner','bye'))        
    else:
        # regular win-lose match
        c.execute('insert into Matches (player_id, result) VALUES (%s, %s) returning id;', (winner,'winner'))
        mid = c.fetchall()[0][0]
        c.execute('insert into Matches (id, player_id, result) VALUES (%s, %s, %s);', (mid, loser,'loser'))
    db.commit()
    db.close()
    # if winner == loser:     
    #     print 'new match result: winner:', winner, '(got a bye)'
    # else:
    #     print 'new match result: winner:', winner, ', loser:', loser



def randomize_standings_ranks(standings):
    '''Returns the players standings list, 
    after randomizing each group of players with the same number of wins (ranks)

    The standings list must be ordered by wins.
    The list returned is ready to be players-paired in sequence, unless 
    other pairing-restrictions are desired.

    Returns:
      A list of tuples, each tuple equal to the original standings tuples:
    '''

    # get wins-ranks and num-players per rank
    db = connect()
    c = db.cursor()
    c.execute('select num_wins, count(num_wins) from player_standings_omw group by num_wins order by num_wins desc')
    rows = c.fetchall()
    db.close()

    # slice players into ranks (wins groups) and randomizes them
    # the algorith is not optimal in avoiding that skipping rematches force unnecessarily 
    # one player from one rank to be paired to another rank, whereas a different randomizition 
    # solve this.
    i=0         # rank index
    cursor=0    # standings cursor
    ranks=[]       # list of rank players' lists
    for i in range(0,len(rows)):
            # print 'rank ' + str(i)  + ': ' + str(cursor) + '-' + str(cursor+rows[i][1])
            ranks.append (standings[cursor:cursor+rows[i][1]])
            # print ranks[i]
            random.shuffle(ranks[i])
            # print ranks[i]
            cursor += rows[i][1]

    newplayerstandings = []
    for r in range(len(rows)):
        newplayerstandings += ranks[r]
    return newplayerstandings


def next_player_to_bye (standings):
    ''' Finds next player to bye, starting from last on standings backwards,
    until the first not having received previously a bye is reached.
    As a design option, the randomized standings order is used, therefore,
        can't be done using queries 

    Arg:
        standings: ordered list of players

    Returns:
        id: index of the chosen player in standings to get a bye 
    '''
    db = connect()
    c = db.cursor()
    c.execute('select player_id from matches where bye = %s;', ('bye',))
    rows = c.fetchall()
    db.close()

    byed_players = [r[0] for r in rows]
    players = range(len(standings))
    for p in reversed(players):
        if standings[p][0] in byed_players:
            continue
        else:
            return p
    # the for loop will never reach the end, 
    # for the number of rounds will be small 
    # compared to the number of players   


def previous_match (p1, p2):
    ''' Checks for previous matches between two players
    
    Args:
        p1: first player id
        p2: second player id

    Returns:
        number of previous matches, 0 if none. 
    '''
    db = connect()
    c = db.cursor()
    c.execute('''
        select id from matches 
        where player_id = %s
            and id in 
            (select id from matches where player_id = %s);
        ''', (p2, p1))
    rows = c.fetchall()
    db.close()
    return len(rows)


def next_unpaired_player (standings, paired, p1, p2=-1):
    '''Validates a given player, and if not valid, 
            returns the next in line that does. 
    if p2 ommited, tests if player p1 is available for pairing.
    If p2 defined, tests if player p2 is available for pairing AND
        had no previous match with player p1

    Args:
        standings: ordered by rank
        paired: a list of paired players, flagged 0|1 
        p1: the index (referring to the standings list) of the first player in a pair to be tested
        p2: optional, the index (referring to the standings list) of the second player in a pair to be tested
        
    Returns:
        the index of the standings list of the next eligible first or second player requested
        returns -1, if a pair can't be formed (a new pairing sequence has to be prepared) 
    '''
    a1 = p1
    a2 = p2
    if a2 == -1:   
        # check 1st player for not being already paired
        while a1 < len(standings):
            if paired[a1]:
                a1 += 1
            else:   
                return a1
        # never reaches this point    
    else: 
        # check 2nd player for not being already paired AND 
        #       not previously matched with p1
        while a2 < len(standings):
            if paired[a2] == 0 and previous_match(standings[a1][0],standings[a2][0]) == 0:
                    return a2
            a2 += 1
        # if reaches this point, means no more free players,
        # must reshuffle standings
        return -1   

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Each player appears exactly once in the pairings.  
    Number of players may be even or odd. In this case, the last ranked player
    receives a bye. Only one bye per player within the tournament.

    Each player is paired randomly with another player with an equal or nearly-equal 
    win record, that is, a player adjacent to him or her in the standings.
    Standings ranks consider omw. However as a design choice, omw is not considered 
    in the pairings, only the number of wins. (No references were found recommending 
    pairings based on wins *and* omw.)
    
    No rematches allowed.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's id
        name1: the first player's name
        id2: the second player's id
        name2: the second player's name
    """

    # Pairing algorithm description:
    # 0. keep a flagged list of players already matched/ free
    # 1. split list of players into groups with same num_wins
    #       randomize each group (rank)
    # 2. bye last player, if odd players
    # 3. select first/ next free player
    #       select second/ next free player. 
    #       Test it agains rematches. 
    #       If not, set pair and flag both as paired
    #       In case last pair is a rematch,   
    #           randomize ranks again and 
    #           start pairing from scratch
    #
    # Assumes that an impossible pairing combination
    # given these restrictions, is impossible.

    while True:     # pairing process will be run again and again
                    # until pairing is successful

        # 1. randomize players list, by num_wins groups
        standings = playerStandings()
        newplayerstandings = randomize_standings_ranks(standings)

        # 0. init variables
        num_players = len(newplayerstandings)
        num_pairs = num_players / 2 + num_players % 2
        paired = [0] * num_players      # flags all players as not yet paired
        pairings = [0] * (num_pairs)    # allows initial insertion of bye as last pair 

        # 2. bye a player if odd number of players
        if num_players % 2 != 0:
            p1 = next_player_to_bye (newplayerstandings)
            bye_tuple = (newplayerstandings[p1][0], newplayerstandings[p1][1],
                newplayerstandings[p1][0], newplayerstandings[p1][1])
            pairings[num_players / 2] = (bye_tuple)
            paired[p1] = 1
            # remainig number of free players is even
        
        # 3. pair players, checking restrictions
        p1 = 0      # player seq id within the list
        i = 0       # pairing list index
        while i < num_players / 2:  # if odd, last pair is already done
            # find first player
            p1 = next_unpaired_player(newplayerstandings, paired, p1)
            p2 = p1 + 1
            # find second player
            p = next_unpaired_player(newplayerstandings, paired, p1, p2)
            if p == -1:     # meaning no more free or un-rematched players, must reshuffle standings
                            # uses p = -1 as flag
                # print 'Must restart pairings, no more valid pairs found.'
                break   
            p2 = p
            # pair them! and flag both players as already paired
            pairing_tuple = (newplayerstandings[p1][0], newplayerstandings[p1][1],
                newplayerstandings[p2][0], newplayerstandings[p2][1])
            pairings[i] = pairing_tuple
            paired[p1] = 1
            paired[p2] = 1
            p1 += 1
            i += 1
        if p == -1:      # restart pairing
            continue
        else:
            break
    
    return pairings


