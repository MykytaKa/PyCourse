from Homeworks.homework_6.airports.airport import Airport


class SeaPlaneBase(Airport):
    def __init__(self, port_info):
        super().__init__(port_info)

    def check_if_aircraft_can_land(self, aircraft):
        if not hasattr(aircraft, 'is_marine'):
            return False
        return super().check_if_aircraft_can_land(aircraft)
