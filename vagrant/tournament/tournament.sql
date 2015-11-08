-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop database if exists tournament;

create database tournament;

\connect tournament;

drop table if exists matches;

drop table if exists players;

create table players (
player_id serial primary key,
player_name text,
submit_time timestamp );

-- Add pseudo player 'bye' for skip round in odd player.
insert into players (player_id, player_name) values (0, 'bye');

create table matches (
match_id serial primary key,
win_id integer references players(player_id),
lose_id integer references players(player_id),
submit_time timestamp );

