from Homeworks.homework_6.aircrafts.aircraft import Aircraft


class Helicopter(Aircraft):
    speed_range = [150, 450]

    def __init__(self, speed, aircraft_id, width=None, num_of_seats=2, landing_distance=0):
        super().__init__(speed=speed,
                         aircraft_id=aircraft_id,
                         width=width,
                         num_of_seats=num_of_seats,
                         landing_distance=landing_distance)

    @staticmethod
    def apply_aircraft_feature():
        print('I am helicopter!!')

    def release_cabin(self, airport):
        if self.amount_of_cargo > 0:
            airport.amount_of_cargo += self.amount_of_cargo
            self.amount_of_cargo = 0
