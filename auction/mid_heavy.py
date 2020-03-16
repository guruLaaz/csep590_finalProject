from collections import defaultdict

from player import Player
from strategy import AuctionKnowledge, AuctionStrategy, StrategyConfig
from team import Team


class MidHeavy(AuctionStrategy):
    """
    Always try to win the top player in each position, no matter what it takes.
    """

    def __init__(self, draft_pos, strategy_config: StrategyConfig, rounds=(2, 5)):
        super().__init__(draft_pos, strategy_config)
        self.sorted_players = sorted(self.initial_players, key=lambda p: p.value, reverse=True)

        i = 0
        best_of_each_pos = defaultdict(list)
        remaining_top = set(strategy_config.team_config.keys())
        while remaining_top:
            player = self.sorted_players[i]
            if len(best_of_each_pos[player.position]) < num_top_players_per_pos:
                best_of_each_pos[player.position].append(player)
            elif player.position in remaining_top:
                remaining_top.remove(player.position)
            i += 1

        self.players_to_target = sorted([p for ps in best_of_each_pos.values() for p in ps],
                                        key=lambda p: p.value,
                                        reverse=True)

    def nominate(self, remaining_players: [Player], teams: [Team]) -> (Player, int):
        players = set(remaining_players)
        for target in self.players_to_target:
            if target in players:
                return target, 1

        return max(remaining_players, key=lambda p: p.value), 1

    def get_bid(self, nominated_player: Player, knowledge: AuctionKnowledge, teams: [Team]) -> int:
        if nominated_player in self.players_to_target:
            # always try to win the players to target
            return knowledge.curr_high_bid + 1

        # just get nominations eventually
        return 0
