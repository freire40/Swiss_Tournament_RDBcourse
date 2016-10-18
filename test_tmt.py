#!/usr/bin/env python
#
# tests multi-tournament functionality
# by running other single tournament test files
# and saving them to tournament repositories,
# and retrieving the first one of them
#


import psycopg2
import random
from tabulate import tabulate
from  tournament import *
from  tournament_tmt import *


def connect():
    """Connect to the PostgreSQL database.  
    Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


import test_lv
HC_tournament = saveAsNewTournament("Hortelano Cup 2016")

import test_jkr2_random
saveAsNewTournament("Hogwarts 9-Cup 2016")

import test_jkr3_random
saveAsNewTournament("Hogwarts 15-Cup 2016")

print '\nList of tournaments:'
print tabulate (listTournaments(), tablefmt='simple', headers=('id', 'designation', 'saved as'))
    
retriveTournament(HC_tournament)  
currentTournament()
# the retrieved data can be confirmed in the PSQL interface

print '\n'
print '\n'
print '\n'




