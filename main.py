import argparse
import json
from random import shuffle
from drafts.snakedraft import SnakeDraft
from drafts.normaldraft import NormalDraft
from strategies.strategy import Strategy
from drafts.player import Player
from drafts.team import HockeyTeam, HockeyTeamWithForwards
import importlib
import inspect


def new_strategy(strategy_name, *args, **kwargs):
    """
    Dynamically initialize strategy classes.

    Initializes class found in module "strategy.<name>". If there
    are more than one classes, returns an arbitrary one.
    (There should only one class in each file, for now).

    Passes all arguments as-is.
    """
    mod = importlib.import_module(f"strategies.{strategy_name}")
    for _, obj in inspect.getmembers(mod):
        if inspect.isclass(obj) and issubclass(obj, Strategy):
            return obj(*args, **kwargs)


team_types = {
    'hockey': HockeyTeam,
    'hockey_forwards': HockeyTeamWithForwards
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--year", default=2019, type=str, help="Which year's player data to use")
    parser.add_argument("--team_type", choices=team_types.keys(), default='hockey', help='Type of team')
    parser.add_argument("--teams", default='./data/teams.txt', type=argparse.FileType('r'),
                        help="File that contains list of strategies")
    parser.add_argument("--shuffle", default=False, action='store_true',
                        help="Shuffle strategies before starting the draft?")
    parser.add_argument("--draft_type", default="normaldraft", type=str, help="Type of draft to use (normaldraft vs snakedraft)")
    args = parser.parse_args()

    # validate arguments
    strategy_names = [name.strip() for name in args.teams.readlines()]
    num_teams = len(strategy_names)
    if num_teams < 6:
        print('Must have at least 6 teams')
        exit(1)

    if args.shuffle:
        shuffle(strategy_names)

    TeamClazz = team_types[args.team_type]
    # load player data
    raw_players = json.load(open(f'./data/stats_{args.year}.json', 'r'))
    players = TeamClazz.transform_players([Player(**p) for p in raw_players])

    # initialize teams
    strategies = []
    teams = []
    for i, name in enumerate(strategy_names):
        strategies.append(new_strategy(name, num_teams, i))
        teams.append(TeamClazz(i, name))

    if args.draft_type == "snakedraft":
        draft = SnakeDraft(players, strategies, teams)
    else:
        draft = NormalDraft(players, strategies, teams)

    draft.run()
    print('draft_pos', 'strategy_name', 'total_value', sep=',')
    for t in sorted(draft.teams, key=lambda t: t.total_value, reverse=True):
        print(f'{t.draft_pos}', t.strategy_name, t.total_value, sep=',')