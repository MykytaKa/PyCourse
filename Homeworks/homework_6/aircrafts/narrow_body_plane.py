from random import randint
from Homeworks.homework_6.aircrafts.aircraft import Aircraft


class NarrowBodyPlane(Aircraft):
    width_range = [10, 20]
    num_of_seats_range = [140, 210]
    speed_range = [800, 1000]
    landing_distance_range = [2000, 3500]

    def __init__(self, speed, aircraft_id, width=None, num_of_seats=2, landing_distance=0):
        super().__init__(speed=speed,
                         aircraft_id=aircraft_id,
                         width=width,
                         num_of_seats=num_of_seats,
                         landing_distance=landing_distance)
        self.is_passenger = True

    @staticmethod
    def apply_aircraft_feature():
        print('I am narrow body plane!!')

    def fill_cabin(self, passengers, cargo_amount):
        passengers_capability = round(len(passengers) * 0.15)
        if passengers_capability != 0:
            for index, passenger in enumerate(passengers, start=1):
                if index > passengers_capability:
                    break
                is_passenger_sit_down = False
                for row in self.seats:
                    if is_passenger_sit_down:
                        break
                    for seat in row:
                        if seat.passenger is None and not is_passenger_sit_down:
                            is_passenger_sit_down = True
                            seat.passenger = passenger
        else:
            self.amount_of_cargo += randint(0, cargo_amount)

    def release_cabin(self, airport):
        for row in self.seats:
            for seat in row:
                if seat.passenger is not None:
                    airport.passengers.append(seat.passenger)
                    seat.passenger = None
        if self.amount_of_cargo > 0:
            airport.amount_of_cargo += self.amount_of_cargo
            self.amount_of_cargo = 0

    def conduct_landing(self, airport):
        self.release_cabin(airport)

    def conduct_taking_off(self):
        pass
