import re

from parsing_utils import update_player_name
from parsing_utils import remove_player
from parsing_utils import update_kill_score
from parsing_utils import format_scores
from parsing_utils import format_deaths

initgame_pattern = re.compile(r'^\d+:\d+ InitGame:')
namechange_pattern = re.compile(r'^\d+:\d+ ClientUserinfoChanged: (\d+) n\\([^\\]+)')    # A PLAYER CAN CHANGE NAME MIDGAME AND KEEP THEIR STATS!!!
playerleft_pattern = re.compile(r'^\d+:\d+ ClientDisconnect: (\d+)')
kill_pattern = re.compile(r'^\d+:\d+ Kill: (\d+) (\d+) \d+: .* by (\w+)')

def parsing_function(lines_list, show_leaving_players=False):
    game_count = 1
    total_kills = [0]
    score_results = {}
    current_players = {}
    leaving_players = {}
    death_cause = {}
    death_results = {}

    for line in lines_list[2:]:
        # Check if another game is initialized. If it is, append the previous game's results. Also, start with World, indexed in the logfile as 1022, with 0 kills.
        # Reason for starting from line_list[2] is due to bug in the log file, as explained in the README section
        if initgame_pattern.match(line):
            # Append the names of players who left during the match in case show_leaving_players=True and leaving_players not empty
            if leaving_players and show_leaving_players:
                # Assign new keys starting from the max key in current_players + 1 for each entry in leaving_players
                leaving_players = {int(max(current_players.keys())) + i + 1: [name, score] for i, (name, score) in enumerate(leaving_players.items())}
                current_players = {**current_players, **leaving_players}
            score_results[str(game_count)] = current_players.copy()
            death_results[str(game_count)] = death_cause.copy()
            current_players = {'1022' : ['World', 0]}
            leaving_players = {}
            death_cause = {}
            game_count+=1
            total_kills.append(0)

        # Check for new players AND name changes.
        elif namechange_pattern.match(line):
            update_player_name(line, namechange_pattern, current_players, leaving_players, show_leaving_players)

        # Check whether a player has left the game. 
        elif playerleft_pattern.match(line):
            remove_player(line, playerleft_pattern, current_players, leaving_players)

        # Check for kills. Attribute 1 point to the killer, and deduce 1 point from the killed
        elif kill_pattern.match(line):
            total_kills[game_count-1] += update_kill_score(line, kill_pattern, current_players, death_cause)
            
    score_results[str(game_count)] = current_players.copy()
    death_results[str(game_count)] = death_cause.copy()
    formatted_scores = format_scores(score_results, total_kills)
    formatted_deaths = format_deaths(death_results)
    
    return formatted_scores, formatted_deaths


    