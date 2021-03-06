from player import Player
from strategy import AuctionKnowledge, AuctionStrategy, StrategyConfig
from team import Team


class TruthfulBidder(AuctionStrategy):
    """
    Figure out total value expected by drafting the best player available, use that total to
    bid proportionally.
    """

    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        super().__init__(draft_pos, strategy_config)

        sorted_players = sorted(self.initial_players, key=lambda p: p.value, reverse=True)
        target_players = sorted_players[self.draft_pos::self.num_teams][:self.num_players_per_team]
        self.optimistic_total = sum([p.value for p in target_players])

    def nominate(self, remaining_players: [Player], teams: [Team]) -> (Player, int):
        return sorted(remaining_players, key=lambda p: p.value, reverse=True)[0], 1

    def get_bid(self, nominated_player: Player, knowledge: AuctionKnowledge, teams: [Team]) -> int:
        return int((nominated_player.value / self.optimistic_total) * self.initial_budget)

    def player_acquired(self, team: Team, winning_bid: int):
        super(TruthfulBidder, self).player_acquired(team, winning_bid)
