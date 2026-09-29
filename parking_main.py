#!/usr/bin/env python3
"""Interactive console application for the parking lot."""

from __future__ import annotations

import sys
from typing import Dict

from parking import (
    NoSpotAvailableError,
    ParkingLot,
    UnknownTicketError,
    VehicleAlreadyParkedError,
    VehicleType,
    create_vehicle,
)
from parking.types import SpotSize


BANNER = """
╔══════════════════════════════════════════╗
║           PARKING LOT                    ║
║   Park · Unpark · Nearest open stall     ║
╚══════════════════════════════════════════╝
"""

MENU = """
  1. Park a vehicle
  2. Unpark by ticket
  3. Available spots
  4. Look up a plate
  5. Show active tickets
  6. Demo: park bike, car, truck then unpark
  0. Exit
"""

DEFAULT_LAYOUT = (
    {SpotSize.SMALL: 4, SpotSize.MEDIUM: 4, SpotSize.LARGE: 2},
    {SpotSize.SMALL: 4, SpotSize.MEDIUM: 4, SpotSize.LARGE: 2},
)


def prompt(message: str) -> str:
    try:
        return input(message).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        sys.exit(0)


def print_availability(lot: ParkingLot) -> None:
    print(f"\n  {lot.name}: {lot.parked_count}/{lot.total_spots} occupied")
    for floor, counts in lot.get_available_spots().items():
        parts = [f"{name}={n}" for name, n in counts.items()]
        print(f"  Floor {floor}: " + ", ".join(parts))
    print()


def print_ticket(ticket, *, closing: bool = False) -> None:
    print(f"  Ticket  {ticket.ticket_id}")
    print(f"  Vehicle {ticket.vehicle}")
    print(f"  Spot    {ticket.spot}")
    print(f"  Entry   {ticket.entry_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    if closing:
        print(f"  Exit    {ticket.exit_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"  Fee     ${ticket.fee:.2f}")


def park_from_prompt(lot: ParkingLot) -> None:
    raw = prompt("  Type [b]ike / [c]ar / [t]ruck: ").lower()
    mapping: Dict[str, VehicleType] = {
        "b": VehicleType.BIKE,
        "bike": VehicleType.BIKE,
        "c": VehicleType.CAR,
        "car": VehicleType.CAR,
        "t": VehicleType.TRUCK,
        "truck": VehicleType.TRUCK,
    }
    if raw not in mapping:
        print("  Unknown vehicle type.")
        return
    plate = prompt("  License plate: ")
    try:
        vehicle = create_vehicle(mapping[raw], plate)
        ticket = lot.park_vehicle(vehicle)
    except (ValueError, NoSpotAvailableError, VehicleAlreadyParkedError) as exc:
        print(f"  {exc}")
        return
    print("  Parked at nearest compatible spot.")
    print_ticket(ticket)


def run_demo(lot: ParkingLot) -> None:
    print("\n  Demo — park a bike, a car, and a truck:")
    for kind, plate in (
        (VehicleType.BIKE, "BK-101"),
        (VehicleType.CAR, "CR-202"),
        (VehicleType.TRUCK, "TK-303"),
    ):
        vehicle = create_vehicle(kind, plate)
        try:
            ticket = lot.park_vehicle(vehicle)
        except (NoSpotAvailableError, VehicleAlreadyParkedError) as exc:
            print(f"  {exc}")
            continue
        print(f"  {vehicle} → {ticket.spot}  ticket {ticket.ticket_id}")
    print_availability(lot)
    parked = lot.find_vehicle("CR-202")
    if parked:
        closed = lot.unpark_vehicle(parked.ticket_id)
        print(f"  Unparked {closed.vehicle} from {closed.spot}. Fee ${closed.fee:.2f}")
    print_availability(lot)


def main() -> None:
    print(BANNER)
    lot = ParkingLot("Downtown Garage", DEFAULT_LAYOUT)
    print_availability(lot)

    while True:
        print(MENU)
        print(f"  Occupied: {lot.parked_count}/{lot.total_spots}")
        choice = prompt("  Choose: ")

        if choice == "0":
            print("Goodbye.")
            return

        if choice == "1":
            park_from_prompt(lot)

        elif choice == "2":
            ticket_id = prompt("  Ticket id: ")
            try:
                ticket = lot.unpark_vehicle(ticket_id)
            except UnknownTicketError as exc:
                print(f"  {exc}")
                continue
            print("  Unparked.")
            print_ticket(ticket, closing=True)

        elif choice == "3":
            print_availability(lot)

        elif choice == "4":
            plate = prompt("  License plate: ")
            ticket = lot.find_vehicle(plate)
            if ticket is None:
                print("  Not parked here.")
            else:
                print_ticket(ticket)

        elif choice == "5":
            if not lot.parked_count:
                print("  No vehicles parked.")
                continue
            print()
            for ticket in lot.active_tickets:
                print(f"  {ticket.ticket_id}  {ticket.vehicle}  {ticket.spot}")
            print()

        elif choice == "6":
            run_demo(lot)

        else:
            print("  Unknown option.")


if __name__ == "__main__":
    main()
