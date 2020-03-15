from typing import List

from draft import Draft, DraftConfig
from player import Player


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
