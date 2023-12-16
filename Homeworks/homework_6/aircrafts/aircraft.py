import string
from random import choice
from Homeworks.homework_6.seat import Seat
from Homeworks.homework_6.consts import SEAT_STATUS, AMOUNT_OF_SEATS_IN_ROW


class Aircraft:
    def __init__(self, speed, aircraft_id, width, landing_distance, num_of_seats):
        self.speed = speed
        self.width = width
        self.id = aircraft_id
        self.departure_time = 0
        self.amount_of_cargo = 0
        self.status = 'in airport'
        self.actual_coordinates = 0
        self.num_of_seats = num_of_seats
        self.seats = self.set_seats
        self.departure_coordinates = 0
        self.destination_coordinates = 0
        self.landing_distance = landing_distance

    def come_back(self):
        self.destination_coordinates, self.departure_coordinates = self.departure_coordinates, \
            self.destination_coordinates

    @property
    def set_seats(self):
        num_of_rows = self.num_of_seats // AMOUNT_OF_SEATS_IN_ROW
        numb_of_seats_in_the_last_row = self.num_of_seats % AMOUNT_OF_SEATS_IN_ROW
        seats = [[0] * AMOUNT_OF_SEATS_IN_ROW for _ in range(num_of_rows)]
        if numb_of_seats_in_the_last_row > 0:
            seats.extend([[0] * numb_of_seats_in_the_last_row])
            num_of_rows += 1
        for row in range(num_of_rows):
            if row == num_of_rows - 1 and numb_of_seats_in_the_last_row > 0:
                for seat in range(numb_of_seats_in_the_last_row):
                    seats[row][seat] = Seat(seat_class=choice(SEAT_STATUS),
                                            number_of_row=row,
                                            position_in_row=string.ascii_uppercase[seat],
                                            seat_id=f'{row}{string.ascii_uppercase[seat]}',
                                            passenger=None)
            else:
                for seat in range(AMOUNT_OF_SEATS_IN_ROW):
                    seats[row][seat] = Seat(seat_class=choice(SEAT_STATUS),
                                            number_of_row=row,
                                            position_in_row=string.ascii_uppercase[seat],
                                            seat_id=f'{row}{string.ascii_uppercase[seat]}',
                                            passenger=None)
        return seats

    def print_info(self):
        print(self.__dict__)

    def recalculate_position(self):
        pass
