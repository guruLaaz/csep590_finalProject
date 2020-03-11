from drafts.player import Player
from copy import copy


class Team(object):
    """
    Keeps track of each team
    """

    def __init__(self, draft_pos, strategy_name, teamConfig):
        self.team_config = teamConfig
        self.draft_pos = draft_pos
        self.strategy_name = strategy_name
        self.remaining_spots_per_pos = copy(teamConfig)
        self.players = []
        self.total_value = 0

    def add_player(self, player: Player):
        self.total_value += player.value
        if self.remaining_spots_per_pos[player.position] == 0:
            raise ValueError(
                f'Team {self.draft_pos} has no remaining spots for position {player.position}')

        self.remaining_spots_per_pos[player.position] -= 1
        self.players.append(player)

    def is_done_drafting(self):
        return self.num_spots_remaining() == 0

    def num_spots_remaining(self):
        remaining = 0
        for pos, num_remaining in self.remaining_spots_per_pos.items():
            remaining += num_remaining

        return remaining

    def team_config(self):
        return self.team_config

    def draftable_players(self, remaining_players: [Player]):
        return list(filter(self._can_draft_player, remaining_players))

    def _can_draft_player(self, player: Player):
        return self.remaining_spots_per_pos[player.position] > 0

    def __hash__(self):
        return hash(self.draft_pos)

    def __str__(self):
        return f"Team: Draft Pos: {self.draft_pos}," \
               f"Strategy: {self.strategy_name}," \
               f"Value: {self.total_value}," \
               f"Players: {self.players}"


class HockeyTeamWithForwards(Team):
    def __init__(self, draft_pos, strategy_name):
        super().__init__(draft_pos, strategy_name, {
            'FWD': 12,
            'D': 6,
            'G': 2,
        })

    @staticmethod
    def transform_players(players: [Player]):
        """
        Treat C, LW, and RW as a single forward position
        """

        def combine_forwards(p: Player):
            if p.position == 'C' or p.position == 'LW' or p.position == 'RW':
                p.position = 'FWD'

            return p

        return [combine_forwards(p) for p in players]


class HockeyTeam(Team):
    def __init__(self, draft_pos, strategy_name):
        super().__init__(draft_pos, strategy_name, {
            'C': 4,
            'LW': 4,
            'RW': 4,
            'D': 6,
            'G': 2,
        })

    @staticmethod
    def transform_players(players: [Player]):
        """
        Don't do anything
        """
        return players
