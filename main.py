import argparse
import importlib
import inspect
import json
from random import shuffle

from drafts.drafts import NormalDraft, SnakeDraft
from drafts.player import Player
from drafts.team import HockeyTeam, HockeyTeamWithForwards
from strategies.strategy import Strategy

def RunDraft(draftYear):
    
    TeamClazz = team_types[args.team_type]
    # load player data
    raw_players = json.load(open(f'./data/stats_{draftYear}.json', 'r'))
    players = TeamClazz.transform_players([Player(**p) for p in raw_players])

    # initialize teams
    strategies = []
    teams = []
    for i, name in enumerate(strategy_names):
        team = TeamClazz(i, name)
        teams.append(team)
        strategies.append(new_strategy(name, num_teams, i, players, team.team_config))

    DraftClazz = draft_types[args.draft_type]
    draft = DraftClazz(players, strategies, teams)
    draft.run()
    print(f"\r\n *** Draft {draftYear} ***\r\n\r\n" "draft_pos", 'strategy_name', 'total_value', sep=',')
    sortedDraft = sorted(draft.teams, key=lambda t: t.total_value, reverse=True)
    for t in sortedDraft:
        print(f'{t.draft_pos}', t.strategy_name, t.total_value, sep=',')

    return sortedDraft

def new_strategy(strategy_name, *args, **kwargs):
    """
    Dynamically initialize strategy classes.

    Initializes a subclass of Strategy found in module "strategy.<name>".
    If there are more than one of such classes, returns an arbitrary one.
    (There should only one such class in each file anyway).

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

draft_types = {
    'snake': SnakeDraft,
    'normal': NormalDraft,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--year", default=None, type=str, help="Which year's player data to use")
    parser.add_argument("--team_type", choices=team_types.keys(), default='hockey', help='Type of team')
    parser.add_argument("--teams", default='./data/teams.txt', type=argparse.FileType('r'),
                        help="File that contains list of strategies")
    parser.add_argument("--shuffle", default=True, action='store_true',
                        help="Shuffle strategies before starting the draft?")
    parser.add_argument("--draft_type", default="normal", choices=draft_types.keys(),
                        help="Type of draft to use")
    args = parser.parse_args()

    # validate arguments
    strategy_names = [name.strip() for name in args.teams.readlines()]
    num_teams = len(strategy_names)
    if num_teams < 6:
        print('Must have at least 6 teams')
        exit(1)

    if args.shuffle:
        shuffle(strategy_names)

    years = [2016, 2017, 2018, 2019]
    sortedDrafts = []
    finalPayoffs = {}

    if (args.year != None):
        RunDraft(2019)
    else:
        for year in years:
            sortedDrafts.append(RunDraft(year))

        # now get the average of each draft
        for draft in sortedDrafts:
            for strat in draft:
                key = f"{strat.strategy_name}:{strat.draft_pos}"
                if key in finalPayoffs:
                    finalPayoffs[key] += strat.total_value
                else:
                    finalPayoffs[key] = strat.total_value

        for strat in finalPayoffs:
            #print("PAYOFF ",strat, " is total of ", finalPayoffs[strat])
            finalPayoffs[strat] /= len(years)
            #print("AVERAGE PAYOFF ",strat, " is ", finalPayoffs[strat])


        print("\r\n*********** TOTAL DRAFT PAYOFFS ***********\r\n")

        for final in sorted(finalPayoffs, key=finalPayoffs.get, reverse=True):
            print(final, finalPayoffs[final])