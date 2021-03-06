from player import Player
from strategy import RoundBasedStrategy


class Ordered(RoundBasedStrategy):
    """
    Picks the best fowards, then best defensemen, then best goaltenders available
    """

    def __init__(self, *args, **kwargs):
        super(Ordered, self).__init__(*args, **kwargs)

    def pick(self, remaining_players: [Player], num_picks_until_next_turn: int):
        best_ForwardPlayer = None
        best_ForwardValue = 0

        best_DefensePlayer = None
        best_DefenseValue = 0

        best_GoaltenderPlayer = None
        best_GoaltenderValue = 0

        for p in remaining_players:
            if p.is_forward():
                if p.value >= best_ForwardValue:
                    best_ForwardPlayer = p
                    best_ForwardValue = p.value

            if p.position == "D":
                if p.value >= best_DefenseValue:
                    best_DefensePlayer = p
                    best_DefenseValue = p.value

            if p.position == "G":
                if p.value >= best_GoaltenderValue:
                    best_GoaltenderPlayer = p
                    best_GoaltenderValue = p.value

        if best_ForwardPlayer != None:
            return best_ForwardPlayer

        if best_DefensePlayer != None:
            return best_DefensePlayer

        return best_GoaltenderPlayer
