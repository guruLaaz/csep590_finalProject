import copy
from dataclasses import dataclass
from typing import List

from player import Player
from strategy import Strategy
from team import Team


@dataclass
class DraftConfig(object):
    players: List[Player]
    strategies: List[Strategy]
    teams: List[Team]
    players_per_team: int


class Draft(object):
    strategies: List[Strategy]
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

    def next_turn(self, remaining_players: List[Player]) -> (int, Player):
        pass  # return -1, None
