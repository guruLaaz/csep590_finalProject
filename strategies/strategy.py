from drafts.player import Player
from typing import List

class Strategy(object):
    """
    Defines an agent that will drafts.
    """

    def __init__(self, num_teams: int, draft_pos: int, players: List[Player], teamConfig: dict):
        self.team_config = teamConfig
        self.num_teams = num_teams
        self.draft_pos = draft_pos
        self.initial_players = players

    def pick(self, remaining_players, num_picks_until_next_turn):
        """
        Select a player to draft. Given remaining players only include
        who are eligible for a team. For example, if the team using this
        strategy already has the maximum allowed Forwards, remaining_players
        will not include any Forwards.
        """
        pass

    def __hash__(self):
        return hash(self.draft_pos)
