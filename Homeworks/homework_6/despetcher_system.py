import csv
from itertools import count
from datetime import datetime
from random import sample, choice
from consts import AIRCRAFT_TYPES
from airport_factory import AirportFactory
from aircraft_producing_company import AircraftProducingCompany

counter = count(start=1)


class DispatcherSystem:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.current_time = datetime.now()
        self.airports = self.initial_setup

    @property
    def initial_setup(self):
        with open('airports_.csv', 'r', encoding='utf-8') as csv_file:
            chosen_airports = sample(list(csv.DictReader(csv_file)), 20)
            airport_factory = AirportFactory()
            airports = [airport_factory.create_airport(info) for info in chosen_airports if info is not None]
        aircraft_factory = AircraftProducingCompany()
        aircrafts_amount = 0
        while aircrafts_amount < 20:
            aircraft = aircraft_factory.produce_aircraft(choice(AIRCRAFT_TYPES), next(counter))
            airport = choice(airports)
            if airport.check_if_aircraft_can_land(aircraft):
                airport.hangars.append(aircraft)
                aircrafts_amount += 1
        return airports

    def describe_aircraft(self, aircraft_id):
        for port in self.airports:
            for aircraft in port.hangars:
                if aircraft.id == aircraft_id:
                    print(aircraft.__dict__)
                    break
        print(f'There is no aircraft with an id of {aircraft_id}')

    def describe_passenger(self, passenger_id):
        for port in self.airports:
            if hasattr(port, 'passengers'):
                for passenger in port.passengers:
                    if passenger.passenger_id == passenger_id:
                        print(passenger.__dict__)
            for aircraft in port.hangars:
                for seat in aircraft.seats:
                    if seat.passenger.passenger_id == passenger_id:
                        print(seat.passenger.__dict__)
        print(f'There is no passenger with an id of {passenger_id}')

    def describe_airport(self, airport_id):
        for airport in self.airports:
            if airport.port_id == airport_id:
                print(airport.__dict__)
        print(f'There is no airport with an id of {airport_id}')

    def show_situation(self):
        for index, port in enumerate(self.airports, start=1):
            print(f'Airport {index}({port.airport_type_description}):')
            if hasattr(port, 'passengers'):
                print('\tPassengers in airport:')
                for i, passenger in enumerate(port.passengers, start=1):
                    print(f'\t                     Passenger {i}:{passenger.__dict__}')
            print('\tAircrafts in airport:')
            for i, aircraft in enumerate(port.hangars, start=1):
                print(f'\t                     Aircraft {i}: {aircraft.__dict__}')

    def change_time(self, delta):
        self.current_time = self.current_time + delta


o1 = DispatcherSystem()
for port_air in o1.airports:
    print(port_air.__dict__)
    if len(port_air.hangars) > 0:
        for plane in port_air.hangars:
            print(f'\t{plane.__dict__}')

