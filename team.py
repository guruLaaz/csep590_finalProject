from copy import copy

from player import Player

DEFAULT_BUDGET = 200


class Team(object):
    """
    Keeps track of each team
    """

    def __init__(self, draft_pos, strategy_name, budget: int = DEFAULT_BUDGET, team_config=None):
        if team_config is None:
            raise ValueError("Required param team_config is missing")

        self.team_config = team_config
        self.draft_pos = draft_pos
        self.strategy_name = strategy_name
        self.players = []

        self.total_value = 0
        self.remaining_budget = budget
        self.remaining_spots_per_pos = copy(team_config)

    def add_player(self, player: Player, cost=0):
        """
        :param player: Player that was acquired by the team
        :param cost: How much the player costed (nonzero in auction drafts, zero by default)
        """
        if self.remaining_spots_per_pos[player.position] == 0:
            raise ValueError(
                f'Team {self.draft_pos} has no remaining spots for position {player.position}')

        if self.remaining_budget < cost:
            raise ValueError(f'Team {self.draft_pos} has no budget to spend {cost}')

        self.total_value += player.value
        self.remaining_budget -= cost
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
        return list(filter(self.can_draft_player, remaining_players))

    def can_draft_player(self, player: Player):
        return self.remaining_spots_per_pos[player.position] > 0

    def __eq__(self, other):
        return (type(other) is type(self)) and (self.draft_pos == other.draft_pos)

    def __hash__(self):
        return hash(self.draft_pos)

    def __str__(self):
        return f"Team: Draft Pos: {self.draft_pos}," \
               f"Strategy: {self.strategy_name}," \
               f"Value: {self.total_value}," \
               f"Players: {self.players}"


class HockeyTeamWithForwards(Team):
    def __init__(self, draft_pos, strategy_name, budget=DEFAULT_BUDGET):
        super().__init__(draft_pos, strategy_name, budget, team_config={
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
    def __init__(self, draft_pos, strategy_name, budget=DEFAULT_BUDGET):
        super().__init__(draft_pos, strategy_name, budget, team_config={
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
