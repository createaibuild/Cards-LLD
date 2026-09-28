"""Playing-card suits."""

from enum import Enum


class Suit(Enum):
    """The four standard suits, ordered Clubs < Diamonds < Hearts < Spades."""

    CLUBS = ("Clubs", "♣")
    DIAMONDS = ("Diamonds", "♦")
    HEARTS = ("Hearts", "♥")
    SPADES = ("Spades", "♠")

    def __init__(self, label: str, symbol: str) -> None:
        self.label = label
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f"Suit.{self.name}"
