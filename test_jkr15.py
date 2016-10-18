import psycopg2
import random
from tabulate import tabulate
from  tournament import *


def connect():
    """Connect to the PostgreSQL database.  
    Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


deleteMatches()
deletePlayers()
db = connect()
c = db.cursor()
c.execute('alter sequence matches_id_seq restart;')
c.execute('alter sequence players_id_seq restart;')
db.close()




p1 = registerPlayer("Albus Dumbledore")
p2 = registerPlayer("Bellatrix Lestrange")
p3 = registerPlayer("Draco Malfoy")
p4 = registerPlayer("Ginny Weasley")
p5 = registerPlayer("Godric Gryffindor")
p6 = registerPlayer("Harry Potter")
p7 = registerPlayer("Hermione Granger")
p8 = registerPlayer("Lord Voldemort")
p9 = registerPlayer("Ron Weasley")
p10 = registerPlayer("Neville Longbottom")
p11 = registerPlayer("Dudley Dursley")
p12 = registerPlayer("Salazar Slytherin")
p13= registerPlayer("Thomas Riddle")
p14 = registerPlayer("Nearly Headless Nick")
p15= registerPlayer("Hedwig")

# round 1 matches
print '\nround 1'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
for pair in pairings:
	reportMatch(pair[0], pair[2])

# round 2 matches
print '\nround 2'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
for pair in pairings:
	reportMatch(pair[0], pair[2])

# round 3 matches
print '\nround 3'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
for pair in pairings:
	reportMatch(pair[0], pair[2])

# round 4 matches
print '\nround 4'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
for pair in pairings:
	reportMatch(pair[0], pair[2])

standings = playerStandings()
print tabulate(standings, headers=('id','name','wins','matches', 'omw'), tablefmt='orgtbl' )

# round 5 matches
print '\nround 5 (to be)'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
# for pair in pairings:
# 	reportMatch(pair[0], pair[2])

standings = playerStandings()
print tabulate(standings, headers=('id','name','wins','matches', 'omw', 'byes'), tablefmt='psql' )



print '\n'
print '\n'
print '\n'

# print tabulate(pairings, headers=('a','b','b','d'), tablefmt='psql' )
# print '\n'
# print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
# print '\n'



