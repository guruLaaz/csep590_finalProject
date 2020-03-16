from player import Player
from strategy import AuctionKnowledge, AuctionStrategy, StrategyConfig
from team import Team


class TopHeavy(AuctionStrategy):
    def __init__(self, draft_pos, strategy_config: StrategyConfig):
        super().__init__(draft_pos, strategy_config)
        self.sorted_players = sorted(self.initial_players, key=lambda p: p.value, reverse=True)

        i = 0
        best_players = {}
        remaining_top = set(strategy_config.team_config.keys())
        while remaining_top:
            player = self.sorted_players[i]
            if player.position in remaining_top:
                best_players[player.position] = player
                remaining_top.remove(player.position)
            i += 1

        self.players_to_target = sorted(best_players.values(), key=lambda p: p.value, reverse=True)

    def nominate(self, remaining_players: [Player]) -> (Player, int):
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

    def player_acquired(self, team: Team, winning_bid: int):
        if team.draft_pos == self.draft_pos:
            print("Top heavy won!")
