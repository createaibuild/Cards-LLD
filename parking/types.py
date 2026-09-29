"""Shared enums and size-compatibility rules."""

from enum import Enum


class VehicleType(Enum):
    BIKE = "bike"
    CAR = "car"
    TRUCK = "truck"


class SpotSize(Enum):
    """Spot capacity, ordered SMALL < MEDIUM < LARGE."""

    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    def can_fit(self, required: "SpotSize") -> bool:
        """A spot can take a vehicle if it is the same size or larger."""
        return self.value >= required.value


# A vehicle may use any spot at least as large as it needs.
COMPATIBLE_SIZES = {
    SpotSize.SMALL: (SpotSize.SMALL, SpotSize.MEDIUM, SpotSize.LARGE),
    SpotSize.MEDIUM: (SpotSize.MEDIUM, SpotSize.LARGE),
    SpotSize.LARGE: (SpotSize.LARGE,),
}

HOURLY_RATE = {
    VehicleType.BIKE: 1.0,
    VehicleType.CAR: 3.0,
    VehicleType.TRUCK: 6.0,
}
