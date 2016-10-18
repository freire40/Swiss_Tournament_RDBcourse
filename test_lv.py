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




p1 = registerPlayer("Diana")
p2 = registerPlayer("Teodoro")
p3 = registerPlayer("Marcela")
p4 = registerPlayer("Tristan")
p5 = registerPlayer("Fabio")
p6 = registerPlayer("Anarda")
p7 = registerPlayer("Ricardo")
p8 = registerPlayer("Ludovico")

# round 1 matches
print '\nround 1'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
reportMatch(p1, p3)
reportMatch(p2, p4)
reportMatch(p6, p5)
reportMatch(p8, p7)

# round 2 matches
print '\nround 2'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
reportMatch(p2, p8)
reportMatch(p1, p6)
reportMatch(p4, p7)
reportMatch(p3, p5)

# round 3 matches
print '\nround 3'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
reportMatch(p2, p1)
reportMatch(p6, p3)
reportMatch(p8, p4)
reportMatch(p5, p7)

# round 4 matches
print '\nround 4 (would be)'
pairings = swissPairings()
print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )

print '\n'
print '\n'
print '\n'

# print tabulate(pairings, headers=('a','b','b','d'), tablefmt='psql' )
# print '\n'
# print tabulate(pairings, headers=('a','b','b','d'), tablefmt='orgtbl' )
# print '\n'



