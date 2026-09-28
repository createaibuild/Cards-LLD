"""A standard 52-card deck with Fisher-Yates shuffle and dealing."""

from __future__ import annotations

import secrets
from typing import Iterable, List, Sequence

from cards.card import Card
from cards.player import Player
from cards.rank import Rank
from cards.suit import Suit


class EmptyDeckError(ValueError):
    """Raised when a deal is requested from an empty or exhausted deck."""


class Deck:
    """A standard deck of 52 unique cards.

    Cards are dealt from the top (end of the internal list) so that
    shuffle + pop remains O(1) per card.
    """

    def __init__(self, cards: Iterable[Card] | None = None) -> None:
        if cards is None:
            self._cards: List[Card] = [
                Card(rank, suit) for suit in Suit for rank in Rank
            ]
        else:
            self._cards = list(cards)

    def __len__(self) -> int:
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def __bool__(self) -> bool:
        return bool(self._cards)

    def __repr__(self) -> str:
        return f"Deck({len(self._cards)} cards)"

    @property
    def remaining(self) -> int:
        """Number of cards still in the deck."""
        return len(self._cards)

    def reset(self) -> None:
        """Restore a full unshuffled 52-card deck."""
        self._cards = [Card(rank, suit) for suit in Suit for rank in Rank]

    def reset_deck(self) -> None:
        """Alias for ``reset`` (common interview / design-doc name)."""
        self.reset()

    def shuffle(self) -> None:
        """Shuffle in place using Fisher-Yates (Knuth) shuffle.

        Each of the n! permutations is equally likely. Uses
        ``secrets.randbelow`` so the index choice is cryptographically
        uniform — important for a fair deal.
        """
        cards = self._cards
        for i in range(len(cards) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            cards[i], cards[j] = cards[j], cards[i]

    def deal(self, n: int = 1) -> List[Card]:
        """Deal ``n`` cards from the top of the deck.

        Raises:
            ValueError: if ``n`` is not a positive integer.
            EmptyDeckError: if fewer than ``n`` cards remain.
        """
        if not isinstance(n, int) or n < 1:
            raise ValueError("n must be a positive integer")
        if n > len(self._cards):
            raise EmptyDeckError(
                f"Cannot deal {n} card(s); only {len(self._cards)} remain"
            )
        dealt = self._cards[-n:]
        del self._cards[-n:]
        dealt.reverse()
        return dealt

    def deal_one(self) -> Card:
        """Deal a single card from the top."""
        return self.deal(1)[0]

    def draw_card(self) -> Card:
        """Return the top card and remove it from the deck."""
        return self.deal_one()

    def deal_hands(
        self,
        players: Sequence[Player],
        cards_per_hand: int,
    ) -> None:
        """Deal ``cards_per_hand`` cards to each player, round-robin.

        Round-robin dealing (one card at a time around the table) is
        the fair casino/home-game convention and keeps any residual
        positional bias evenly distributed.
        """
        if not players:
            raise ValueError("at least one player is required")
        if cards_per_hand < 1:
            raise ValueError("cards_per_hand must be a positive integer")

        needed = len(players) * cards_per_hand
        if needed > len(self._cards):
            raise EmptyDeckError(
                f"Need {needed} cards for {len(players)} player(s) "
                f"× {cards_per_hand}; only {len(self._cards)} remain"
            )

        for _ in range(cards_per_hand):
            for player in players:
                player.receive(self.deal_one())

    def deal_all(self, players: Sequence[Player]) -> None:
        """Distribute every remaining card fairly, round-robin.

        If the deck does not divide evenly, earlier seats receive one
        extra card — the standard leftover convention.
        """
        if not players:
            raise ValueError("at least one player is required")
        while self._cards:
            for player in players:
                if not self._cards:
                    break
                player.receive(self.deal_one())

    def peek(self, n: int = 5) -> List[Card]:
        """Return up to ``n`` top cards without removing them (for display)."""
        if n < 1:
            return []
        top = self._cards[-n:]
        return list(reversed(top))
