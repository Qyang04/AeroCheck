from datetime import datetime, timedelta

class Flight:
    def __init__(self, flightNumber: str, airline: str, departureDateTime: datetime, gate: str, origin: str, destination: str):
        self.__flightNumber = flightNumber
        self.__airline = airline
        self.__departureDateTime = departureDateTime
        self.__gate = gate
        self.__origin = origin
        self.__destination = destination
        self.__boardingTime = self.__departureDateTime - timedelta(minutes=40)
        
    def get_flight_number(self) -> str:
        return self.__flightNumber
    
    def set_flight_number(self, flightNumber: str):
        self.__flightNumber = flightNumber
        
    def get_airline(self) -> str:
        return self.__airline
    
    def set_airline(self, airline: str):
        self.__airline = airline
        
    def get_departure_datetime(self) -> datetime:
        return self.__departureDateTime
    
    def set_departure_datetime(self, departureDateTime: datetime):
        self.__departureDateTime = departureDateTime
        self.__boardingTime = self.__departureDateTime - timedelta(minutes=40)
        
    def get_gate(self) -> str:
        return self.__gate
    
    def set_gate(self, gate: str):
        self.__gate = gate
        
    def get_origin(self) -> str:
        return self.__origin
    
    def set_origin(self, origin: str):
        self.__origin = origin
        
    def get_destination(self) -> str:
        return self.__destination
    
    def set_destination(self, destination: str):
        self.__destination = destination
        
    # get the DEPART DATE ONLY of the flight
    def get_flight_date(self) -> datetime.date:
        return self.__departureDateTime.date()
    
    # get the BOARDING TIME
    # set the boarding time is 40 min earlier than departure time
    def get_boarding_time(self) -> datetime.time:
        return self.__boardingTime.time() # return time only
    
    # get DEPARTURE TIME ONLY
    def get_departure_time(self) -> datetime.time:
        return self.__departureDateTime.time()