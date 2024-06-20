from typing import List
from .passenger import Passenger

class GroupPassenger:
    def __init__(self, groupID: str, representative: Passenger, passengers: List[Passenger]):
        self.__groupID = groupID
        self.__representative = representative
        self.__passengers = passengers
        
    def get_groupID(self) -> str:
        return self.__groupID
    
    def set_groupID(self, groupID: str):
        self.__groupID = groupID
    
    def get_representative(self) -> Passenger:
        return self.__representative
    
    def set_representative(self, representative: Passenger):
        self.__representative = representative
    
    def get_passengers(self) -> List[Passenger]:
        return self.__passengers
    
    def add_member(self, passenger: Passenger):
        self.__passengers.append(passenger)