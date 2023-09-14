from Homeworks.homework_6.aircrafts.aircraft import Aircraft
from Homeworks.homework_6.mixin_classes import WaterLanderMixin


class WaterPlane(Aircraft, WaterLanderMixin):
    speed_range = [70, 150]

    def __init__(self, speed, aircraft_id, width=None, num_of_seats=2, landing_distance=0):
        super().__init__(speed=speed,
                         aircraft_id=aircraft_id,
                         width=width,
                         num_of_seats=num_of_seats,
                         landing_distance=landing_distance)
        self.is_marine = True

    @staticmethod
    def apply_aircraft_feature():
        print('I am water plane!!')

    def release_cabin(self, airport):
        if self.amount_of_cargo > 0:
            airport.amount_of_cargo += self.amount_of_cargo
            self.amount_of_cargo = 0

    def conduct_landing(self, airport):
        self.release_cabin(airport)

    def conduct_taking_off(self):
        pass
