class Strategy(object):
    """
    Defines an agent that will drafts.
    """

    def __init__(self, num_teams: int, draft_pos: int):
        self.num_teams = num_teams
        self.draft_pos = draft_pos

    def pick(self, remaining_players):
        """
        Select a player to draft. Given remaining players only include
        who are eligible for a team. For example, if the team using this
        strategy already has the maximum allowed Forwards, remaining_players
        will not include any Forwards.
        """
        pass
