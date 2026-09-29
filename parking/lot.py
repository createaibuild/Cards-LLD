"""ParkingLot: floors + HashMap indexes + nearest-spot assignment."""

from __future__ import annotations

import heapq
from typing import Dict, Iterable, List, Mapping, Tuple

from parking.floor import ParkingFloor
from parking.spot import ParkingSpot
from parking.ticket import Ticket
from parking.types import COMPATIBLE_SIZES, SpotSize
from parking.vehicle import Vehicle


class NoSpotAvailableError(ValueError):
    """No compatible stall is free."""


class VehicleAlreadyParkedError(ValueError):
    """This plate already has an open ticket."""


class UnknownTicketError(KeyError):
    """Ticket id is not in the active map."""


class ParkingLot:
    """Multi-floor garage.

    Data structures
    ---------------
    ``_spots`` : HashMap spot_id → ParkingSpot
        O(1) spot lookup when closing a ticket.
    ``_active_tickets`` : HashMap ticket_id → Ticket
        O(1) unpark by ticket.
    ``_parked`` : HashMap license_plate → Ticket
        O(1) "is this vehicle already inside?"
    ``_available`` : HashMap SpotSize → min-heap of (floor, number, spot_id)
        Nearest free stall of a given size in O(log n).
    ``_available_ids`` : HashMap SpotSize → set of spot_id
        Validates heap entries after unpark/re-insert (lazy discard).
    """

    def __init__(
        self,
        name: str,
        floor_layouts: Iterable[Mapping[SpotSize, int]],
    ) -> None:
        self.name = name
        self.floors: List[ParkingFloor] = []
        self._spots: Dict[str, ParkingSpot] = {}
        self._active_tickets: Dict[str, Ticket] = {}
        self._parked: Dict[str, Ticket] = {}
        self._available: Dict[SpotSize, List[Tuple[int, int, str]]] = {
            size: [] for size in SpotSize
        }
        self._available_ids: Dict[SpotSize, set[str]] = {size: set() for size in SpotSize}

        for index, counts in enumerate(floor_layouts, start=1):
            floor = ParkingFloor(index, dict(counts))
            self.floors.append(floor)
            for spot in floor.spots:
                self._spots[spot.spot_id] = spot
                self._push_available(spot)

    # --- public API (parkVehicle / unparkVehicle / getAvailableSpots) ---

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        """Assign the nearest compatible spot and issue a ticket."""
        if vehicle.license_plate in self._parked:
            existing = self._parked[vehicle.license_plate]
            raise VehicleAlreadyParkedError(
                f"{vehicle.license_plate} is already in {existing.spot.spot_id} "
                f"(ticket {existing.ticket_id})"
            )

        spot = self._pop_nearest(vehicle)
        if spot is None:
            raise NoSpotAvailableError(f"no spot available for {vehicle}")

        spot.park(vehicle)
        ticket = Ticket(vehicle, spot)
        self._active_tickets[ticket.ticket_id] = ticket
        self._parked[vehicle.license_plate] = ticket
        return ticket

    def unpark_vehicle(self, ticket_id: str) -> Ticket:
        """Free the stall, compute the fee, and close the ticket."""
        try:
            ticket = self._active_tickets.pop(ticket_id.upper())
        except KeyError as exc:
            raise UnknownTicketError(f"unknown ticket {ticket_id}") from exc

        ticket.spot.unpark()
        ticket.close()
        self._parked.pop(ticket.vehicle.license_plate, None)
        self._push_available(ticket.spot)
        return ticket

    def get_available_spots(self) -> Dict[int, Dict[str, int]]:
        """Free stalls per floor, keyed by size name. O(floors × spots)."""
        report: Dict[int, Dict[str, int]] = {}
        for floor in self.floors:
            counts = floor.available_counts()
            report[floor.floor_number] = {size.name: n for size, n in counts.items()}
        return report

    # --- lookups ---

    def find_ticket(self, ticket_id: str) -> Ticket | None:
        return self._active_tickets.get(ticket_id.upper())

    def find_vehicle(self, license_plate: str) -> Ticket | None:
        return self._parked.get(license_plate.strip().upper())

    @property
    def parked_count(self) -> int:
        return len(self._parked)

    @property
    def active_tickets(self) -> List[Ticket]:
        return list(self._active_tickets.values())

    @property
    def total_spots(self) -> int:
        return len(self._spots)

    # --- nearest-spot index ---

    def _push_available(self, spot: ParkingSpot) -> None:
        heapq.heappush(
            self._available[spot.size],
            (spot.floor, spot.number, spot.spot_id),
        )
        self._available_ids[spot.size].add(spot.spot_id)

    def _peek_nearest(self, size: SpotSize) -> ParkingSpot | None:
        heap = self._available[size]
        live = self._available_ids[size]
        while heap and heap[0][2] not in live:
            heapq.heappop(heap)
        if not heap:
            return None
        return self._spots[heap[0][2]]

    def _pop_nearest(self, vehicle: Vehicle) -> ParkingSpot | None:
        """Among every compatible size, take the lowest (floor, number)."""
        best: ParkingSpot | None = None
        for size in COMPATIBLE_SIZES[vehicle.required_size]:
            candidate = self._peek_nearest(size)
            if candidate is None:
                continue
            if best is None or (candidate.floor, candidate.number) < (
                best.floor,
                best.number,
            ):
                best = candidate
        if best is None:
            return None
        self._available_ids[best.size].discard(best.spot_id)
        # Leave the heap entry; the next peek discards it as stale.
        return best

    def __repr__(self) -> str:
        return (
            f"ParkingLot({self.name!r}, floors={len(self.floors)}, "
            f"parked={self.parked_count}/{self.total_spots})"
        )
