from drafts.player import Player
from .strategy import Strategy
from itertools import groupby, chain
from operator import itemgetter

class BaselineByAverage(Strategy):
    """
    1. Baseline = Average points expected for the peers of j
    """
    baselinePerPosition = {}
    numberOfPlayersPerPosition = {}

    def __init__(self, *args, **kwargs):
        super(BaselineByAverage, self).__init__(*args, **kwargs)

        #now initialize each baseline, per position
        for player in self.initialPlayers:
            if player.position in self.baselinePerPosition:  
                self.baselinePerPosition[player.position] += player.value  
            else:
                self.baselinePerPosition[player.position] = player.value

            if player.position in self.numberOfPlayersPerPosition:  
                self.numberOfPlayersPerPosition[player.position] += 1
            else:
                self.numberOfPlayersPerPosition[player.position] = 1
                        
        # baseline: average of all peers of a player
        for key in self.baselinePerPosition.keys():
            numberOfPlayersAtPosition = self.numberOfPlayersPerPosition[key]
            #print(numberOfPlayersAtPosition, " at position ", key)
            totalPointsAtPosition = self.baselinePerPosition.get(key)
            #print(totalPointsAtPosition, " at position ", key)            
            #print("average point per player: ", totalPointsAtPosition / numberOfPlayersAtPosition)
            self.baselinePerPosition[key] = totalPointsAtPosition / numberOfPlayersAtPosition

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