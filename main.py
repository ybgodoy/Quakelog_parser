import argparse
import json
from parsing import parsing_function

def read_lines():
    with open('qgames.log', 'r') as file:
        lines = file.read().splitlines()
    
    return [line.lstrip() for line in lines]


if __name__ == "__main__":

    lines = read_lines()

    parser = argparse.ArgumentParser(description="Process Quake log files.")
    parser.add_argument("--scores", action="store_true", help="Print only formatted scores")
    parser.add_argument("--deaths", action="store_true", help="Print only formatted deaths")
    parser.add_argument("--all", action="store_true", help="Print merged results")
    parser.add_argument("--show_leaving_players", action="store_true", help="Include leaving players in parsing")
    args = parser.parse_args()

    formatted_scores, formatted_deaths = parsing_function(lines, show_leaving_players=args.show_leaving_players)

    if args.scores:
        print(json.dumps(formatted_scores, indent=2))
    elif args.deaths:
        print(json.dumps(formatted_deaths, indent=2))
    elif args.all:
        merged_results = {game_key: {**formatted_scores[game_key], **formatted_deaths[game_key]}
                          for game_key in formatted_scores}
        print(json.dumps(merged_results, indent=2))
    else:
        print("No flag provided. Use --scores, --deaths, or --all to specify what to print. Don't forget to add --show_leaving_players if you wish to see data on players that left the match.")
