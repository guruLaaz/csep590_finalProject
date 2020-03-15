from drafts.player import Player
from .strategy import RoundBasedStrategy


class Best(RoundBasedStrategy):
    """
    Returns the remaining player with the highest value.
    """

    def __init__(self, *args, **kwargs):
        super(Best, self).__init__(*args, **kwargs)

    def pick(self, remaining_players: [Player], num_picks_until_next_turn: int):
        max_value = float('-inf')
        best_player = None
        for p in remaining_players:
            if p.value > max_value:
                best_player = p
                max_value = p.value

        return best_player
