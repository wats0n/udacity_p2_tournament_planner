# Project 2 : Tournament Planner

This is a game tournament planning and scoring system. Using Python module to simulate Swiss system for pairing matches and store relative information to PostgreSQL via SQL syntax.
Add 9th testing extra conditions with odd pairing, initial random matching, and Opponent Match chance.

## Quick Start

1. Install [Git 2.6.3](http://git-scm.com/downloads)
2. Install [Virtual Box 4.3.28](https://www.virtualbox.org/wiki/Download_Old_Builds_4_3)
3. Install [Vagrant 1.7.4](https://www.vagrantup.com/downloads.html)
4. Clone project by 
  * "git clone https://github.com/wats0n/udacity_p2_tournament_planner.git"
5. Find "vagrant" folder in download project directory.
6. Using "Git bash here" on mouse menu
7. Execute following command to setup and login VM:
  * vagrant up
  * vagrant ssh
8. In VM prompt, typing following command to project directory:
  * cd /vagrant/tournament/
9. Using below command to setup PostgreSQL
  * psql -f tournament.sql
10. Executing "python tournament_test.py" to test tournament planner result.
11. Exit vagrant by "exit" command, exit git-bash environment is "exit" command, too.

## What's Included

Within the download you'll find following directories and files.
All dependency library and resource are packed in this package.

```
./
|-pg_config.sh
|-Vagrantfile
|-.vagrant/
|-catalog/
|-tournament/
|--tournament.py
|--tournament.sql
|--tournament_test.py

```

## Creator(s)
------
Watson Huang (wats0n)
11/08, 2015