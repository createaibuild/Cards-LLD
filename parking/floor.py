"""One level of the garage: a sequence of spots plus per-size counts."""

from __future__ import annotations

from typing import Dict, List

from parking.spot import ParkingSpot
from parking.types import SpotSize


class ParkingFloor:
    """Owns the spots on one floor. The lot, not the floor, assigns vehicles."""

    def __init__(self, floor_number: int, size_counts: Dict[SpotSize, int]) -> None:
        if floor_number < 1:
            raise ValueError("floor_number must be >= 1")
        self.floor_number = floor_number
        self.spots: List[ParkingSpot] = []
        number = 1
        # Lower numbers sit closer to the entrance on this floor.
        for size in (SpotSize.SMALL, SpotSize.MEDIUM, SpotSize.LARGE):
            for _ in range(size_counts.get(size, 0)):
                self.spots.append(ParkingSpot(floor_number, number, size))
                number += 1

    def available_counts(self) -> Dict[SpotSize, int]:
        counts = {size: 0 for size in SpotSize}
        for spot in self.spots:
            if spot.is_available:
                counts[spot.size] += 1
        return counts

    def __len__(self) -> int:
        return len(self.spots)

    def __repr__(self) -> str:
        return f"ParkingFloor({self.floor_number}, {len(self.spots)} spots)"
