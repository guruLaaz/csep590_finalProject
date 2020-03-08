"""
python download_data.py --year 2019
"""

import json
import argparse
import requests


def player_value(stat):
    return stat['FantasyPointsYahoo']


def player_id(stat):
    return stat['PlayerID']


def player_position(stat):
    return stat['Position']


def player_name(stat):
    return stat['Name']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download FantasyData.')
    parser.add_argument('--year', default=2019, type=str)
    args = parser.parse_args()

    json_api_body = requests.get("https://fantasydata.com/FantasyStatsNHL/FantasyStats_Read?sort=FantasyPoints-desc"
                                 f"&pageSize=1000&filters.scope=1&filters.season={args.year}&filters.seasontype=1") \
        .json()

    stats = json_api_body['Data']
    players = []
    for i, stat in enumerate(stats):
        players.append({
            "id": player_id(stat),
            "name": player_name(stat),
            "position": player_position(stat),
            "value": player_value(stat)
        })

    with open(f'./data/stats_{args.year}.json', 'w') as out:
        json.dump(players, out, indent=2)
