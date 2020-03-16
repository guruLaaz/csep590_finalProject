from auction.truthful_bidder import TruthfulBidder
from player import Player
from strategy import AuctionKnowledge, StrategyConfig
from team import Team


def get_current_round(teams: [Team]):
    picks = sum([len(t.players) for t in teams])
    return picks // len(teams)


# never nominate players ranked before the following "round"
NOMINATION_ROUND_OFFSET = 8


class ForceEarlyStrategy(TruthfulBidder):
    """
    Nominate non-top players first and make other players lose money & use up spots.
    """

    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        super().__init__(draft_pos, strategy_config)
        self.initial_players = sorted(self.initial_players, key=lambda p: p.value, reverse=True)
        self.nominations = set(self.initial_players[NOMINATION_ROUND_OFFSET * self.num_teams:])

    def should_force_early(self, round) -> bool:
        return True

    def nominate(self, remaining_players: [Player], teams: [Team]) -> (Player, int):
        remaining_players = sorted(remaining_players, key=lambda p: p.value, reverse=True)

        for p in remaining_players:
            if p in self.nominations:
                return p, 1


def get_bid(self, nominated_player: Player, knowledge: AuctionKnowledge, teams: [Team]) -> int:
    if knowledge.nominating_team.draft_pos == self.draft_pos:
        return 0

    return super(ForceEarlyStrategy, self).get_bid(nominated_player, knowledge, teams)
