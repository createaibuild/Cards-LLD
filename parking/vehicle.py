"""Vehicle hierarchy: one type per subclass, shared identity by plate."""

from __future__ import annotations

from parking.types import SpotSize, VehicleType


class Vehicle:
    """Abstract parked vehicle. Identity is the license plate."""

    vehicle_type: VehicleType
    required_size: SpotSize

    def __init__(self, license_plate: str) -> None:
        plate = license_plate.strip().upper()
        if not plate:
            raise ValueError("license plate cannot be empty")
        self.license_plate = plate

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.license_plate == other.license_plate

    def __hash__(self) -> int:
        return hash(self.license_plate)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.license_plate!r})"

    def __str__(self) -> str:
        return f"{self.vehicle_type.value} {self.license_plate}"


class Bike(Vehicle):
    vehicle_type = VehicleType.BIKE
    required_size = SpotSize.SMALL


class Car(Vehicle):
    vehicle_type = VehicleType.CAR
    required_size = SpotSize.MEDIUM


class Truck(Vehicle):
    vehicle_type = VehicleType.TRUCK
    required_size = SpotSize.LARGE


_FACTORIES = {
    VehicleType.BIKE: Bike,
    VehicleType.CAR: Car,
    VehicleType.TRUCK: Truck,
}


def create_vehicle(vehicle_type: VehicleType, license_plate: str) -> Vehicle:
    """Factory so callers do not switch on subclasses themselves."""
    return _FACTORIES[vehicle_type](license_plate)
