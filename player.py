from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    position: str
    value: str

    def __hash__(self):
        return hash(self.id)

    def is_forward(self):
        return self.position == 'C' or self.position == 'LW' or self.position == 'RW' or self.position == "FWD"
