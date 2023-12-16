
class Airport:
    def __init__(self, port_info):
        self.hangars = []
        self.hangars_amount = int(port_info['num_hangars'])
        self.coordinates = [float(port_info['latitude_deg']), float(port_info['longitude_deg'])]
        self.port_id = port_info['id'] + port_info['ident']
        self.name = port_info['name']
        self.airport_type_description = port_info['type']

    def operate_aircraft_landing(self):
        pass

    def operate_aircraft_take_off(self):
        pass

    def put_vehicle(self, aircraft):
        if self.get_number_of_free_hangars() > 0:
            self.hangars.append(aircraft)

    def show_airport_type_description(self):
        print(f'Airport type is {" ".join(self.airport_type_description.split("_"))}')

    def get_number_of_free_hangars(self):
        return self.hangars_amount - len(self.hangars)

    def show_aircrafts(self):
        for index, aircraft in enumerate(self.hangars, start=1):
            print(f'Aircraft number {index}:\n{aircraft.__dict__}')

    def check_if_aircraft_can_land(self, aircraft):
        if self.get_number_of_free_hangars() == 0:
            return False
        return True

    def __eq__(self, other):
        return self.airport_type_description == other.airport_type_description

    def __str__(self):
        return f'Airport name:{self.name};\n\tcoordinates: {self.coordinates}'
