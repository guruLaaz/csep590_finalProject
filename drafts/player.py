from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    position: str
    value: str

    def __hash__(self):
        return hash(self.id)
