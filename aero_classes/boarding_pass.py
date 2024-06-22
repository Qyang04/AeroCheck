from datetime import datetime
from .passenger import Passenger
from .flight import Flight

class BoardingPass:
    def __init__(self, bookingID: str, passenger: Passenger, seat: str, flight:Flight):
        self.__bookingID = bookingID
        self.__passenger = passenger
        self.__seat = seat
        self.__flight = flight
    
    def get_bookingID(self) -> str:
        return self.__bookingID
    
    def set_bookingID(self, bookingID: str):
        self.__bookingID = bookingID
    
    def get_passenger(self) -> Passenger:
        return self.__passenger
    
    def set_passenger(self, passenger: Passenger):
        self.__passenger = passenger
        
    def get_seat(self) -> str:
        return self.__seat
    
    def set_seat(self, seat: str):
        self.__seat = seat
        
    def get_flight_details(self) -> Flight:
        return self.__flight
    
    def set_flight_details(self, flight: Flight):
        self.__flight = flight
        
    def get_boarding_time(self) -> datetime.time:
        return self.__flight.get_boarding_time()
    
    def get_departure_time(self) -> datetime.time:
        return self.__flight.get_departure_time()
    
    def get_flight_date(self) -> datetime.date:
        return self.__flight.get_flight_date()