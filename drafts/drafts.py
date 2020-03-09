import copy
from typing import List

from strategies.strategy import Strategy
from .player import Player
from .team import Team


class Draft(object):
    strategies: List[Strategy]
    teams: List[Team]

    def __init__(self, players, strategies, teams):
        self.num_players = len(players)
        self.players = players

        self.num_teams = len(strategies)
        self.strategies = strategies
        self.teams = teams

    def run(self):
        teams_remaining = set([t.draft_pos for t in self.teams])
        remaining_players = set(copy.copy(self.players))

        while teams_remaining:
            # noinspection PyTupleAssignmentBalance
            team_idx, player = self.next_turn(list(remaining_players))

            team = self.teams[team_idx]
            team.add_player(player)
            remaining_players.remove(player)

            if team.is_done_drafting():
                teams_remaining.remove(team.draft_pos)

    def next_turn(self, remaining_players: List[Player]):
        pass  # return -1, None


class NormalDraft(Draft):

    def __init__(self, players, strategies, teams):
        super().__init__(players, strategies, teams)
        self.round = 0
        self.pick = 0

    def next_turn(self, remaining_players: List[Player]):
        # figure out whose turn it is
        team_idx = self.pick % self.num_teams

        # use strategy to figure out what player the team chooses
        eligible_players = self.teams[team_idx].draftable_players(remaining_players)
        player = self.strategies[team_idx].pick(eligible_players)

        # update counters for next pick
        self.pick += 1
        self.round = self.pick % self.num_teams

        return team_idx, player


class SnakeDraft(Draft):
    def __init__(self, players, strategies, teams):
        super().__init__(players, strategies, teams)
        self.round = 0
        self.pick = 0

    def next_turn(self, remaining_players: List[Player]):
        # figure out whose turn it is
        team_idx = self.pick % self.num_teams
        if self.round % 2 == 1:  # flip the order
            team_idx = self.num_teams - 1 - team_idx

        # use strategy to figure out what player the team chooses
        eligible_players = self.teams[team_idx].draftable_players(remaining_players)
        player = self.strategies[team_idx].pick(eligible_players)

        # update counters for next pick
        self.pick += 1
        self.round = self.pick // self.num_teams

        return team_idx, player
