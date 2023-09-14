from Homeworks.homework_6.airports.heliport import Heliport
from Homeworks.homework_6.airports.small_airport import SmallAirport
from Homeworks.homework_6.airports.seaplane_base import SeaPlaneBase
from Homeworks.homework_6.airports.medium_airport import MediumAirport
from Homeworks.homework_6.airports.large_airport import LargeAirport


class AirportFactory:
    @staticmethod
    def create_airport(airport_info):
        match airport_info['type']:
            case 'heliport':
                return Heliport(airport_info)
            case 'small_airport':
                return SmallAirport(airport_info)
            case 'seaplane_base':
                return SeaPlaneBase(airport_info)
            case 'medium_airport':
                return MediumAirport(airport_info)
            case 'large_airport':
                return LargeAirport(airport_info)
