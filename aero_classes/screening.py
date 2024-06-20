from datetime import datetime

class Screening:
    def __init__(self, screeningID: str, status: str, timestamp: datetime = None):
        self.__screeningID = screeningID
        self.__status = status
        self.__timestamp = timestamp if timestamp else datetime.now()
        
    def get_screeningID(self) -> str:
        return self.__screeningID
    
    def set_screeningID(self, screeningID: str):
        self.__screeningID = screeningID
    
    def get_status(self) -> str:
        return self.__status
    
    def set_status(self, status: str):
        self.__status = status
        
    def get_timestamp(self):
        return self.__timestamp
    
    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp
