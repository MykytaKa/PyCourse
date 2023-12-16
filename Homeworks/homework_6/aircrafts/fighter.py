from Homeworks.homework_6.mixin_classes import BomberMixin
from Homeworks.homework_6.aircrafts.aircraft import Aircraft


class Fighter(Aircraft, BomberMixin):
    width_range = [2, 7]
    speed_range = [700, 1200]

    def __init__(self, speed, aircraft_id, width=None, num_of_seats=2, landing_distance=0):
        super().__init__(speed=speed,
                         aircraft_id=aircraft_id,
                         width=width,
                         num_of_seats=num_of_seats,
                         landing_distance=landing_distance)
        self.is_combat = True

    @staticmethod
    def apply_aircraft_feature():
        print('I am military fighter!!')
