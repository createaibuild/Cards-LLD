"""Playing-card ranks."""

from enum import Enum


class Rank(Enum):
    """Standard ranks from Ace (low) through King."""

    ACE = ("A", 1)
    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("J", 11)
    QUEEN = ("Q", 12)
    KING = ("K", 13)

    def __init__(self, label: str, numeric: int) -> None:
        self.label = label
        self.numeric = numeric

    def __str__(self) -> str:
        return self.label

    def __repr__(self) -> str:
        return f"Rank.{self.name}"
