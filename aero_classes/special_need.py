class SpecialNeed:
    def __init__(self, type: str, assistance: str):
        self.__type = type
        self.__assistance = assistance
        
    def get_type(self) -> str:
        return self.__type

    def set_type(self, type: str):
        self.__type = type
        
    def get_assistance(self) -> str:
        return self.__assistance
    
    def set_assistance(self, assistance: str):
        self.__assistance = assistance
