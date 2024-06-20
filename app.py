from flask import Flask, render_template, request, redirect, url_for, flash
from data import data
from aero_classes.group_pass import GroupPassenger

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Fetch individual passenger details by booking ID
def fetch_individual_passenger_details(booking_id):
    for boarding_pass in data['boarding_passes']:
        if boarding_pass.get_bookingID() == booking_id:
            passenger = boarding_pass.get_passenger()
            flight = boarding_pass.get_flight_details()
            return {
                'id': passenger.get_passengerID(),
                'name': passenger.get_name(),
                'booking_id': booking_id,
                'contact': passenger.get_contact(),
                'special_need': passenger.get_specialNeed().get_assistance() if passenger.get_specialNeed() else None,
                'flight': {
                    'flight_number': flight.get_flight_number(),
                    'airline': flight.get_airline(),
                    'departure_datetime': flight.get_departure_datetime(),
                    'gate': flight.get_gate()
                }
            }
    return None

# Fetch group passenger details by booking ID
def fetch_group_passenger_details(booking_id):
    for boarding_pass in data['boarding_passes']:
        if boarding_pass.get_bookingID() == booking_id:
            passenger = boarding_pass.get_passenger()
            if isinstance(passenger, GroupPassenger):
                members = []
                flight = boarding_pass.get_flight_details()
                for member in passenger.get_passengers():
                    members.append({
                        'id': member.get_passengerID(),
                        'name': member.get_name(),
                        'booking_id': booking_id,
                        'contact': member.get_contact(),
                        'special_need': member.get_specialNeed().get_assistance() if member.get_specialNeed() else None,
                        'flight': {
                            'flight_number': flight.get_flight_number(),
                            'airline': flight.get_airline(),
                            'departure_datetime': flight.get_departure_datetime(),
                            'gate': flight.get_gate()
                        }
                    })
                representative = passenger.get_representative()
                return {
                    'group_id': passenger.get_groupID(),
                    'representative': {
                        'id': representative.get_passengerID(),
                        'name': representative.get_name(),
                        'booking_id': booking_id,
                        'contact': representative.get_contact(),
                        'special_need': representative.get_specialNeed().get_assistance() if representative.get_specialNeed() else None,
                        'flight': {
                            'flight_number': flight.get_flight_number(),
                            'airline': flight.get_airline(),
                            'departure_datetime': flight.get_departure_datetime(),
                            'gate': flight.get_gate()
                        }
                    },
                    'members': members
                }
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/type')
def select_type():
    return render_template('type.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'GET':
        passenger_type = request.args.get('passenger_type')
        return render_template('booking.html', passenger_type=passenger_type)

    if request.method == 'POST':
        passenger_type = request.form['passenger_type']
        booking_id = request.form['booking_id']
        
        if passenger_type == 'individual':
            passenger = fetch_individual_passenger_details(booking_id)
            if passenger:
                return render_template('passenger_details.html', passenger=passenger)
            else:
                flash("Booking Number not found for individual passenger.", 'error')
                return redirect(url_for('booking', passenger_type=passenger_type))
        
        elif passenger_type == 'group':
            group = fetch_group_passenger_details(booking_id)
            if group:
                return render_template('group_details.html', group=group)
            else:
                flash("Booking Number not found for group.", 'error')
                return redirect(url_for('booking', passenger_type=passenger_type))
        
        return redirect(url_for('index'))
        
@app.route('/generate_boarding_pass', methods=['POST'])
def generate_boarding_pass():
    # Logic to generate boarding pass and baggage tags
    return "Boarding pass and baggage tags generated"

if __name__ == '__main__':
    app.run(debug=True)