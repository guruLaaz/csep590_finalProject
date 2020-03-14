from drafts.player import Player
from .strategy import Strategy
from itertools import groupby, chain
from operator import itemgetter

class BaselineByWorstPeer(Strategy):
    """
    1. Baseline = Average points expected for the worst peer of j (a viable peer is the worst player likely to get picked in the draft, at j's position)
    """
    baselinePerPosition = {}

    def __init__(self, *args, **kwargs):
        super(BaselineByWorstPeer, self).__init__(*args, **kwargs)

        #init the dict

        for key in self.team_config.keys():
            # get all players that match the position
            playersAtThatPosition = {}
            for p in self.initial_players:
                if p.position == key:
                    playersAtThatPosition[p] = p.value

            # sort the players at that position by value
            sortedPlayers = sorted(playersAtThatPosition, key=playersAtThatPosition.get, reverse=True)

            # now get the worst player that is likely to be drafted for each position
            totalSlotsForPosition = self.team_config[key] * self.num_teams
            worstPeer = sortedPlayers[totalSlotsForPosition - 1]
            #print("Worst peer for position ", key, "is ", worstPeer.name)
            self.baselinePerPosition[key] = worstPeer.value

    def pick(self, remaining_players: [Player]):
        max_value = float('-inf')

        # rank players by how much they're above the baseline
        greatestBaseline = -1000000
        playerToPick = remaining_players[0]

        for p in remaining_players:
            baseline = p.value - self.baselinePerPosition[p.position]
            if baseline > greatestBaseline:
                playerToPick = p
                greatestBaseline = baseline

        #print("returning player ", playerToPick.name, ". value: ", playerToPick.value, ". baseline is ", greatestBaseline)
        return playerToPick