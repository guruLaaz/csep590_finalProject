from dataclasses import dataclass
from typing import List

from player import Player
from team import Team


@dataclass
class StrategyConfig(object):
    num_teams: int
    players: List[Player]
    team_config: dict
    initial_budget: int = float('inf')


class Strategy(object):
    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        self.draft_pos = draft_pos

        self.num_teams = strategy_config.num_teams
        self.initial_players = strategy_config.players
        self.team_config = strategy_config.team_config
        self.num_players_per_team = sum(self.team_config.values())

    def __eq__(self, other):
        return (type(other) is type(self)) and (self.draft_pos == other.draft_pos)

    def __hash__(self):
        return hash(self.draft_pos)


class RoundBasedStrategy(Strategy):
    """
    Defines an agent that will standard.
    """

    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        super(RoundBasedStrategy, self).__init__(draft_pos, strategy_config)

    def pick(self, remaining_players: [Player], num_picks_until_next_turn: int) -> Player:
        """
        Select a player to draft. Given remaining players only include
        who are eligible for a team. For example, if the team using this
        strategy already has the maximum allowed Forwards, remaining_players
        will not include any Forwards.
        """
        pass


@dataclass
class AuctionKnowledge:
    bid_limit: int
    curr_high_bid: int
    cur_high_bidding_team: Team
    nominating_team: Team


class AuctionStrategy(Strategy):
    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        super(AuctionStrategy, self).__init__(draft_pos, strategy_config)
        self.initial_budget = strategy_config.initial_budget

    def nominate(self, remaining_players: [Player], teams: [Team]) -> (Player, int):
        """
        Nominate a player that will be drafted -- note: a nomination is equivalent
        to a $1 bid.

        :param remaining_players: Players to choose from (this list will only include positions
                                  that can be drafted by the team)
        """
        pass

    def get_bid(self, nominated_player: Player, knowledge: AuctionKnowledge, teams: [Team]) -> int:
        """
        Return bid for given nominated_player or None if you do not wish to acquire this player.

        Bids lower than the current maximum bid price (provided in the knowledge) are ignored.
        """
        pass

    def player_acquired(self, winning_team: Team, winning_bid: int):
        """
        Notifies strategy that a player was acquired. The current strategy won if
        team#draft_pos == self.draft_pos
        """
        if winning_team.draft_pos == self.draft_pos:
            print(f"Team {self.draft_pos} won with {winning_bid}!")
