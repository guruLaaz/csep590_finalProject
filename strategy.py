from dataclasses import dataclass
from typing import List

from player import Player


@dataclass
class StrategyConfig(object):
    num_teams: int
    players: List[Player]
    team_config: dict
    initial_budget: float = float('inf')


class Strategy(object):
    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        self.draft_pos = draft_pos

        self.num_teams = strategy_config.num_teams
        self.initial_players = strategy_config.players
        self.team_config = strategy_config.team_config

    def __hash__(self):
        return hash(self.draft_pos)


class RoundBasedStrategy(Strategy):
    """
    Defines an agent that will standard.
    """

    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        super(RoundBasedStrategy, self).__init__(draft_pos, strategy_config)

    def pick(self, remaining_players, num_picks_until_next_turn):
        """
        Select a player to draft. Given remaining players only include
        who are eligible for a team. For example, if the team using this
        strategy already has the maximum allowed Forwards, remaining_players
        will not include any Forwards.
        """
        pass


class AuctionStrategy(Strategy):
    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        super(AuctionStrategy, self).__init__(draft_pos, strategy_config)
        self.initial_budget = strategy_config.initial_budget
