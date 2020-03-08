from drafts.player import Player
from .strategy import Strategy
from random import choice


class Rand(Strategy):
    """
    Returns the remaining player with the highest value.
    """

    def __init__(self, *args, **kwargs):
        super(Rand, self).__init__(*args, **kwargs)

    def pick(self, remaining_players: [Player]):
        return choice(remaining_players)
