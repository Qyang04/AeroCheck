from datetime import datetime
from aero_classes.passenger import Passenger
from aero_classes.group_pass import GroupPassenger
from aero_classes.baggage import Baggage
from aero_classes.flight import Flight
from aero_classes.screening import Screening
from aero_classes.special_need import SpecialNeed
from aero_classes.boarding_pass import BoardingPass
from aero_classes.check_in import CheckIn
from aero_classes.individual_pass import IndividualPassenger

# Create sample special needs
wheelchair = SpecialNeed(type="Wheelchair", assistance="Requires wheelchair assistance")
blind = SpecialNeed(type="Blind", assistance="Requires assistance for visually impaired")

# Create sample flights
flight1 = Flight(flightNumber="A123", airline="AirFly", departureDateTime=datetime(2024, 5, 25, 15, 30), gate="A1", origin="CityA", destination="CityB")
flight2 = Flight(flightNumber="B456", airline="UpHigh", departureDateTime=datetime(2024, 5, 26, 10, 45), gate="B2", origin="CityC", destination="CityD")

# Create sample passengers
passenger1 = IndividualPassenger(passengerID="P001", name="John Doe", contact="john@gmail.com", specialNeed=wheelchair)
passenger2 = IndividualPassenger(passengerID="P002", name="Jane Smith", contact="jane@gmail.com")
passenger3 = Passenger(passengerID="P003", name="Alice Brown", contact="alice@gmail.com")
passenger4 = Passenger(passengerID="P004", name="Bob White", contact="bob@gmail.com")
passenger5 = Passenger(passengerID="P005", name="Charlie Green", contact="charlie@gmail.com")

# Create a group passenger
group_passenger = GroupPassenger(groupID="G001", representative=passenger3, passengers=[passenger3, passenger4, passenger5])

# Create sample baggage
baggage1 = Baggage(baggageID="B001", weight=20.5, length=55.0, width=40.0, height=20.0, tagID="T001", trackingStatus="Checked in", screening=None)
baggage2 = Baggage(baggageID="B002", weight=18.0, length=50.0, width=38.0, height=22.0, tagID="T002", trackingStatus="Checked in", screening=None)

# Create sample screenings
screening1 = Screening(screeningID="S001", status="Cleared", timestamp=datetime.utcnow())
screening2 = Screening(screeningID="S002", status="Cleared", timestamp=datetime.utcnow())

# set seat for each of the passenger
passenger3.set_seat("10A")
passenger4.set_seat("10B")
passenger5.set_seat("10C")

# Create boarding passes
boarding_pass1 = BoardingPass(bookingID="BK001", passenger=passenger1, seat="12A", flight=flight1)
boarding_pass2 = BoardingPass(bookingID="BK002", passenger=passenger2, seat="14B", flight=flight2)
boarding_pass3 = BoardingPass(bookingID="G001", passenger=group_passenger, seat=[passenger3.get_seat(), passenger4.get_seat(), passenger5.get_seat()], flight=flight1)

# Data for use in the Flask app
data = {
    "special_needs": [wheelchair, blind],
    "flights": [flight1, flight2],
    "passengers": [passenger1, passenger2, passenger3, passenger4, passenger5],
    "group_passenger": [group_passenger],
    "baggages": [baggage1, baggage2],
    "screenings": [screening1, screening2],
    "boarding_passes": [boarding_pass1, boarding_pass2, boarding_pass3]
}