import copy
from typing import List
from dataclasses import dataclass

from strategies.strategy import RoundBasedStrategy
from .player import Player
from .team import Team


@dataclass
class DraftConfig():
    players: List[Player]
    strategies: List[RoundBasedStrategy]
    teams: List[Team]
    players_per_team: int


class Draft(object):
    strategies: List[RoundBasedStrategy]
    teams: List[Team]

    def __init__(self, config: DraftConfig):
        self.num_players = len(config.players)
        self.players = config.players

        self.num_teams = len(config.strategies)
        self.strategies = config.strategies
        self.teams = config.teams
        self.players_per_team = config.players_per_team

    def run(self):
        teams_remaining = set([t.draft_pos for t in self.teams])
        remaining_players = set(copy.copy(self.players))

        while teams_remaining:
            # noinspection PyTupleAssignmentBalance
            team_idx, player = self.next_turn(list(remaining_players))
            if player is None:
                raise AssertionError(
                    f'Team {team_idx} using strategy {self.teams[team_idx].strategy_name} made an invalid selection')

            team = self.teams[team_idx]
            team.add_player(player)
            remaining_players.remove(player)

            if team.is_done_drafting():
                teams_remaining.remove(team.draft_pos)

    def next_turn(self, remaining_players: List[Player]):
        pass  # return -1, None


class NormalDraft(Draft):

    def __init__(self, config: DraftConfig):
        super().__init__(config)
        self.round = 0
        self.pick = 0

    def next_turn(self, remaining_players: List[Player]):
        # figure out whose turn it is
        team_idx = self.pick % self.num_teams

        # use strategy to figure out what player the team chooses
        eligible_players = self.teams[team_idx].draftable_players(remaining_players)

        # in a normal draft, the agent gets to pick every N rounds, where N is the number of agents.
        # unless we are in the last round, in that case return -1.
        if self.round == self.players_per_team - 1:
            num_picks_until_next_turn = -1
        else:
            num_picks_until_next_turn = self.num_teams

        player = self.strategies[team_idx].pick(eligible_players, num_picks_until_next_turn)

        # update counters for next pick
        self.pick += 1
        self.round = self.pick // self.num_teams

        return team_idx, player


class SnakeDraft(Draft):
    def __init__(self, config: DraftConfig):
        super().__init__(config)
        self.round = 0
        self.pick = 0

    def next_turn(self, remaining_players: List[Player]):
        # figure out whose turn it is
        team_idx = self.pick % self.num_teams
        flipOrder = self.round % 2 == 1

        if flipOrder:  # flip the order
            team_idx = self.num_teams - 1 - team_idx
            num_picks_until_next_turn = team_idx * 2 + 1
        else:
            num_picks_until_next_turn = (self.num_teams - team_idx) * 2 - 1

        # use strategy to figure out what player the team chooses
        eligible_players = self.teams[team_idx].draftable_players(remaining_players)
        player = self.strategies[team_idx].pick(eligible_players, num_picks_until_next_turn)

        # update counters for next pick
        self.pick += 1
        self.round = self.pick // self.num_teams

        return team_idx, player
