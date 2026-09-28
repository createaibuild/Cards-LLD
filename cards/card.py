"""A single playing card."""

from functools import total_ordering

from cards.rank import Rank
from cards.suit import Suit


@total_ordering
class Card:
    """An immutable card identified by rank and suit."""

    __slots__ = ("_rank", "_suit")

    def __init__(self, rank: Rank, suit: Suit) -> None:
        if not isinstance(rank, Rank):
            raise TypeError("rank must be a Rank")
        if not isinstance(suit, Suit):
            raise TypeError("suit must be a Suit")
        self._rank = rank
        self._suit = suit

    @property
    def rank(self) -> Rank:
        return self._rank

    @property
    def suit(self) -> Suit:
        return self._suit

    def __str__(self) -> str:
        return f"{self._rank}{self._suit}"

    def __repr__(self) -> str:
        return f"Card({self._rank!r}, {self._suit!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (self._rank, self._suit) == (other._rank, other._suit)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (self._rank.numeric, self._suit.name) < (other._rank.numeric, other._suit.name)

    def __hash__(self) -> int:
        return hash((self._rank, self._suit))
