# Quakelog parser
This is Quake III Arena server log file parser. The log file consists of many informations, such as when a match starts, when it ends, when a player joins, changes their name, kills another player, and so on. As an observation, there seems to be a little bug in the provided log file. The second game is initialized, but not finished (lines 11 - 97). Line 98 simply states that another game has begun. The log file can be easily fixed, but, since this is a coding test, I won't be overwriting the given log.

## First task
The first task consists of printing grouped information for each match, in the following manner:

```
"game_1": {
"total_kills": 45,
"players": ["Dono da bola", "Isgalamido", "Zeh"],
"kills": {
  "Dono da bola": 5,
  "Isgalamido": 18,
  "Zeh": 20
  }
}
```

## Second task
The second task consists of a report of deaths grouped by death cause for each match, e.g.:

```
"game-1": {
  "kills_by_means": {
    "MOD_SHOTGUN": 10,
    "MOD_RAILGUN": 2,
    "MOD_GAUNTLET": 1,
    ...
  }
}
```

## Running the code
Make sure you have git installed and insert the following commands on Terminal
1. Clone repository: ```git clone https://github.com/ybgodoy/Quakelog_parser.git```
2. Access the folder: ```cd Quakelog_parser```
3. For printing only the First Task: ```python main.py --scores```
4. For printing only the Second Task: ```python main.py --deaths```
5. For printing both Tasks merged: ```python main.py --all```
6. In case you want to consider players that have left the game mid-match and their respective score, add the flag ```--show_leaving_player``` to step 3 or step 4. **Without** this flag, players that leave the match **do not show up on the final results**, and **players that leave the match and come back, have their scores reset**. By adding this flag, players that do come back, return with the same score they had as they left.
7. To emphasize, for printing both Tasks merged, considering every player that has participated in the match at some point, you should run:
```python main.py --all --show_leaving_player```
As a general comment, notice that players can also change their names mid-match. If they do so, their score **does not** change, but their name gets updated. Only their last used name gets printed