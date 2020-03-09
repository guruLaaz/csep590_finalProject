import copy
from typing import List

from strategies.strategy import Strategy


class NormalDraft(object):
    strategies: List[Strategy]

    def __init__(self, players, strategies, teams):
        self.num_players = len(players)
        self.players = players

        self.num_teams = len(teams)
        self.strategies = strategies
        self.teams = teams

    def run(self):
        num_rounds = 20
        remaining_players = set(copy.copy(self.players))
        for rnd in range(num_rounds):
            for i in range(self.num_teams):
                team = self.teams[i]
                strategy = self.strategies[i]

                # apply strategy to select player to draft
                players = team.eligible_players(list(remaining_players))
                chosen_player = strategy.pick(players)
                if chosen_player is None:
                    raise ValueError(
                        f'Team {team.draft_pos} Must select a player')

                # update team & remove player from future selections
                self.teams[i].sign_player(chosen_player)
                remaining_players.remove(chosen_player)
