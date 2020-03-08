import copy
import importlib
import inspect
from typing import List

from drafts.player import Player
from strategies.strategy import Strategy


class HockeyTeam(object):
    def __init__(self, draft_pos, strategy_name):
        self.draft_pos = draft_pos
        self.strategy_name = strategy_name
        self.total_value = 0
        self.players = []
        self.remaining = {
            'FWD': 12,
            'D': 6,
            'G': 2,
        }

    def sign_player(self, player: Player):
        self.total_value += player.value
        if self.remaining[player.position] == 0:
            raise ValueError(f'Team {self.draft_pos} has no remaining spots for position {player.position}')

        self.remaining[player.position] -= 1
        self.players.append(player)

    def eligible_players(self, remaining_players):
        return filter(self._can_sign_player, remaining_players)

    def _can_sign_player(self, player):
        return self.remaining[player.position] > 0

    def __hash__(self):
        return hash(self.draft_pos)

    def __str__(self):
        return f"Team: Draft Pos: {self.draft_pos}," \
               f"Strategy: {self.strategy_name}," \
               f"Value: {self.total_value}," \
               f"Players: {self.players}"


class SnakeDraft(object):
    strategies: List[Strategy]

    def __init__(self, players, strategy_names):
        self.num_players = len(players)
        self.players = players

        self.num_teams = len(strategy_names)
        self.strategy_names = strategy_names
        self.strategies = [new_strategy(strategy_name, num_teams=self.num_teams, draft_position=i)
                           for i, strategy_name in enumerate(strategy_names)]

        self.hockey_teams = [HockeyTeam(i + 1, s) for i, s in enumerate(self.strategy_names)]

    def run(self):
        num_rounds = 20
        remaining_players = set(copy.copy(self.players))
        for i in range(num_rounds):
            for j in range(self.num_teams):
                snaked_idx = j if i % 2 == 0 else (self.num_teams - j - 1)
                eligible_players = self.hockey_teams[snaked_idx].eligible_players(list(remaining_players))
                chosen = self.strategies[snaked_idx].pick(eligible_players)
                self.hockey_teams[snaked_idx].sign_player(chosen)
                remaining_players.remove(chosen)

    def teams(self):
        return self.hockey_teams


def new_strategy(strategy_name, *args, **kwargs):
    mod = importlib.import_module(f"strategies.{strategy_name}")
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        return obj(*args, **kwargs)
