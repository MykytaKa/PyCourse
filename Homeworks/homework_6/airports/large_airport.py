from Homeworks.homework_6.airports.airport import Airport
from Homeworks.homework_6.aircrafts.helicopter import Helicopter


class LargeAirport(Airport):
    def __init__(self, port_info):
        super().__init__(port_info)
        self.lend_lines_len = int(port_info['runaway_length'])
        self.lend_lines_width = int(port_info['runaway_width'])
        self.passengers = []
        self.amount_of_cargo = 0

    def check_if_aircraft_can_land(self, aircraft):
        if isinstance(aircraft, Helicopter):
            return False
        elif aircraft.landing_distance >= self.lend_lines_len or aircraft.width >= self.lend_lines_width * 0.8:
            return False
        return super().check_if_aircraft_can_land(aircraft)

    def take_passengers(self, passengers):
        self.passengers.extend(passengers)

    def move_passengers_to_aircraft(self, aircraft, passengers):
        pass
