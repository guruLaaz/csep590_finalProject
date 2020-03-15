import argparse
import copy
import importlib
import inspect
import json
import pkgutil
from collections import Counter
from random import shuffle

from draft import Draft, DraftConfig
from draft_results import DraftResults, TrialResult
from player import Player
from strategy import Strategy, StrategyConfig
from team import DEFAULT_BUDGET, HockeyTeam, HockeyTeamWithForwards


def load_clazzes():
    draft_clazz = {}
    strategy_clazz = {}

    for x in ['standard', 'auction']:
        for p in pkgutil.iter_modules(path=[x]):
            mod = importlib.import_module(f'{x}.{p[1]}')
            for _, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and issubclass(obj, Draft) and p[1] in obj.__module__:
                    draft_clazz[obj.__name__.lower().strip('draft')] = obj

                if inspect.isclass(obj) and issubclass(obj, Strategy) and p[1] in obj.__module__:
                    strategy_clazz[p[1]] = obj

    return draft_clazz, strategy_clazz


def new_draft(draft_type, *args, **kwargs):
    return draft_clazzes[draft_type](*args, **kwargs)


def new_strategy(strategy_name, *args, **kwargs):
    return strategy_clazzes[strategy_name](*args, **kwargs)


def run_trial(TeamClazz, DraftClazz, year, players, strategy_names, budget):
    # initialize teams & strategies
    strategies = []
    teams = []

    for draft_pos, strategy_name in enumerate(strategy_names):
        team = TeamClazz(draft_pos, strategy_name, budget=budget)
        teams.append(team)
        strategy_config = StrategyConfig(num_teams, players, team.team_config, budget)
        strategies.append(new_strategy(strategy_name, draft_pos, strategy_config))

    draft_config = DraftConfig(players, strategies, teams, TeamClazz.number_players_in_team())
    draft = DraftClazz(draft_config)
    draft.run()
    ranked_teams = sorted(draft.teams, key=lambda t: t.total_value, reverse=True)

    results = []
    for rank, team in enumerate(ranked_teams):
        results.append(
            TrialResult(year, team.strategy_name, team.total_value, rank, team.draft_pos))

    # print("\r\n**** DRAFT RESULT ****\r\n")
    # for t in ranked_teams:
    #     name = t.strategy_name
    #     print(f'{t.draft_pos}', name, t.total_value, sep=',')

    return results


team_types = {
    'hockey': HockeyTeam,
    'hockey_forwards': HockeyTeamWithForwards
}

draft_clazzes, strategy_clazzes = load_clazzes()

if __name__ == '__main__':
    years = [2016, 2017, 2018, 2019]
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--years", default=years, type=int, nargs="*",
                        help="Which years player data to use")
    parser.add_argument("--num_trials", default=10, type=int, help="Number of trials to run")
    parser.add_argument("--team_type", choices=team_types.keys(), default='hockey',
                        help='Type of team')
    parser.add_argument("--teams", default='./data/teams.txt', type=argparse.FileType('r'),
                        help="File that contains list of strategies")
    parser.add_argument("--shuffle", default=True, action='store_true',
                        help="Shuffle strategies before starting the draft?")
    parser.add_argument("--draft_type", default="normal", choices=draft_clazzes.keys(),
                        help="Type of draft to use")
    parser.add_argument("--budget", default=DEFAULT_BUDGET, type=int,
                        help="Initial budget for each time (only applies to auction drafts)")

    args = parser.parse_args()

    # validate arguments
    given_strategy_names = [name.strip() for name in args.teams.readlines()]
    for name in given_strategy_names:
        if name not in strategy_clazzes:
            raise ValueError(f'{name} is not a valid strategy for draft type {args.draft_type}')

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
    print("\nRunning trials...\n\n")

    TeamClazz = team_types[args.team_type]
    DraftClazz = draft_clazzes[args.draft_type]

    overall_results = DraftResults(num_teams)
    for year in args.years:
        raw_players = json.load(open(f'./data/stats_{year}.json', 'r'))
        players = TeamClazz.transform_players([Player(**p) for p in raw_players])

        for _ in range(0, args.num_trials):
            trial_strategy_names = copy.copy(given_strategy_names)
            if args.shuffle:
                shuffle(trial_strategy_names)

            trial_results = run_trial(TeamClazz, DraftClazz, year, copy.copy(players),
                                      trial_strategy_names,
                                      args.budget)

            overall_results.add_trials(trial_results)

    overall_results.summary_by_strategy()
