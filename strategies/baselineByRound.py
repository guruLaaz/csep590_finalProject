from drafts.player import Player
from .strategy import Strategy
from itertools import groupby, chain
from operator import itemgetter

class BaselineByRound(Strategy):
    """
    1. Baseline reset every time we pick. The baseline for a player j is relative to the best peer of j
    that we estimate will be available for us to pick next round. The estimate assumes that other agents are
    picking the best players.
    """

    def __init__(self, *args, **kwargs):
        super(BaselineByRound, self).__init__(*args, **kwargs)

    def pick(self, remaining_players: [Player], numberOfRoundsUntilNextPick: int):

        # remaining players by their value
        sortedPlayers = sorted(remaining_players, key=lambda x: x.value, reverse=True)

        #print("BEST PLAYER THIS ROUND: ", sortedPlayers[0].name)

        if numberOfRoundsUntilNextPick == -1:
            #last pick of the draft
            return sortedPlayers[0]

        #split players by position
        playersByPosition = {}
        for p in sortedPlayers:
            if not p.position in playersByPosition:
                playersByPosition[p.position] = [] # init array
            
            playersByPosition[p.position].append(p)
            
        #baseline: the number of points that should still be available to us next time we pick a player, for each position
        baselineByPosition = []

        #adjust numberOfRoundsUntilNextPick to account for team balance

        #print("PICKING A PLAYER")

        for position in playersByPosition.keys():
            #print("looking at position ", position, " available in ", numberOfRoundsUntilNextPick, " rounds.")
            # get the player that we think we can still pick at that position N picks laters
            baselinePeer = None
            if len(playersByPosition[position]) < numberOfRoundsUntilNextPick:
                #print("there is only ", len(playersByPosition), " players at position ", position, " left")
                baselinePeer = playersByPosition[position][-1] #last element of the array
            else:
                baselinePeer = playersByPosition[position][numberOfRoundsUntilNextPick]

            #baseline is the diff between the best player at a position and his peer N picks laters
            #print(f"comparing {playersByPosition[position][0].name} {playersByPosition[position][0].value} with baseline {baselinePeer.name} {baselinePeer.value}")
            baseline = playersByPosition[position][0].value - baselinePeer.value
            
            pair = (position, baseline)
            baselineByPosition.append(pair)

        # Now get the position where the baseline is the biggest. This means that there is a large difference 
        # between a best player at a position and his peer available next round
        greatestBaseline = baselineByPosition[0]

        for baseline in baselineByPosition:
            #cost of not picking: diff between best player available at a position and his peer N rounds later
            if baseline[1] > greatestBaseline[1]:
                greatestBaseline = baseline        

        #print("Greatest baseline was for position ", greatestBaseline[0])
                
        #return the best player at the baseline's position
        return next(x for x in sortedPlayers if x.position == greatestBaseline[0])