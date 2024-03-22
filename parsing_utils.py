def update_player_name(line, namechange_pattern, current_players, leaving_players, show_leaving_players=False):
    match = namechange_pattern.match(line)
    player_id, player_name = match.group(1), match.group(2)

    if not show_leaving_players:
        if player_id not in current_players:
            current_players[player_id] = [player_name, 0]
        else:
            current_players[player_id][0] = player_name         
    else:
        if player_name in leaving_players:
            current_players[player_id] = [player_name, leaving_players[player_name]]
            del leaving_players[player_name]
        elif player_id not in current_players:
            current_players[player_id] = [player_name, 0]
        else:
            current_players[player_id][0] = player_name

def remove_player(line, playerleft_pattern, current_players, leaving_players):
    match = playerleft_pattern.match(line)
    player_id = match.group(1)
    player_name, player_score = current_players[player_id][0], current_players[player_id][1]
    leaving_players[player_name] = player_score
    del current_players[player_id]

def update_kill_score(line, kill_pattern, current_players, death_cause):
    match = kill_pattern.match(line)
    win, lose, cause = match.group(1), match.group(2), match.group(3)
    current_players[win][1] += 1
    current_players[lose][1] -= 1
    
    if cause not in death_cause:
        death_cause[cause] = 1
    else:
        death_cause[cause] += 1

    return 1

def format_scores(score_results, total_kills):
    formatted_score = {}
    for game_num, players_scores in score_results.items():
        game_info = {
            'total_kills': total_kills[int(game_num)-1],
            'players': [name for name, _ in players_scores.values() if name != 'World'],  # Exclude 'World' as requested
            'kills': {name: kill for name, kill in players_scores.values() if name != 'World'}
        }
        formatted_score[f'game_{game_num}'] = game_info

    return formatted_score

def format_deaths(death_results):
    formatted_deaths = {}
    for game_num, causes in death_results.items():
        game_info = {
            "kills_by_means": causes
        }
        formatted_deaths[f"game_{game_num}"] = game_info
    
    return formatted_deaths