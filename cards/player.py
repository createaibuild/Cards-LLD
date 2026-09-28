"""A player who holds a hand of cards."""

from __future__ import annotations

from typing import Iterable, List

from cards.card import Card


class Player:
    """Named player with an ordered hand."""

    def __init__(self, name: str) -> None:
        if not name or not name.strip():
            raise ValueError("player name cannot be empty")
        self.name = name.strip()
        self._hand: List[Card] = []

    @property
    def hand(self) -> List[Card]:
        return list(self._hand)

    def __len__(self) -> int:
        return len(self._hand)

    def __repr__(self) -> str:
        return f"Player({self.name!r}, {len(self._hand)} cards)"

    def receive(self, card: Card) -> None:
        """Add a single card to the hand."""
        self._hand.append(card)

    def receive_many(self, cards: Iterable[Card]) -> None:
        """Add several cards to the hand."""
        self._hand.extend(cards)

    def clear_hand(self) -> None:
        """Discard the current hand."""
        self._hand.clear()

    def sorted_hand(self) -> List[Card]:
        """Return the hand sorted by rank, then suit."""
        return sorted(self._hand)

    def format_hand(self, sort: bool = True) -> str:
        cards = self.sorted_hand() if sort else self._hand
        if not cards:
            return f"{self.name}: (empty)"
        rendered = "  ".join(str(card) for card in cards)
        return f"{self.name} ({len(cards)}): {rendered}"
