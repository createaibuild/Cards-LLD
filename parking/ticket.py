"""Entry ticket: vehicle + spot + timestamps + fee."""

from __future__ import annotations

from datetime import datetime, timezone
from math import ceil

from parking.spot import ParkingSpot
from parking.types import HOURLY_RATE
from parking.vehicle import Vehicle


class Ticket:
    """Issued on park, closed on unpark. Fee is computed at exit."""

    _next_id = 1

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot) -> None:
        self.ticket_id = f"T{Ticket._next_id}"
        Ticket._next_id += 1
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now(timezone.utc)
        self.exit_time: datetime | None = None
        self.fee: float | None = None

    @property
    def is_open(self) -> bool:
        return self.exit_time is None

    def close(self, exit_time: datetime | None = None) -> float:
        if not self.is_open:
            raise ValueError(f"ticket {self.ticket_id} is already closed")
        self.exit_time = exit_time or datetime.now(timezone.utc)
        hours = (self.exit_time - self.entry_time).total_seconds() / 3600
        billed_hours = max(1, ceil(hours))
        self.fee = billed_hours * HOURLY_RATE[self.vehicle.vehicle_type]
        return self.fee

    def __repr__(self) -> str:
        return f"Ticket({self.ticket_id}, {self.vehicle!r}, {self.spot.spot_id})"
