from .screening import Screening

class Baggage:
    def __init__(self, baggageID: str, weight: float, length: float, width: float, height: float, screening: Screening):
        self.__baggageID = baggageID
        self.__weight = weight
        self.__length = length
        self.__width = width
        self.__height = height
        self.__screening = screening

    def get_baggageID(self) -> str:
        return self.__baggageID

    def set_baggageID(self, baggageID: str):
        self.__baggageID = baggageID

    def get_weight(self) -> float:
        return self.__weight

    def set_weight(self, weight: float):
        self.__weight = weight

    def get_length(self) -> float:
        return self.__length

    def set_length(self, length: float):
        self.__length = length

    def get_width(self) -> float:
        return self.__width

    def set_width(self, width: float):
        self.__width = width

    def get_height(self) -> float:
        return self.__height

    def set_height(self, height: float):
        self.__height = height

    # method to get the dimension of the baggage in the form like 55.0 x 40.0 x 20.0
    def get_dimensions(self) -> tuple:
        return f"{self.__length} x {self.__width} x {self.__height}"

    def get_screening(self) -> Screening:
        return self.__screening

    def set_screening(self, screening: Screening):
        self.__screening = screening