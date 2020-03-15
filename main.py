import argparse
import importlib
import inspect
import json
import copy
from random import shuffle

from drafts.drafts import NormalDraft, SnakeDraft
from drafts.player import Player
from drafts.team import HockeyTeam, HockeyTeamWithForwards
from strategies.strategy import Strategy
from draft_results import DraftResults, TrialResult
from collections import Counter


def run_trial(TeamClazz, DraftClazz, year, players, strategy_names):
    # initialize teams & strategies
    strategies = []
    teams = []
    numberOfPlayersPerTeam = TeamClazz.number_players_in_team()

    for i, name in enumerate(strategy_names):
        team = TeamClazz(i, name)
        teams.append(team)
        strategies.append(new_strategy(name, num_teams, i, players, team.team_config))

    draft = DraftClazz(players, strategies, teams)
    draft.run()
    ranked_teams = sorted(draft.teams, key=lambda t: t.total_value, reverse=True)

    results = []
    for rank, team in enumerate(ranked_teams):
        results.append(TrialResult(year, team.strategy_name, team.total_value, rank, team.draft_pos))

    return results


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
    years = [2016, 2017, 2018, 2019]
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--years", default=years, type=int, nargs="*", help="Which years player data to use")
    parser.add_argument("--num_trials", default=10, type=int, help="Number of trials to run")
    parser.add_argument("--team_type", choices=team_types.keys(), default='hockey', help='Type of team')
    parser.add_argument("--teams", default='./data/teams.txt', type=argparse.FileType('r'),
                        help="File that contains list of strategies")
    parser.add_argument("--shuffle", default=True, action='store_true',
                        help="Shuffle strategies before starting the draft?")
    parser.add_argument("--draft_type", default="normal", choices=draft_types.keys(),
                        help="Type of draft to use")
    args = parser.parse_args()

    # validate arguments
    given_strategy_names = [name.strip() for name in args.teams.readlines()]
    num_teams = len(given_strategy_names)
    if num_teams < 6:
        print('Must have at least 6 teams')
        exit(1)

    print("Scenario")
    print(f"Num trials: {args.num_trials}")
    print(f"Draft type: {args.draft_type}")
    print(f"Shuffle?: {args.shuffle}")
    print(f"Team type: {args.team_type}")
    print(f"Strategies: {Counter(given_strategy_names)}")
    print("====")

    TeamClazz = team_types[args.team_type]
    DraftClazz = draft_types[args.draft_type]

    overall_results = DraftResults()
    for year in args.years:
        raw_players = json.load(open(f'./data/stats_{year}.json', 'r'))
        players = TeamClazz.transform_players([Player(**p) for p in raw_players])

        for _ in range(0, args.num_trials):
            trial_strategy_names = copy.copy(given_strategy_names)
            if args.shuffle:
                shuffle(trial_strategy_names)

            trial_results = run_trial(TeamClazz, DraftClazz, year, copy.copy(players), trial_strategy_names)
            overall_results.add_trials(trial_results)

    overall_results.summary_by_strategy()
