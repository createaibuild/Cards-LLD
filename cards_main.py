#!/usr/bin/env python3
"""Interactive console application for a shuffled deck of cards."""

from __future__ import annotations

import sys
from typing import List

from cards import Deck, EmptyDeckError, Player


BANNER = """
╔══════════════════════════════════════════╗
║           DECK OF CARDS                  ║
║   Shuffle · Deal · Play from the console ║
╚══════════════════════════════════════════╝
"""

MENU = """
  1. New unshuffled deck
  2. Shuffle (Fisher-Yates)
  3. Deal N cards to each player
  4. Deal all remaining cards fairly
  5. Show remaining cards
  6. Show player hands
  7. Demo: shuffle and deal 5-card hands
  0. Exit
"""


def prompt(message: str) -> str:
    try:
        return input(message).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        sys.exit(0)


def prompt_int(message: str, minimum: int = 1, maximum: int | None = None) -> int:
    while True:
        raw = prompt(message)
        try:
            value = int(raw)
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if value < minimum:
            print(f"  Must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"  Must be at most {maximum}.")
            continue
        return value


def print_hands(players: List[Player]) -> None:
    if not players:
        print("  No players yet. Deal first.")
        return
    print()
    for player in players:
        print(f"  {player.format_hand()}")
    print()


def print_remaining(deck: Deck, preview: int = 13) -> None:
    print(f"\n  {deck.remaining} card(s) left.")
    if deck.remaining == 0:
        return
    shown = deck.peek(min(preview, deck.remaining))
    print("  Top (next to be dealt): " + "  ".join(str(c) for c in shown))
    if deck.remaining > preview:
        print(f"  … and {deck.remaining - preview} more")
    print()


def collect_players() -> List[Player]:
    count = prompt_int("  How many players? ", minimum=1, maximum=52)
    players: List[Player] = []
    for i in range(1, count + 1):
        name = prompt(f"  Player {i} name [{f'Player {i}'}]: ")
        players.append(Player(name or f"Player {i}"))
    return players


def run_demo() -> None:
    deck = Deck()
    print(f"\n  Fresh deck: {deck.remaining} cards")
    print("  Order before shuffle (first 13):")
    print("   ", "  ".join(str(c) for c in list(deck)[:13]))

    deck.shuffle()
    print("\n  Shuffled with Fisher-Yates.")
    print("  New top 13:")
    print("   ", "  ".join(str(c) for c in deck.peek(13)))

    players = [Player("Alice"), Player("Bob"), Player("Carol")]
    deck.deal_hands(players, cards_per_hand=5)
    print("\n  Dealt 5 cards to 3 players (round-robin):")
    print_hands(players)
    print(f"  Remaining in deck: {deck.remaining}")


def main() -> None:
    print(BANNER)
    deck = Deck()
    players: List[Player] = []

    while True:
        print(MENU)
        print(f"  Deck: {deck.remaining} remaining · Players: {len(players)}")
        choice = prompt("  Choose: ")

        if choice == "0":
            print("Goodbye.")
            return

        if choice == "1":
            deck.reset()
            players = []
            print("  New 52-card deck created. Hands cleared.")

        elif choice == "2":
            if not deck:
                print("  Deck is empty. Create a new deck first.")
                continue
            deck.shuffle()
            print(f"  Shuffled {deck.remaining} card(s) with Fisher-Yates.")

        elif choice == "3":
            if not deck:
                print("  Deck is empty. Create a new deck first.")
                continue
            players = collect_players()
            cards_each = prompt_int(
                "  Cards per player? ",
                minimum=1,
                maximum=deck.remaining,
            )
            try:
                deck.deal_hands(players, cards_each)
            except EmptyDeckError as exc:
                print(f"  {exc}")
                continue
            print(f"  Dealt {cards_each} card(s) to {len(players)} player(s).")
            print_hands(players)

        elif choice == "4":
            if not deck:
                print("  Deck is empty. Create a new deck first.")
                continue
            players = collect_players()
            deck.deal_all(players)
            extras = len(players[0]) - len(players[-1]) if players else 0
            print("  Dealt every remaining card, round-robin.")
            if extras:
                print("  Leftover cards went to the earlier seats.")
            print_hands(players)

        elif choice == "5":
            print_remaining(deck)

        elif choice == "6":
            print_hands(players)

        elif choice == "7":
            run_demo()

        else:
            print("  Unknown option.")


if __name__ == "__main__":
    main()
