from drafts.player import Player
from .strategy import RoundBasedStrategy
from itertools import groupby, chain
from operator import itemgetter
import math

class BaselineByRound(RoundBasedStrategy):
    """
    1. Baseline reset every time we pick. The baseline for a player j is relative to the best peer of j
    that we estimate will be available for us to pick next round. The estimate assumes that other agents are
    picking the best players.
    """

    def __init__(self, *args, **kwargs):
        super(BaselineByRound, self).__init__(*args, **kwargs)

        #from team_config, get how many players total are drafted
        self.total_players_drafted_per_team = 0
        for config in self.team_config:
            self.total_players_drafted_per_team += self.team_config[config]

    def pick(self, remaining_players: [Player], num_picks_until_next_turn: int):

        # remaining players by their value
        sorted_players = sorted(remaining_players, key=lambda x: x.value, reverse=True)

        if num_picks_until_next_turn == -1:
            #last pick of the draft
            return sorted_players[0]

        #split and sort players by position
        players_sorted_by_position = {}
        for p in sorted_players:
            if not p.position in players_sorted_by_position:
                players_sorted_by_position[p.position] = [] # init array
            
            players_sorted_by_position[p.position].append(p)
            
        #baseline: the number of points that should still be available to us next time we pick a player, for each position
        baseline_per_position = []
            
        for position in players_sorted_by_position.keys():
            # get the player that we think we can still pick at that position N picks laters
            #adjust to account for team balance, because we're looking at players that are likely to still be available next round
            #eg. let's say that a team has 12F, 6D and 2G composition, and there are 10 agents drafting. Then, we expect each 6F, 3D and 1G to be drafted
            #on average before we get to pick again (so a factor of 10/20 = 0.5 is applied on each position)
            adjustement_factor = self.num_teams / self.total_players_drafted_per_team
            #get the index in the array of the peer we think should be available next turn, on average. Round down.
            index_of_peer_available_next_turn = int(adjustement_factor * self.team_config[position])

            baseline_peer = None
            if len(players_sorted_by_position[position]) < num_picks_until_next_turn:
                assert false, "should not happen"
                baseline_peer = players_sorted_by_position[position][-1] #last element of the array
            else:
                baseline_peer = players_sorted_by_position[position][index_of_peer_available_next_turn]

            #baseline is the diff between the best player at a position and his peer we can pick next round
            baseline = players_sorted_by_position[position][0].value - baseline_peer.value
            
            pair = (position, baseline)
            baseline_per_position.append(pair)

        # Now get the position where the baseline is the biggest. This means that there is a large difference 
        # between a best player at a position and his peer available next round
        greatest_baseline = baseline_per_position[0]

        for baseline in baseline_per_position:
            #cost of not picking: diff between best player available at a position and his peer N rounds later
            if baseline[1] > greatest_baseline[1]:
                greatest_baseline = baseline        
                
        #return the best player at the baseline's position
        return next(x for x in sorted_players if x.position == greatest_baseline[0])