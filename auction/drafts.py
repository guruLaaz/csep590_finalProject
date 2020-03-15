import copy
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

    def next_turn(self, remaining_players: List[Player]) -> (int, Player):
        # figure out whose turn it is
        team_idx = self.pick % self.num_teams

        nominated_player, nominee_bid = self.run_nomination(remaining_players, team_idx)
        winning_team_idx, winning_bid = self.run_auction(nominated_player, team_idx, nominee_bid)
        self.teams[winning_team_idx].add_player(nominated_player, winning_bid)

        # update counters for next pick
        self.pick += 1
        self.round = self.pick // self.num_teams

        return winning_team_idx, nominated_player

    def run_nomination(self, remaining_players, team_idx):
        # use strategy to figure out what player the team chooses
        eligible_players = self.teams[team_idx].draftable_players(remaining_players)

        nominated_player, nominee_bid = self.strategies[team_idx].nominate(eligible_players)

        if nominee_bid < 1:
            raise AssertionError(f"Minimum get_bid is $1, team {team_idx} get_bid {nominee_bid}")

        if nominated_player is None:
            raise AssertionError(f"Team {team_idx} must nominate a player")

        return nominated_player, nominee_bid

    def run_auction(self, player: Player, nominating_team_idx, nominating_bid: int):
        curr_high_bid = nominating_bid
        curr_high_bid_team_idx = nominating_team_idx

        while True:
            # give each team a chance to get_bid for the player

            bids = []
            for i in range(self.num_teams):
                team = self.teams[i]

                # assume team needs $1 to get_bid to fill up for every remaining spot
                bid_limit = team.remaining_budget - team.num_spots_remaining() + 1
                bid = self.strategies[i].get_bid(player,
                                                 AuctionKnowledge(bid_limit, curr_high_bid,
                                                                  self.teams[curr_high_bid_team_idx]),
                                                 [copy.copy(t) for t in self.teams])

                if bid is not None and bid > curr_high_bid:
                    bids.append((max(bid, bid_limit), i))

            if bids:
                # at least one get_bid beats the current highest get_bid
                # shuffle the get_bid so that we arbitrarily break ties
                curr_high_bid, curr_high_bid_team_idx = max(shuffle(bids), key=lambda b: b[0])
            else:
                break

        return curr_high_bid_team_idx, curr_high_bid
