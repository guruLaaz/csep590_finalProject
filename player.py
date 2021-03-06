from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    position: str
    value: float

    def __eq__(self, other):
        return (type(other) is type(self)) and (self.id == other.id)

    def __hash__(self):
        return hash(self.id)

    def is_forward(self):
        return self.position == 'C' or self.position == 'LW' or self.position == 'RW' or self.position == "FWD"
