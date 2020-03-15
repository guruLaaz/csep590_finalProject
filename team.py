from copy import copy

from player import Player


class Team(object):
    """
    Keeps track of each team
    """

    def __init__(self, draft_pos, strategy_name, budget=float('inf'), team_config={}):
        self.team_config = team_config
        self.draft_pos = draft_pos
        self.strategy_name = strategy_name
        self.players = []

        self.total_value = 0
        self.remaining_budget = budget
        self.remaining_spots_per_pos = copy(team_config)

    def add_player(self, player: Player, spent=0):
        if self.remaining_spots_per_pos[player.position] == 0:
            raise ValueError(
                f'Team {self.draft_pos} has no remaining spots for position {player.position}')

        if self.remaining_budget < spent:
            raise ValueError(f'Team {self.draft_pos} has no budget to spend {spent}')

        self.total_value += player.value
        self.remaining_budget -= spent
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
        super().__init__(draft_pos, strategy_name, team_config={
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

    @staticmethod
    def number_players_in_team():
        return 20


class HockeyTeam(Team):
    def __init__(self, draft_pos, strategy_name):
        super().__init__(draft_pos, strategy_name, team_config={
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

    @staticmethod
    def number_players_in_team():
        return 20
