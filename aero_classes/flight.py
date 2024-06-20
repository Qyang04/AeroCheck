from datetime import datetime, timedelta

class Flight:
    def __init__(self, flightNumber: str, airline: str, departureDateTime: datetime, gate: str):
        self.__flightNumber = flightNumber
        self.__airline = airline
        self.__departureDateTime = departureDateTime
        self.__gate = gate
        
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
        
    def get_gate(self) -> str:
        return self.__gate
    
    def set_get(self, gate: str):
        self.__gate = gate
        
    # get the date of the flight depart
    def get_flight_date(self) -> datetime.date:
        return self.__departureDateTime.date()
    
    # get the boarding time
    def get_boarding_time(self) -> datetime.time:
        boarding_time = self.__departureDateTime - timedelta(minutes=30)
        return boarding_time.time()
    
    # get departure time
    def get_departure_time(self) -> datetime.time:
        return self.__departureDateTime.time()