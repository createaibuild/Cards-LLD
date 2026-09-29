#!/usr/bin/env python3
"""Generate two interview-prep PDFs from the cards and parking designs."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF


NAVY = (22, 42, 74)
TEAL = (16, 92, 110)
SLATE = (45, 55, 72)
MUTED = (95, 105, 120)
RULE = (200, 208, 216)
CODE_BG = (245, 247, 250)
CALL_BG = (232, 244, 248)
WARN_BG = (255, 246, 230)


class InterviewPDF(FPDF):
    def __init__(self, title: str, subtitle: str) -> None:
        super().__init__(format="A4", unit="mm")
        self.doc_title = title
        self.doc_subtitle = subtitle
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(16, 18, 16)
        self.set_title(title)
        self.set_author("OOP design notes")

    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, self.doc_title, align="L")
        self.set_draw_color(*RULE)
        self.line(16, 12, 194, 12)
        self.ln(8)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_draw_color(*RULE)
        self.line(16, 283, 194, 283)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, f"Technical interview notes   |   page {self.page_no()}", align="C")

    def cover(self, tagline: str) -> None:
        self.add_page()
        self.ln(28)
        self.set_fill_color(*NAVY)
        self.rect(16, 40, 178, 3, "F")
        self.ln(18)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*TEAL)
        self.cell(0, 8, "SYSTEM DESIGN  ·  OOP  ·  INTERVIEW PREP", align="L")
        self.ln(12)
        self.set_font("Helvetica", "B", 26)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 12, self.doc_title)
        self.ln(2)
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*SLATE)
        self.multi_cell(0, 7, self.doc_subtitle)
        self.ln(8)
        self.set_font("Helvetica", "I", 11)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 6, tagline)
        self.ln(10)
        self.set_fill_color(*CALL_BG)
        self.set_text_color(*SLATE)
        self.set_font("Helvetica", "", 10)
        box = (
            "How to use this document in an interview: start with the 90-second pitch, "
            "draw the class diagram, name the data structures and their complexities, "
            "then walk the core flow. Use the SOLID and follow-up sections when the "
            "interviewer pushes on extensibility."
        )
        self._box(box, CALL_BG)

    def h1(self, text: str) -> None:
        self.ln(4)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 8, text)
        self.set_draw_color(*TEAL)
        self.line(16, self.get_y(), 80, self.get_y())
        self.ln(4)

    def h2(self, text: str) -> None:
        self.ln(3)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*TEAL)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def h3(self, text: str) -> None:
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def p(self, text: str) -> None:
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*SLATE)
        self.multi_cell(0, 5.2, text)
        self.ln(1.5)

    def bullets(self, items: list[str], numbered: bool = False) -> None:
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*SLATE)
        for i, item in enumerate(items, start=1):
            mark = f"{i}." if numbered else "-"
            self.set_x(20)
            self.multi_cell(0, 5.2, f"{mark}  {item}")
            self.ln(0.6)
        self.ln(1)

    def say(self, text: str) -> None:
        self._box("SAY THIS:  " + text, CALL_BG)

    def watch(self, text: str) -> None:
        self._box("WATCH OUT:  " + text, WARN_BG)

    def code(self, text: str) -> None:
        self._box(text, CODE_BG, font=("Courier", 8.2), line=4.4)

    def _box(self, text: str, bg: tuple[int, int, int], font=("Helvetica", 9.2), line=5.0) -> None:
        if self.get_y() > 258:
            self.add_page()
        self.set_font(font[0], "", font[1])
        self.set_text_color(*SLATE)
        y = self.get_y()
        self.set_fill_color(*bg)
        self.set_xy(16, y)
        self.multi_cell(178, line, "  " + text, fill=True)
        end_y = self.get_y()
        self.set_fill_color(*TEAL)
        self.rect(16, y, 1.5, max(end_y - y, line), "F")
        self.set_y(end_y + 2)

    def kv_table(self, rows: list[tuple[str, str]]) -> None:
        col1 = 48
        col2 = 130
        self.set_font("Helvetica", "B", 8.5)
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        self.cell(col1, 7, "Topic", border=0, fill=True)
        self.cell(col2, 7, "What to say / what we did", border=0, fill=True, new_x="LMARGIN", new_y="NEXT")
        fill = False
        for left, right in rows:
            if self.get_y() > 265:
                self.add_page()
            self.set_font("Helvetica", "B", 8.5)
            self.set_text_color(*NAVY)
            bg = (240, 244, 248) if fill else (255, 255, 255)
            self.set_fill_color(*bg)
            y = self.get_y()
            self.multi_cell(col1, 5, left, fill=True)
            h1 = self.get_y() - y
            self.set_xy(16 + col1, y)
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(*SLATE)
            self.multi_cell(col2, 5, right, fill=True)
            h2 = self.get_y() - y
            self.set_y(y + max(h1, h2) + 0.5)
            fill = not fill
        self.ln(2)


def write_cards(path: Path) -> None:
    pdf = InterviewPDF(
        "Deck of 52 Cards",
        "Object-oriented design, Fisher-Yates shuffle, and fair dealing",
    )
    pdf.cover(
        "A classic low-level OOP interview. Interviewers want a clean model, "
        "an unbiased shuffle you can prove, and a deal that does not starve players."
    )

    pdf.h1("1. 90-second pitch")
    pdf.p(
        "I model the domain as four types: Suit and Rank are closed enums, Card is an "
        "immutable pair of those enums, and Deck owns a list of 52 unique cards. "
        "The top of the deck is the end of the list so a draw is O(1). Shuffle is "
        "in-place Fisher-Yates: for i from n-1 down to 1, swap i with a uniformly "
        "chosen j in 0..i. That produces each of the 52! permutations with equal "
        "probability. Deal is either draw_card() for one card or deal_hands() which "
        "walks the table round-robin so every player gets the same count and any "
        "positional bias is spread evenly."
    )
    pdf.say(
        "I would not shuffle with random.shuffle in an interview without saying that "
        "it is Fisher-Yates underneath. Implement it yourself so you can discuss "
        "uniformity and off-by-one bugs."
    )

    pdf.h1("2. Problem statement and requirements")
    pdf.h2("Functional")
    pdf.bullets(
        [
            "Represent a standard 52-card deck (13 ranks x 4 suits, no jokers unless asked).",
            "Shuffle the deck so every permutation is equally likely.",
            "Draw / deal one or more cards from the top.",
            "Deal N cards to P players fairly.",
            "Reset the deck to a full unshuffled pack.",
            "Optionally show remaining cards and player hands.",
        ]
    )
    pdf.h2("Non-functional / interview quality bar")
    pdf.bullets(
        [
            "Correctness of uniqueness: no duplicate cards after construct or shuffle.",
            "Unbiased randomization (do not use swap-with-rand(n) for every index).",
            "Clear ownership: Deck mutates itself; Card does not.",
            "Fail loudly on over-deal rather than returning None or wrapping around.",
            "O(1) draw, O(n) shuffle, O(1) extra memory.",
        ]
    )
    pdf.h2("Assumptions I would state out loud")
    pdf.bullets(
        [
            "Ace is low for display sort (value 1). If this is blackjack or poker, Ace may be high or dual.",
            "No jokers, no multiple decks, no cut card, unless the interviewer adds them.",
            "Players do not steal cards from each other; they only receive from the Deck.",
            "Fair deal means equal count, not equal strength of hands.",
        ]
    )

    pdf.h1("3. High-level design")
    pdf.h2("Class diagram (what to draw on the whiteboard)")
    pdf.code(
        "Suit  (enum)          Rank (enum)\n"
        "  CLUBS, DIAMONDS       ACE..KING\n"
        "  HEARTS, SPADES        label, numeric\n"
        "         \\              /\n"
        "          \\            /\n"
        "           Card (immutable)\n"
        "             rank, suit\n"
        "             eq / lt / hash\n"
        "                  |\n"
        "                  | composed of 52\n"
        "                  v\n"
        "                Deck\n"
        "             List[Card]  (top = end)\n"
        "             shuffle, draw_card, deal,\n"
        "             deal_hands, reset_deck\n"
        "                  |\n"
        "                  | deals to\n"
        "                  v\n"
        "               Player\n"
        "             name, hand[]"
    )
    pdf.p(
        "Composition, not inheritance: a Deck has Cards; a Card has a Suit and a Rank. "
        "There is no 'RedCard' subclass. Inheritance would be the wrong tool here."
    )
    pdf.h2("Module map in this repo")
    pdf.kv_table(
        [
            ("cards/suit.py", "Four suits with a print symbol and a label."),
            ("cards/rank.py", "Thirteen ranks. numeric is sort strength; value is reserved by Enum."),
            ("cards/card.py", "Immutable value object. Comparable and hashable."),
            ("cards/deck.py", "52-card owner. Shuffle, draw, deal, reset."),
            ("cards/player.py", "Named hand. Receives cards; does not draw from the deck itself."),
            ("cards_main.py", "Console UI. No domain rules live here."),
        ]
    )

    pdf.h1("4. Class responsibilities")
    pdf.h2("Suit and Rank")
    pdf.p(
        "Enums are the right type because the set is closed. You cannot construct a fifth "
        "suit. Each member carries display data (label/symbol) plus, for Rank, a numeric "
        "order. Rank.numeric is named that way on purpose: Enum already owns .value "
        "(the raw tuple). Mentioning this shows you have hit the Python enum footgun."
    )
    pdf.h2("Card")
    pdf.p(
        "A Card is a value object. Identity is the pair (rank, suit). After construction "
        "it cannot change -- slots plus read-only properties. That lets us put cards in a "
        "set to prove uniqueness, and sort a hand without mutating it. @total_ordering "
        "fills in >, <=, >= from __eq__ and __lt__."
    )
    pdf.code(
        "@total_ordering\n"
        "class Card:\n"
        "    __slots__ = ('_rank', '_suit')\n"
        "    def __eq__(self, other):\n"
        "        return (self._rank, self._suit) == (other._rank, other._suit)\n"
        "    def __lt__(self, other):\n"
        "        return (self._rank.numeric, self._suit.name) < (...)\n"
        "    def __hash__(self):\n"
        "        return hash((self._rank, self._suit))"
    )
    pdf.h2("Deck")
    pdf.p(
        "Deck is the aggregate root. It is the only type that may reorder or remove cards "
        "from the pack. Internal list _cards: index 0 is the bottom, the last index is "
        "the top. Construction is a Cartesian product: for each Suit, for each Rank, "
        "emit one Card. That is 4 * 13 = 52 and is automatically unique."
    )
    pdf.h2("Player")
    pdf.p(
        "Player is a separate aggregate so dealing is not 'return a list of lists'. The "
        "hand property returns a copy, so a caller cannot mutate the real hand. receive() "
        "is the only write path. This is Law of Demeter: Deck talks to Player, not to "
        "player._hand."
    )

    pdf.h1("5. Data structures")
    pdf.kv_table(
        [
            ("List[Card]", "Primary store. Contiguous, ordered, O(1) pop from end."),
            ("set(Card)", "Used in tests / as a talking point to prove 52 unique hashes."),
            ("Enum", "Closed vocabulary. Iteration order is declaration order."),
            ("Why not a queue?", "collections.deque is also O(1) pop. A list with top-at-end is enough and simpler to shuffle in place."),
            ("Why not a linked list?", "Shuffle needs random access. Linked list makes Fisher-Yates O(n^2)."),
        ]
    )
    pdf.p(
        "Interviewers sometimes ask 'how would you implement an infinite shoe' (blackjack). "
        "Answer: keep a factory that can reset/shuffle a new 52-card block, or hold several "
        "decks in one list (6 * 52) and shuffle once. The Card type does not change."
    )

    pdf.h1("6. Key algorithm: Fisher-Yates shuffle")
    pdf.p(
        "This is the part they will linger on. The modern (Knuth) Fisher-Yates shuffle:"
    )
    pdf.code(
        "def shuffle(self) -> None:\n"
        "    cards = self._cards\n"
        "    for i in range(len(cards) - 1, 0, -1):\n"
        "        j = secrets.randbelow(i + 1)   # uniform in 0..i inclusive\n"
        "        cards[i], cards[j] = cards[j], cards[i]"
    )
    pdf.h2("Why this is unbiased")
    pdf.p(
        "At step i, the card that lands in position i is chosen uniformly from the first "
        "i+1 cards (indices 0..i). Those i+1 cards are exactly the ones not yet finalized. "
        "By induction, every permutation has probability 1/n * 1/(n-1) * ... * 1/1 = 1/n!."
    )
    pdf.h2("The naive bug they expect you to name")
    pdf.p(
        "The broken version is: for i in 0..n-1: swap(i, randrange(n)). That is NOT uniform. "
        "Each swap has n choices, so you generate n^n outcomes mapped onto n! permutations. "
        "n^n is not divisible by n! for n>2, so some permutations get more mappings than "
        "others. Example they love: n=3, 27 outcomes into 6 permutations -- cannot be equal."
    )
    pdf.watch(
        "Off-by-one: randbelow(i) instead of randbelow(i+1) excludes swapping with self "
        "and skews the distribution. Inclusive upper bound is required."
    )
    pdf.h2("Why secrets.randbelow, not random.randint")
    pdf.p(
        "random is a PRNG (Mersenne Twister). Fine for games. secrets is CSPRNG, uniform "
        "over the range, and is the right story if the interviewer says 'this is an online "
        "casino'. In a board-game app, random.Random with an optional seed is better for "
        "tests. Mention both; pick based on the product."
    )
    pdf.h2("Complexity")
    pdf.bullets(
        [
            "Time: O(n) swaps, one pass. n = 52, effectively constant, but say O(n).",
            "Space: O(1) extra. In-place.",
            "random.shuffle in CPython is the same algorithm -- say so if asked to reuse stdlib.",
        ]
    )

    pdf.h1("7. Dealing cards")
    pdf.h2("draw_card / deal_one")
    pdf.p(
        "Pop from the tail. If the deck is empty, raise EmptyDeckError -- a dedicated "
        "exception, not a bare ValueError, so the UI can distinguish 'bad N' from 'deck dry'."
    )
    pdf.h2("deal(n)")
    pdf.p(
        "Slice the last n cards, delete them, reverse so the first returned card is the "
        "old top. This matches n calls to deal_one without n resizes of a tiny list."
    )
    pdf.h2("deal_hands(players, cards_per_hand) -- fair deal")
    pdf.p(
        "Round-robin: for each of N cards, walk every player once. Casino and home-game "
        "convention. Alternatives and why we rejected them:"
    )
    pdf.bullets(
        [
            "Give player 1 all N cards, then player 2: faster to slice, but if the shuffle "
            "had any residual clump, one player eats a whole run. Also feels unfair at a table.",
            "Randomly assign remaining cards: more code, same fairness if shuffle is already unbiased.",
        ]
    )
    pdf.p(
        "We pre-check players * N <= remaining. Fail before mutating any hand. That is "
        "transactional thinking -- say the word 'all-or-nothing'."
    )
    pdf.h2("deal_all")
    pdf.p(
        "Keep dealing round-robin until empty. Leftover cards go to earlier seats "
        "(standard leftover convention). Hand sizes differ by at most 1."
    )

    pdf.h1("8. OOP principles in this design")
    pdf.h2("Encapsulation")
    pdf.p(
        "Deck._cards, Card._rank/_suit, Player._hand are private. Callers use methods. "
        "Player.hand returns a copy so encapsulation is not a suggestion."
    )
    pdf.h2("Abstraction")
    pdf.p(
        "The console never builds Card(rank, suit) in a loop. It asks Deck to shuffle and "
        "deal. The 'how' of Fisher-Yates is hidden behind shuffle()."
    )
    pdf.h2("Composition over inheritance")
    pdf.p(
        "Card has-a Suit and Rank. Deck has-a list of Cards. We did not make SpadeCard "
        "subclasses. If the interviewer asks 'where is inheritance?', the honest answer "
        "is: this domain does not need it. Forcing it would violate YAGNI."
    )
    pdf.h2("Immutability as a design choice")
    pdf.p(
        "Cards never change identity. Only the Deck's order and the Player's hand change. "
        "That eliminates a class of bugs (a card in two hands that later 'changes suit')."
    )

    pdf.h1("9. SOLID principles")
    pdf.h2("S -- Single Responsibility")
    pdf.kv_table(
        [
            ("Suit / Rank", "Vocabulary only. No shuffle, no I/O."),
            ("Card", "Identity and comparison of one card."),
            ("Deck", "Pack lifecycle: build, shuffle, draw, reset."),
            ("Player", "Hold a hand. Does not know Fisher-Yates."),
            ("cards_main.py", "I/O and menu. If we add poker scoring, it does not go here."),
        ]
    )
    pdf.h2("O -- Open/Closed")
    pdf.p(
        "Adding a joker: introduce Rank.JOKER or a Joker card type and teach Deck to "
        "optionally include it. Existing shuffle and deal methods do not change. Adding "
        "a new game (poker hand evaluator) is a new module that reads Card.rank/suit -- "
        "Deck stays closed."
    )
    pdf.p(
        "Honest gap: Ace-high vs Ace-low is baked into Card.__lt__. A Strategy "
        "(comparator injected into sort) would be more OCP if we supported multiple games."
    )
    pdf.h2("L -- Liskov Substitution")
    pdf.p(
        "No inheritance hierarchy of cards, so LSP is vacuously true. If we later add "
        "Joker(Card), it must still hash/compare without breaking set(Deck). A joker with "
        "no suit must not crash __lt__."
    )
    pdf.h2("I -- Interface Segregation")
    pdf.p(
        "Python has no formal interface here, but the public surface is small: shuffle, "
        "draw_card, deal_hands, reset_deck. Peek is display-only. We do not force Player "
        "to implement shuffle."
    )
    pdf.h2("D -- Dependency Inversion")
    pdf.p(
        "cards_main depends on the Deck abstraction (public methods), not on the list "
        "layout. Deck depends on Card, not on the console. To unit-test shuffle, inject "
        "a tiny Deck([c1,c2,c3]) -- the constructor already accepts an iterable (test seam)."
    )

    pdf.h1("10. Design patterns")
    pdf.kv_table(
        [
            ("Value Object", "Card: equality by value, hashable, immutable."),
            ("Aggregate / Facade", "Deck is the only entry for pack operations. UI talks to Deck, not to the raw list."),
            ("Factory (lightweight)", "Deck.__init__ and reset() manufacture the 52-card product."),
            ("Iterator", "__iter__ / __len__ / __bool__ make Deck a collection."),
            ("Decorator (stdlib)", "@total_ordering synthesizes the missing comparisons."),
            ("Null/empty object? No", "We raise EmptyDeckError instead of returning a dummy card. Prefer fail-fast in interviews unless they ask for Optional."),
        ]
    )
    pdf.p(
        "Patterns we deliberately did not use: Singleton (a global deck is hostile to tests), "
        "Observer (no UI subscribers in the domain), Strategy for shuffle (one correct "
        "algorithm). Name the unused patterns -- it shows taste, not just a checklist."
    )

    pdf.h1("11. Complexity cheat sheet")
    pdf.kv_table(
        [
            ("Build / reset", "O(52) = O(1) for a standard deck, O(n) generally."),
            ("shuffle", "O(n) time, O(1) extra space."),
            ("draw_card", "O(1)."),
            ("deal(k)", "O(k)."),
            ("deal_hands(P, N)", "O(P*N) draws, plus an O(1) capacity check."),
            ("sorted hand", "O(h log h) using Card.__lt__."),
        ]
    )

    pdf.h1("12. Trade-offs and extensions")
    pdf.bullets(
        [
            "Multiple decks / shoe: Deck(cards=Deck()._cards * 6) then shuffle. Track depletion and reshuffle threshold (cut card).",
            "Seeded shuffle for replay tests: accept an rng argument on shuffle(rng=).",
            "Ace high: pass a key= to sorted(), or a Comparator strategy.",
            "Thread safety: a lock around shuffle+deal if two tables share a shoe. Usually one deck per table, no lock.",
            "Persistence: serialize remaining cards as (rank, suit) pairs. Card is already a value object.",
            "UI: cards_main is a client. A web API would call the same Deck methods.",
        ]
    )

    pdf.h1("13. Follow-up questions (with answers)")
    pdf.h3("Why not random.shuffle?")
    pdf.p(
        "It is Fisher-Yates. Implementing it yourself lets you discuss uniformity. In "
        "production I would use random.shuffle or secrets and a comment."
    )
    pdf.h3("How do you test a shuffle?")
    pdf.p(
        "Invariant tests: same multiset of cards, length 52, no duplicates. Statistical "
        "test: over many trials, P(card C is on top) ~= 1/52. Chi-square if they want rigor. "
        "Never assert a specific order after shuffle."
    )
    pdf.h3("Is your shuffle cryptographically secure?")
    pdf.p(
        "The algorithm is unbiased given a uniform index. Security is a property of the "
        "RNG. secrets.randbelow is the right choice for gambling; random is fine for solitaire."
    )
    pdf.h3("How would you deal so player 1 is not advantaged?")
    pdf.p(
        "If the shuffle is unbiased, first card is as random as any other. Round-robin is "
        "about social fairness and breaking clumps, not about fixing a biased RNG."
    )
    pdf.h3("Can two threads draw at once?")
    pdf.p(
        "Not safely. List pop is not atomic across check-and-pop. Either give each table "
        "its own Deck or lock the draw path."
    )
    pdf.h3("Model a discard pile?")
    pdf.p(
        "Second list on Deck, or a DiscardPile object. reset() can be 'shuffle discard "
        "back into deck' -- that is a new method, not a change to Card."
    )

    pdf.h1("14. Whiteboard script (10 minutes)")
    pdf.bullets(
        [
            "Minute 1: requirements + Ace-low assumption + no jokers.",
            "Minute 2-3: draw Suit, Rank, Card, Deck, Player. Say composition.",
            "Minute 4-5: list as the store, top at the end, O(1) draw.",
            "Minute 6-7: write Fisher-Yates. Call out the naive n^n bug.",
            "Minute 8: deal_hands round-robin + all-or-nothing check.",
            "Minute 9: SOLID in one breath (SRP of Deck vs Card, OCP for jokers).",
            "Minute 10: extensions -- shoe, seeded RNG, Ace-high comparator.",
        ],
        numbered=True,
    )

    pdf.h1("15. Common mistakes to avoid")
    pdf.bullets(
        [
            "Using inheritance for suits (RedCard / BlackCard) with no behavior difference.",
            "Shuffle via sort(key=random) -- biased and O(n log n).",
            "Returning the same list from Player.hand (leaks mutability).",
            "Silent empty draw (return None) without saying Optional.",
            "Forgetting that Enum.value is reserved in Python.",
            "Claiming 'O(1) shuffle' because n=52. Say O(n), then 'n is 52'.",
        ]
    )

    pdf.output(path)


def write_parking(path: Path) -> None:
    pdf = InterviewPDF(
        "Scalable Parking Lot",
        "Multi-floor OOP design, nearest-spot assignment, HashMaps and heaps",
    )
    pdf.cover(
        "A classic object-oriented design interview. They want vehicle polymorphism, "
        "O(1) lookups, a clear park/unpark flow, and a story for adding floors, "
        "spot types, and pricing without rewriting the lot."
    )

    pdf.h1("1. 90-second pitch")
    pdf.p(
        "A ParkingLot is a composition of floors, each floor a list of ParkingSpots. "
        "Vehicles are a small hierarchy -- Bike, Car, Truck -- that advertise a required "
        "spot size. A bike may take a larger stall; a truck may not take a smaller one. "
        "On park I pick the nearest compatible stall: lowest floor, then lowest spot "
        "number. I do not scan the garage. I keep a min-heap of free stall ids per size, "
        "plus HashMaps from plate to ticket and ticket id to ticket. Park and unpark are "
        "O(log n) for the heap and O(1) for the maps. Unpark closes the Ticket, which "
        "owns fee calculation, and pushes the stall back onto the heap."
    )
    pdf.say(
        "Lead with data structures. 'I would put vehicles in a list and for-loop for a "
        "free spot' is the junior answer. HashMap + heap is the expected upgrade."
    )

    pdf.h1("2. Problem statement and requirements")
    pdf.h2("Functional")
    pdf.bullets(
        [
            "Multiple floors, each with a configurable mix of SMALL / MEDIUM / LARGE spots.",
            "Vehicle types: bike, car, truck -- different minimum sizes.",
            "park_vehicle(vehicle) -> Ticket, assigning the nearest compatible spot.",
            "unpark_vehicle(ticket_id) -> closed Ticket with fee.",
            "get_available_spots() -- free counts by floor and size.",
            "Reject a plate that is already parked. Reject a full-compatible-lot.",
        ]
    )
    pdf.h2("Non-functional")
    pdf.bullets(
        [
            "Park / unpark / 'is this plate inside?' must be fast as the garage grows.",
            "Adding a floor or a new vehicle type should not rewrite ParkingLot.park_vehicle.",
            "Clear domain exceptions, not boolean flags, for full / duplicate / unknown ticket.",
            "Fee policy isolated so hourly vs daily vs EV surcharge can change.",
        ]
    )
    pdf.h2("Assumptions to say first")
    pdf.bullets(
        [
            "Nearest = (floor ascending, spot number ascending). Spot 1 on a floor is closest to the entrance.",
            "A vehicle may use a larger stall if no exact size is free and that larger stall is still nearer.",
            "One vehicle per plate. One open ticket per vehicle.",
            "Minimum one hour billed, then ceil to the next hour. Bike $1, car $3, truck $6.",
            "Single-threaded unless they ask. I will mention locking as an extension.",
            "No reservations, no EV chargers, no handicap-only spots -- until they add them.",
        ]
    )

    pdf.h1("3. High-level design")
    pdf.h2("Class diagram")
    pdf.code(
        "Vehicle  <--+-- Bike    required_size = SMALL\n"
        "            +-- Car     required_size = MEDIUM\n"
        "            +-- Truck   required_size = LARGE\n"
        "                 |\n"
        "                 | parks in\n"
        "                 v\n"
        "           ParkingSpot  (floor, number, size, vehicle?)\n"
        "                 ^\n"
        "                 | 1..*\n"
        "           ParkingFloor\n"
        "                 ^\n"
        "                 | 1..*\n"
        "           ParkingLot   <<facade>>\n"
        "             park_vehicle / unpark_vehicle\n"
        "             get_available_spots\n"
        "                 |\n"
        "                 | issues\n"
        "                 v\n"
        "               Ticket   (id, vehicle, spot, in, out, fee)\n"
        "\n"
        "create_vehicle(type, plate)  <<factory>>"
    )
    pdf.h2("Module map in this repo")
    pdf.kv_table(
        [
            ("parking/types.py", "VehicleType, SpotSize, compatibility table, hourly rates."),
            ("parking/vehicle.py", "Vehicle hierarchy + create_vehicle factory."),
            ("parking/spot.py", "One stall. Occupancy and can_fit."),
            ("parking/floor.py", "Builds numbered spots. Counts free stalls."),
            ("parking/ticket.py", "Entry/exit timestamps and fee."),
            ("parking/lot.py", "Indexes, nearest assignment, park/unpark."),
            ("parking_main.py", "Console only. Domain stays in the package."),
        ]
    )

    pdf.h1("4. Class responsibilities")
    pdf.h2("Vehicle / Bike / Car / Truck")
    pdf.p(
        "Identity is the license plate (normalized to uppercase). Subclasses do not override "
        "behavior; they declare class-level vehicle_type and required_size. That is "
        "polymorphism by data: ParkingLot never writes if isinstance(v, Truck). It asks "
        "v.required_size. Adding Van(required_size=MEDIUM) is a new subclass plus one "
        "factory map entry."
    )
    pdf.h2("SpotSize and compatibility")
    pdf.p(
        "SMALL=1, MEDIUM=2, LARGE=3. A spot can_fit a vehicle when spot.size >= required. "
        "COMPATIBLE_SIZES is the inverted index the heap walker uses:"
    )
    pdf.code(
        "SMALL  -> SMALL, MEDIUM, LARGE\n"
        "MEDIUM -> MEDIUM, LARGE\n"
        "LARGE  -> LARGE"
    )
    pdf.h2("ParkingSpot")
    pdf.p(
        "Knows its coordinates, size, and current vehicle. park/unpark/can_fit live here "
        "so the lot cannot put a truck in a small stall even if a bug skipped the heap "
        "filter -- defense in depth."
    )
    pdf.h2("ParkingFloor")
    pdf.p(
        "Constructs spots in entrance order: all SMALL, then MEDIUM, then LARGE, numbered "
        "from 1. It does not assign vehicles. That keeps 'where stalls live' separate from "
        "'which stall is chosen' (SRP)."
    )
    pdf.h2("Ticket")
    pdf.p(
        "Created at park, closed at unpark. Fee is computed only at close() so an open "
        "ticket does not hold a stale price if rates change mid-stay (rates are read at "
        "close). Minimum one hour, then ceiling."
    )
    pdf.h2("ParkingLot")
    pdf.p(
        "The facade. It owns floors, the HashMaps, and the heaps. External code should not "
        "reach into spots to park. This is also the transaction boundary: park updates "
        "spot + ticket map + plate map together."
    )

    pdf.h1("5. Data structures (the core of the interview)")
    pdf.p(
        "This is where you outrun a linear scan. Five indexes, each justified:"
    )
    pdf.kv_table(
        [
            ("_spots: dict[spot_id, Spot]", "O(1) resolve a heap entry or a ticket's stall."),
            ("_active_tickets: dict[id, Ticket]", "O(1) unpark by ticket id."),
            ("_parked: dict[plate, Ticket]", "O(1) duplicate-plate check and plate lookup."),
            ("_available: dict[size, min-heap]", "Nearest free stall of a given size, O(log n) push/pop."),
            ("_available_ids: dict[size, set]", "Membership so stale heap entries can be discarded."),
        ]
    )
    pdf.h2("Why a heap, not a scan")
    pdf.p(
        "Naive park: for floor in floors: for spot in floor.spots: if spot.can_fit(v): take it. "
        "That is O(S) per park, S = total stalls. Fine for 50 spots, poor for a stadium. "
        "A min-heap keyed by (floor, number, id) gives the nearest free stall of one size "
        "in O(1) peek and O(log n) pop."
    )
    pdf.h2("Nearest across compatible sizes")
    pdf.p(
        "A bike can sit in three heaps. I peek the live head of each compatible heap and "
        "take the min (floor, number). Then I mark that id removed. I do not pop the other "
        "heaps. Example: floor 1 smalls are gone, floor 1 medium #4 vs floor 2 small #1 -- "
        "(1,4) wins, so the bike takes a medium on floor 1. That matches 'nearest', not "
        "'prefer exact size even if farther'."
    )
    pdf.h2("Lazy heap deletion")
    pdf.p(
        "heapq cannot delete an arbitrary element in O(log n) without extras. On assign I "
        "remove the id from _available_ids and leave the tuple in the heap. The next peek "
        "pops stale heads until it finds an id that is still live. Amortized cheap if we "
        "do not churn the same stall pathologically."
    )
    pdf.watch(
        "If they say 'I need decrease-key / delete', offer a position map + tombstones, "
        "or a balanced tree (sorted set) of (floor, number, id). Python's heapq is the "
        "honest stdlib choice."
    )
    pdf.h2("Why HashMap for plates")
    pdf.p(
        "Duplicate parking is a real bug (two tickets, one car). A linear search of active "
        "tickets is O(parked). A dict is O(1) and is the sentence they want: "
        "'HashMap for quick lookup of parked vehicles.'"
    )

    pdf.h1("6. Key flows")
    pdf.h2("park_vehicle")
    pdf.bullets(
        [
            "If plate in _parked: raise VehicleAlreadyParkedError (include existing spot).",
            "spot = _pop_nearest(vehicle). If None: raise NoSpotAvailableError.",
            "spot.park(vehicle) -- second check on size and occupancy.",
            "Create Ticket. Index by ticket_id and plate. Return ticket.",
        ],
        numbered=True,
    )
    pdf.h2("unpark_vehicle")
    pdf.bullets(
        [
            "Pop ticket from _active_tickets or raise UnknownTicketError.",
            "spot.unpark(). ticket.close() -- writes exit time and fee.",
            "Remove plate from _parked. _push_available(spot).",
            "Return the closed ticket so the booth can print the fee.",
        ],
        numbered=True,
    )
    pdf.h2("get_available_spots")
    pdf.p(
        "Walks floors and counts free stalls by size. O(S). This is a report, not the "
        "hot path. If a dashboard needed O(1), I would keep running counters updated on "
        "push/pop -- mention that as a follow-up optimization."
    )

    pdf.h1("7. OOP principles")
    pdf.h2("Encapsulation")
    pdf.p(
        "Occupancy is ParkingSpot._vehicle. Availability indexes are private on the lot. "
        "The console uses park_vehicle / unpark_vehicle / get_available_spots only."
    )
    pdf.h2("Abstraction")
    pdf.p(
        "Callers do not know there is a heap. They know 'nearest compatible spot'. That "
        "lets us swap the heap for a tree later without touching parking_main."
    )
    pdf.h2("Inheritance (where it earns its keep)")
    pdf.p(
        "Vehicle is the only hierarchy. Subclasses are substitutable: any Vehicle can be "
        "parked. We do not inherit ParkingSpot into CompactSpot / HandicapSpot unless "
        "behavior diverges -- a size enum plus a flags set is enough for most variants."
    )
    pdf.h2("Polymorphism")
    pdf.p(
        "create_vehicle returns Vehicle. park_vehicle accepts Vehicle. Fee uses "
        "vehicle.vehicle_type to index HOURLY_RATE. New types plug in without editing "
        "the loop in park_vehicle."
    )
    pdf.h2("Composition")
    pdf.p(
        "Lot has floors; floors have spots; tickets have a vehicle and a spot. The garage "
        "is a tree of has-a, not a God class with 40 fields."
    )

    pdf.h1("8. SOLID principles")
    pdf.h2("S -- Single Responsibility")
    pdf.kv_table(
        [
            ("Vehicle", "Who is parking. Not fees, not heaps."),
            ("ParkingSpot", "Can this stall hold this vehicle right now?"),
            ("ParkingFloor", "Layout of one level."),
            ("Ticket", "Stay duration and money."),
            ("ParkingLot", "Assignment policy + indexes + use-case API."),
            ("parking_main.py", "Human I/O."),
        ]
    )
    pdf.p(
        "Honest gap: HOURLY_RATE lives in types.py. A PricingPolicy class would be a "
        "cleaner SRP split if pricing rules grow (grace period, night rate, EV). I would "
        "say that unprompted -- it scores more than pretending the design is finished."
    )
    pdf.h2("O -- Open/Closed")
    pdf.p(
        "Closed: park_vehicle does not change when we add Van or a third floor. Open: new "
        "Vehicle subclass, new factory entry, optional new SpotSize. PricingPolicy would "
        "make rate changes closed as well."
    )
    pdf.p(
        "If they add EV-only stalls: either a new SpotSize/flag and a filter on the heap "
        "key, or a separate heap. Do not put if vehicle.is_ev inside five classes -- "
        "extend the compatibility table."
    )
    pdf.h2("L -- Liskov Substitution")
    pdf.p(
        "Any Vehicle passed to park_vehicle must be parkable using required_size. A "
        "subclass that leaves required_size unset, or that throws in __str__, would "
        "violate LSP. Bike/Car/Truck only specialize two class attributes -- safe."
    )
    pdf.h2("I -- Interface Segregation")
    pdf.p(
        "The lot's public API is three verbs plus lookups. Floors do not implement park. "
        "Spots do not implement fee. Clients are not forced to depend on heap internals."
    )
    pdf.h2("D -- Dependency Inversion")
    pdf.p(
        "ParkingLot depends on the Vehicle abstraction, not on Car. The factory returns "
        "Vehicle. Ticket.close depends on a rate table keyed by VehicleType -- if we "
        "inject a PricingPolicy, Ticket depends on an interface, not a dict in types.py. "
        "That is the DIP improvement I would make next."
    )

    pdf.h1("9. Design patterns")
    pdf.kv_table(
        [
            ("Factory Method / Simple Factory", "create_vehicle(type, plate) hides Bike/Car/Truck constructors from the UI."),
            ("Facade", "ParkingLot is the one object the application talks to."),
            ("Composite-style tree", "Lot -> Floor -> Spot. Operations roll up (available counts)."),
            ("Value / entity split", "Ticket and Spot are entities (identity). Vehicle is an entity keyed by plate. SpotSize is a value."),
            ("Strategy (ready)", "Nearest-spot policy and pricing are the two strategies I would extract if a second policy appears (e.g. 'prefer exact size')."),
            ("Template-ish flow", "park is a fixed sequence: validate, allocate, occupy, ticket. Hooks would be allocate() and price()."),
        ]
    )
    pdf.p(
        "Not used, and I would say so: Singleton (one global lot kills tests and multi-garage "
        "apps), Observer (gate displays can poll get_available_spots), Object Pool (spots "
        "are not disposable workers)."
    )

    pdf.h1("10. Complexity cheat sheet")
    pdf.kv_table(
        [
            ("park_vehicle", "O(1) plate check + O(k log n) nearest, k = compatible sizes (max 3) ~ O(log n)."),
            ("unpark_vehicle", "O(1) map ops + O(log n) heap push."),
            ("find_vehicle / find_ticket", "O(1)."),
            ("get_available_spots", "O(S) scan, S = total spots. Optional: O(F) with counters."),
            ("Memory", "O(S) spots + O(S) heap entries + O(P) tickets, P = parked cars."),
        ]
    )

    pdf.h1("11. Concurrency and scale (they will ask)")
    pdf.p(
        "This implementation is single-threaded. Two booths calling park_vehicle at once "
        "could pop the same heap head. Fixes, in order of complexity:"
    )
    pdf.bullets(
        [
            "A single asyncio/thread lock around park and unpark. Simple, correct, may serialize booths.",
            "Per-size locks so a bike heap and a truck heap can proceed in parallel.",
            "Allocate in a DB transaction with SELECT FOR UPDATE on the chosen spot row -- the production version.",
            "Distributed lot: Redis heap or a parking service with a lease (spot reserved for 5s while payment confirms).",
        ]
    )
    pdf.p(
        "Horizontal scale: the in-memory maps become Redis hashes; the heap becomes a "
        "sorted set (ZADD score = floor*K + number). The class diagram stays the same. "
        "That is the line that makes the design sound scalable rather than 'I used a dict'."
    )

    pdf.h1("12. Extensions interviewers love")
    pdf.bullets(
        [
            "Handicap / EV / compact: add flags on ParkingSpot; filter in _pop_nearest.",
            "Reservations: hold a spot with an expiry; a sweeper returns expired holds to the heap.",
            "Dynamic pricing: PricingPolicy(time, occupancy_ratio, vehicle_type).",
            "Multi-entrance nearest: distance is not (floor, number) but Euclidean to the entry used. Heap key becomes (distance, id).",
            "Payment: Ticket stays; a PaymentService charges on close. Do not put Stripe in ParkingLot.",
            "Display boards: Observer or a scheduled get_available_spots.",
        ]
    )

    pdf.h1("13. Follow-up questions (with answers)")
    pdf.h3("Bike vs a closer large spot vs a farther small?")
    pdf.p(
        "I defined nearest as physical (floor, number) among compatible stalls. A farther "
        "exact-size stall loses. If the product wants 'never waste a large on a bike if a "
        "small exists anywhere', that is a different strategy: walk compatible sizes in "
        "size order, not by distance. I would ask which rule they want."
    )
    pdf.h3("What if the lot has 10,000 spots?")
    pdf.p(
        "Heaps stay O(log n). Maps stay O(1). get_available_spots should switch to counters. "
        "Memory is the real limit in-process -- at that size I persist spots and keep only "
        "free-id heaps hot."
    )
    pdf.h3("How do you prevent double parking the same plate?")
    pdf.p(
        "_parked[plate] checked before allocation. Plate is normalized. I would also unique "
        "that column in a database."
    )
    pdf.h3("Where does money live?")
    pdf.p(
        "Ticket.close(). ParkingLot is not a cashier. If receipts need tax, a PricingPolicy "
        "or BillingService is the next class -- not more if-else in the lot."
    )
    pdf.h3("Why not one list of free spots sorted by distance?")
    pdf.p(
        "Then every park must filter by size while scanning from the front -- worst case "
        "O(S). Per-size heaps jump to a compatible candidate in O(log n)."
    )
    pdf.h3("How would you unit-test nearest?")
    pdf.p(
        "Build a tiny lot: 2 small, 2 medium, 1 large on two floors. Park a bike, assert "
        "F01-S001. Park a car, assert first medium. Fill smalls, park another bike, assert "
        "it took the nearest medium, not a small on floor 2 if floor 1 medium is closer. "
        "That test is in the design we shipped."
    )

    pdf.h1("14. Whiteboard script (15 minutes)")
    pdf.bullets(
        [
            "Clarify: floors, sizes, nearest definition, leftover large-for-bike rule, fees.",
            "Draw Vehicle hierarchy and Spot / Floor / Lot / Ticket.",
            "Write the three public methods and the exception cases.",
            "Draw the five indexes. Circle HashMap and Heap -- say complexities.",
            "Walk park then unpark with a bike, car, truck example.",
            "SOLID in 60 seconds, then name Factory + Facade.",
            "Extensions: EV, lock, Redis sorted set, PricingPolicy.",
        ],
        numbered=True,
    )

    pdf.h1("15. Common mistakes to avoid")
    pdf.bullets(
        [
            "One ParkingLot class that also computes fees, prints tickets, and talks to payment.",
            "isinstance(vehicle, Car) trees -- breaks OCP.",
            "Scanning all spots every park and calling it 'scalable' because 'computers are fast'.",
            "Forgetting to return a freed spot to the free index (leak of capacity).",
            "Allowing the same plate twice.",
            "Putting console input() inside ParkingLot.",
            "Calling the lot a Singleton so 'there is only one garage in the world'.",
        ]
    )

    pdf.h1("16. Side-by-side with the cards problem")
    pdf.p(
        "Same interview muscle: domain types, one facade, private data structures, "
        "fail-fast errors, UI kept out. Difference: cards is an algorithm problem "
        "(prove Fisher-Yates). Parking is an indexing problem (prove you would not "
        "scan). If you get both in one loop, say that sentence -- it shows you can "
        "classify the problem, not just dump patterns."
    )

    pdf.output(path)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    cards = root / "Deck_of_Cards_Interview_Design.pdf"
    parking = root / "Parking_Lot_Interview_Design.pdf"
    write_cards(cards)
    write_parking(parking)
    print(f"Wrote {cards}")
    print(f"Wrote {parking}")


if __name__ == "__main__":
    main()
