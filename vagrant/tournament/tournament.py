#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager

@contextmanager
def conn_cur():
    dbconn = connect();
    cur = dbconn.cursor();
    yield cur
    dbconn.commit();
    cur.close();
    dbconn.close();

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    with conn_cur() as cur:
        cur.execute("delete from matches;");
        cur.execute("alter sequence matches_match_id_seq restart with 1;");

def deletePlayers():
    """Remove all the player records from the database."""
    with conn_cur() as cur:
        cur.execute("delete from players;");
        cur.execute("insert into players (player_id, player_name) values (0, 'bye');");
        cur.execute("alter sequence players_player_id_seq restart with 1;");

def countPlayers():
    """Returns the number of players currently registered."""
    with conn_cur() as cur:
        cur.execute("select count(player_id) as player_count from players where player_id > 0;");
        dbdata = cur.fetchall();
    return dbdata[0][0];

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    with conn_cur() as cur:
        cur.execute("insert into players (player_name, submit_time) values (%s, %s);", \
               (name, "now"));

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with conn_cur() as cur:
        cur.execute("\
            drop view if exists win_view;\
            drop view if exists match_view;\
            create view win_view as select players.player_id, count(matches.win_id) as win_count\
                from players left join matches\
                on players.player_id = matches.win_id and players.player_id > 0\
                group by players.player_id;\
            create view match_view as select players.player_id, count(matches.match_id) as match_count\
                from players left join matches\
                on (players.player_id = matches.win_id or players.player_id = matches.lose_id) and players.player_id > 0\
                group by players.player_id;\
            select players.player_id, players.player_name, win_view.win_count, match_view.match_count\
                from players, win_view, match_view\
                where (players.player_id = win_view.player_id and players.player_id = match_view.player_id) and players.player_id > 0\
                order by win_view.win_count desc, players.player_id;");
        ret_stand = cur.fetchall();

    return ret_stand;
    
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    if(winner == 0):
        winner, loser = loser, winner; #Swap winner/loser when meet "bye" id on winner.
    
    with conn_cur() as cur:
        cur.execute("insert into matches (win_id, lose_id, submit_time) values (%s, %s, %s);", \
               (winner, loser, "now"));
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ret_pair = [];
    with conn_cur() as cur:
        cur.execute("\
        select players.player_id, players.player_name, count(matches.win_id) as win_count\
            from players left join matches\
            on (players.player_id = matches.win_id)\
            where player_id > 0\
            group by players.player_id\
            order by win_count desc, players.player_id;");
        win_data = cur.fetchall();
    
    for i in range((len(win_data)/2)):
        ret_pair.append((win_data[i*2][0], win_data[i*2][1], win_data[i*2+1][0], win_data[i*2+1][1]));
    if(len(win_data)%2):
        ret_pair.append((win_data[(i+1)*2][0], win_data[(i+1)*2][1], 0, "bye"));
    
    return ret_pair;

