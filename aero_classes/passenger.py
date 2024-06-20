from .special_need import SpecialNeed
from .baggage import Baggage
from typing import List

class Passenger:
    def __init__(self, passengerID: str, name: str, contact: str, specialNeed: SpecialNeed = None):
        self.__passengerID = passengerID
        self.__name = name
        self.__contact = contact
        self.__specialNeed = specialNeed
        self.__baggages = []
        
    # getter setter method
    def get_passengerID(self) -> str:
        return self.__passengerID
    
    def set_passengerID(self, passengerID: str):
        self.__passengerID = passengerID
    
    def get_name(self) -> str:
        return self.__name
    
    def set_name(self, name: str):
        self.__name = name
    
    def get_contact(self) -> str:
        return self.__contact
    
    def set_contact(self, contact: str):
        self.__contact = contact
    
    def get_specialNeed(self) -> SpecialNeed:
        return self.__specialNeed
    
    def set_specialNeed(self, specialNeed: SpecialNeed):
        self.__specialNeed = specialNeed
        
    # method to add baggage
    def add_baggage(self, baggage: Baggage):
        self.__baggages.append(baggage)
        
    def get_baggage_list(self) -> List[Baggage]:
        return self.__baggages