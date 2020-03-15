from player import Player
from strategy import AuctionKnowledge, AuctionStrategy, StrategyConfig
from team import Team


class NomineeWins(AuctionStrategy):
    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        super().__init__(draft_pos, strategy_config)

    def nominate(self, remaining_players: [Player]) -> (Player, int):
        """
        :param remaining_players:
        :return: Return most valued team for $1
        """
        return sorted(remaining_players, key=lambda p: p.value, reverse=True)[0], 1

    def get_bid(self, nominated_player: Player, knowledge: AuctionKnowledge, teams: [Team]) -> int:
        return None

    def player_acquired(self, team: Team, winning_bid: int):
        super(NomineeWins, self).player_acquired(team, winning_bid)
