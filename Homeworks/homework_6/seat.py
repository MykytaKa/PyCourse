from passenger import Passenger
from dataclasses import dataclass


@dataclass
class Seat:
    seat_class: str
    number_of_row: int
    position_in_row: str
    seat_id: str
    passenger: Passenger
