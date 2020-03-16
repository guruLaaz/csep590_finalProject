from copy import copy
from random import shuffle
from typing import List

from draft import Draft, DraftConfig
from player import Player
from strategy import AuctionKnowledge, AuctionStrategy


class LiveAuction(Draft):
    strategies: List[AuctionStrategy]

    def __init__(self, config: DraftConfig):
        super().__init__(config)
        self.round = 0
        self.pick = 0

    def next_turn(self, remaining_players: List[Player]) -> (int, Player, int):
        while True:
            # figure out whose turn it is
            team_idx = self.pick % self.num_teams

            if not self.teams[team_idx].is_done_drafting():
                nominated_player, nominee_bid = self.get_nomination(remaining_players, team_idx)
                winning_team_idx, winning_bid = self.run_auction(nominated_player, team_idx,
                                                                 nominee_bid)

                self.pick += 1
                self.round = self.pick // self.num_teams
                return winning_team_idx, nominated_player, winning_bid
            else:
                self.pick += 1
                self.round = self.pick // self.num_teams

    def get_nomination(self, remaining_players, team_idx) -> (Player, int):
        # use strategy to figure out what player the team chooses
        eligible_players = self.teams[team_idx].draftable_players(remaining_players)
        nominated_player, nominee_bid = self.strategies[team_idx] \
            .nominate(eligible_players, copy(self.teams))
        assert nominee_bid >= 1, f"Minimum nomination bid is $1 but was {nominee_bid}"
        return nominated_player, nominee_bid

    def run_auction(self, player: Player, nominating_team_idx, nominating_bid: int) -> (int, int):
        curr_winning_team, curr_high_bid = nominating_team_idx, nominating_bid

        while True:
            # give each team a chance to get_bid for the player
            bids = []
            for team_idx in range(self.num_teams):
                team = self.teams[team_idx]
                if not team.can_draft_player(player):
                    continue

                # assume team needs $1 to get_bid to fill up for every remaining spot
                limit = team.remaining_budget - team.num_spots_remaining() + 1
                teams = [copy(t) for t in self.teams]
                team_bid = self.strategies[team_idx] \
                    .get_bid(player,
                             AuctionKnowledge(limit, curr_high_bid, teams[curr_winning_team],
                                              teams[nominating_team_idx]),
                             teams)

                bid = None if team_bid is None else int(min(limit, team_bid))
                if bid is not None and bid > curr_high_bid:
                    bids.append((team_idx, bid))

            if len(bids) == 0:
                break

            # at least one get_bid beats the current highest get_bid
            # shuffle the get_bid so that we arbitrarily break ties
            shuffle(bids)
            curr_winning_team, curr_high_bid = max(bids, key=lambda b: b[0])

        return curr_winning_team, curr_high_bid
