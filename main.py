import argparse
import json
from random import shuffle
from drafts.snakedraft import SnakeDraft
from drafts.player import Player

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", default=2019, type=str, help="Which year's player data to use")
    parser.add_argument("--teams", default='./data/teams.txt', type=argparse.FileType('r'),
                        help="File that contains list of strategies")
    parser.add_argument("--shuffle", default=False, action='store_true',
                        help="Shuffle strategies before starting the draft?")
    args = parser.parse_args()

    raw_players = json.load(open(f'./data/stats_{args.year}.json', 'r'))
    players = [Player(**p) for p in raw_players]

    strategy_names = [name.strip() for name in args.teams.readlines()]
    if len(players) < 6:
        print('Must have at least 6 teams')
        exit(1)

    if args.shuffle:
        shuffle(strategy_names)

    draft = SnakeDraft(players, strategy_names)
    draft.run()
    print('draft_pos', 'strategy_name', 'total_value', sep=',')
    for t in sorted(draft.teams(), key=lambda t: t.total_value, reverse=True):
        print(f'{t.draft_pos}', t.strategy_name, t.total_value, sep=',')
