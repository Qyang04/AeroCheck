from .passenger import Passenger

class CheckIn:
    def __init__(self):
        self.__checked_in_passengers = []
        
    def check_in_passenger(self, passenger: Passenger, flight):
        # validation of passenger
        
        
        self.__checked_in_passengers.append((passenger, flight))