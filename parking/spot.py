"""A single parking stall on a floor."""

from __future__ import annotations

from parking.types import SpotSize
from parking.vehicle import Vehicle


class SpotOccupiedError(ValueError):
    """Spot is already holding a vehicle."""


class ParkingSpot:
    """One stall. Occupancy is stored here; the lot tracks availability indexes."""

    def __init__(self, floor: int, number: int, size: SpotSize) -> None:
        if floor < 1 or number < 1:
            raise ValueError("floor and spot number must be >= 1")
        self.floor = floor
        self.number = number
        self.size = size
        self._vehicle: Vehicle | None = None

    @property
    def spot_id(self) -> str:
        return f"F{self.floor:02d}-S{self.number:03d}"

    @property
    def vehicle(self) -> Vehicle | None:
        return self._vehicle

    @property
    def is_available(self) -> bool:
        return self._vehicle is None

    def can_fit(self, vehicle: Vehicle) -> bool:
        return self.is_available and self.size.can_fit(vehicle.required_size)

    def park(self, vehicle: Vehicle) -> None:
        if not self.is_available:
            raise SpotOccupiedError(f"{self.spot_id} is occupied")
        if not self.size.can_fit(vehicle.required_size):
            raise ValueError(
                f"{vehicle} needs {vehicle.required_size.name}; "
                f"{self.spot_id} is {self.size.name}"
            )
        self._vehicle = vehicle

    def unpark(self) -> Vehicle:
        if self._vehicle is None:
            raise ValueError(f"{self.spot_id} is already empty")
        vehicle = self._vehicle
        self._vehicle = None
        return vehicle

    def __repr__(self) -> str:
        state = self._vehicle.license_plate if self._vehicle else "empty"
        return f"ParkingSpot({self.spot_id}, {self.size.name}, {state})"

    def __str__(self) -> str:
        return f"{self.spot_id} [{self.size.name}]"
