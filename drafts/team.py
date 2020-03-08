from drafts.player import Player


class Team(object):
    def __init__(self, draft_pos, strategy_name, remaining_pos):
        self.draft_pos = draft_pos
        self.strategy_name = strategy_name
        self.players = []
        self.remaining_pos = remaining_pos
        self.total_value = 0

    def sign_player(self, player: Player):
        self.total_value += player.value
        if self.remaining_pos[player.position] == 0:
            raise ValueError(
                f'Team {self.draft_pos} has no remaining spots for position {player.position}')

        self.remaining_pos[player.position] -= 1
        self.players.append(player)

    def can_sign_player(self, player: Player):
        return self.remaining_pos[player.position] > 0

    def eligible_players(self, remaining_players):
        return list(filter(self.can_sign_player, remaining_players))

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
