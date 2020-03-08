class Strategy(object):
    """
    Defines an agent that will drafts.
    """

    def __init__(self, num_teams: int, draft_position: int):
        self.num_teams = num_teams
        self.draft_position = draft_position

    def pick(self, remaining_players):
        """
        Select a player to draft
        """
        pass
