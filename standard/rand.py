from player import Player
from strategy import RoundBasedStrategy
from random import choice


class Rand(RoundBasedStrategy):
    """
    Returns a player at random.
    """

    def __init__(self, *args, **kwargs):
        super(Rand, self).__init__(*args, **kwargs)

    def pick(self, remaining_players: [Player], num_picks_until_next_turn: int):
        return choice(remaining_players)
