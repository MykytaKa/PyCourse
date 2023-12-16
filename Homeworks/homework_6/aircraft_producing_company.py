from random import randint
from Homeworks.homework_6.aircrafts.jet import Jet
from Homeworks.homework_6.aircrafts.cargo import Cargo
from Homeworks.homework_6.aircrafts.fighter import Fighter
from Homeworks.homework_6.aircrafts.helicopter import Helicopter
from Homeworks.homework_6.aircrafts.water_plane import WaterPlane
from Homeworks.homework_6.aircrafts.wide_body_plane import WideBodyPlane
from Homeworks.homework_6.aircrafts.maritime_patrol import MaritimePatrol
from Homeworks.homework_6.aircrafts.piston_aircraft import PistonAircraft
from Homeworks.homework_6.aircrafts.combat_transport import CombatTransport
from Homeworks.homework_6.aircrafts.narrow_body_plane import NarrowBodyPlane
from Homeworks.homework_6.aircrafts.turboprop_aircraft import TurbopropAircraft

# constants = {'Jet': {'class': Jet, 'sped_low': 303, 'speed_h'}}

class AircraftProducingCompany:
    @staticmethod
    def produce_aircraft(aircraft_type, aircraft_id):
        # data = constants[aircraft_type]
        #
        # data['class']()
        match aircraft_type:
            case 'Jet':
                return Jet(speed=randint(Jet.speed_range[0], Jet.speed_range[1]),
                           aircraft_id=aircraft_id,
                           width=randint(Jet.width_range[0], Jet.width_range[1]),
                           num_of_seats=randint(Jet.num_of_seats_range[0], Jet.num_of_seats_range[1]),
                           landing_distance=randint(Jet.landing_distance_range[0], Jet.landing_distance_range[1]))
            case 'Turboprop Aircraft':
                return TurbopropAircraft(speed=randint(TurbopropAircraft.speed_range[0],
                                                       TurbopropAircraft.speed_range[1]),
                                         aircraft_id=aircraft_id,
                                         width=randint(TurbopropAircraft.width_range[0],
                                                       TurbopropAircraft.width_range[1]),
                                         num_of_seats=randint(TurbopropAircraft.num_of_seats_range[0],
                                                              TurbopropAircraft.num_of_seats_range[1]),
                                         landing_distance=randint(TurbopropAircraft.landing_distance_range[0],
                                                                  TurbopropAircraft.landing_distance_range[1]))
            case 'Piston Aircraft':
                return PistonAircraft(speed=randint(PistonAircraft.speed_range[0],
                                                    PistonAircraft.speed_range[1]),
                                      aircraft_id=aircraft_id,
                                      width=randint(PistonAircraft.width_range[0],
                                                    PistonAircraft.width_range[1]),
                                      num_of_seats=randint(PistonAircraft.num_of_seats_range[0],
                                                           PistonAircraft.num_of_seats_range[1]),
                                      landing_distance=randint(PistonAircraft.landing_distance_range[0],
                                                               PistonAircraft.landing_distance_range[1]))
            case 'Wide-body plane':
                return WideBodyPlane(speed=randint(WideBodyPlane.speed_range[0],
                                                   WideBodyPlane.speed_range[1]),
                                     aircraft_id=aircraft_id,
                                     width=randint(WideBodyPlane.width_range[0],
                                                   WideBodyPlane.width_range[1]),
                                     num_of_seats=randint(WideBodyPlane.num_of_seats_range[0],
                                                          WideBodyPlane.num_of_seats_range[1]),
                                     landing_distance=randint(WideBodyPlane.landing_distance_range[0],
                                                              WideBodyPlane.landing_distance_range[1]))
            case 'Narrow-body plane':
                return NarrowBodyPlane(speed=randint(NarrowBodyPlane.speed_range[0],
                                                     NarrowBodyPlane.speed_range[1]),
                                       aircraft_id=aircraft_id,
                                       width=randint(NarrowBodyPlane.width_range[0],
                                                     NarrowBodyPlane.width_range[1]),
                                       num_of_seats=randint(NarrowBodyPlane.num_of_seats_range[0],
                                                            NarrowBodyPlane.num_of_seats_range[1]),
                                       landing_distance=randint(NarrowBodyPlane.landing_distance_range[0],
                                                                NarrowBodyPlane.landing_distance_range[1]))
            case 'Cargo':
                return Cargo(speed=randint(Cargo.speed_range[0],
                                           Cargo.speed_range[1]),
                             aircraft_id=aircraft_id,
                             width=randint(Cargo.width_range[0],
                                           Cargo.width_range[1]),
                             landing_distance=randint(Cargo.landing_distance_range[0],
                                                      Cargo.landing_distance_range[1]))
            case 'Maritime Patrol':
                return MaritimePatrol(speed=randint(MaritimePatrol.speed_range[0],
                                                    MaritimePatrol.speed_range[1]),
                                      aircraft_id=aircraft_id)
            case 'Water-plane':
                return WaterPlane(speed=randint(WaterPlane.speed_range[0],
                                                WaterPlane.speed_range[1]),
                                  aircraft_id=aircraft_id)
            case 'Helicopter':
                return Helicopter(speed=randint(Helicopter.speed_range[0],
                                                Helicopter.speed_range[1]),
                                  aircraft_id=aircraft_id)
            case 'Fighter':
                return Fighter(speed=randint(Fighter.speed_range[0],
                                             Fighter.speed_range[1]),
                               aircraft_id=aircraft_id,
                               width=randint(Fighter.width_range[0],
                                             Fighter.width_range[1]))
            case 'Combat transport':
                return CombatTransport(speed=randint(CombatTransport.speed_range[0],
                                                     CombatTransport.speed_range[1]),
                                       aircraft_id=aircraft_id,
                                       width=randint(CombatTransport.width_range[0],
                                                     CombatTransport.width_range[1]))
