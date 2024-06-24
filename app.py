import qrcode
import json
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, flash
from data import data
from aero_classes.group_pass import GroupPassenger
from aero_classes.boarding_pass import BoardingPass
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Fetch individual passenger details by booking ID
def fetch_individual_passenger_details(booking_id):
    for boarding_pass in data['boarding_passes']:
        if boarding_pass.get_bookingID() == booking_id:
            passenger = boarding_pass.get_passenger()
            if isinstance(passenger, GroupPassenger):
                return None
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
                    'arrival_datetime': flight.get_arrival_datetime(),
                    'gate': flight.get_gate(),
                    'origin': flight.get_origin(),
                    'destination': flight.get_destination(),
                    'boarding_time': flight.get_boarding_time().strftime('%H:%M')
                },
                'seat': boarding_pass.get_seat(),
                'baggage_list': passenger.get_baggage_list()
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
                    member_boarding_pass = BoardingPass(booking_id, member, member.get_seat(), flight)
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
                            'arrival_datetime': flight.get_arrival_datetime(),
                            'gate': flight.get_gate(),
                            'origin': flight.get_origin(),
                            'destination': flight.get_destination(),
                            'boarding_time': flight.get_boarding_time().strftime('%H:%M')
                        },
                        'seat': [member_boarding_pass.get_seat()],
                        'baggage_list': member.get_baggage_list()
                    })
                representative = passenger.get_representative()
                representative_boarding_pass = BoardingPass(booking_id, representative, representative.get_seat(), flight)
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
                            'arrival_datetime': flight.get_arrival_datetime(),
                            'gate': flight.get_gate(),
                            'origin': flight.get_origin(),
                            'destination': flight.get_destination(),
                            'boarding_time': flight.get_boarding_time().strftime('%H:%M')
                        },
                        'seat': [representative_boarding_pass.get_seat()],
                        'baggage_list': representative.get_baggage_list()
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
    passenger_type = request.form.get('passenger_type')
    booking_id = request.form.get('booking_id')
    
    if not passenger_type or not booking_id:
        flash("Missing passenger type or booking ID.", 'error')
        return redirect(url_for('index'))
    
    baggage_tags = []
    baggage_not_checked_in = False

    # method to create qr for bp
    def generate_qr_code(data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=9,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
    
    if passenger_type == 'individual':
        passenger = fetch_individual_passenger_details(booking_id)
        if passenger:
            for boarding_pass in data['boarding_passes']:
                if boarding_pass.get_bookingID() == booking_id:
                    for baggage in boarding_pass.get_passenger().get_baggage_list():
                        screening_status = baggage.get_screening().get_status() if baggage.get_screening() else 'Not screened yet'
                        if screening_status != 'Checked In':
                            baggage_not_checked_in = True
                        baggage_tags.append({
                            'baggage_id': baggage.get_baggageID(),
                            'weight': baggage.get_weight(),
                            'dimensions': baggage.get_dimensions(),
                            'screening_status': screening_status,
                            'destination': boarding_pass.get_flight_details().get_destination(),
                            'flight_number': boarding_pass.get_flight_details().get_flight_number(),
                            'booking_id': boarding_pass.get_bookingID(),
                            'passenger_name': passenger['name']
                        })
            if baggage_not_checked_in:
                flash("Some of your baggage has not been checked in.", 'warning')
            flight = passenger['flight']
            total_time = flight['arrival_datetime'] - flight['departure_datetime']
            boarding_pass_details = {
                'passenger': passenger['name'],
                'origin': flight['origin'],
                'destination': flight['destination'],
                'flight': flight['flight_number'],
                'depart_date': flight['departure_datetime'].strftime("%b %d, %Y"),
                'depart_time': flight['departure_datetime'].strftime("%H:%M"),
                'arrival_date': flight['arrival_datetime'].strftime("%b %d, %Y"),
                'arrival_time': flight['arrival_datetime'].strftime("%H:%M"),
                'total_time_seconds': int(total_time.total_seconds()),  # Ensure it's an integer
                'boarding_time': flight['boarding_time'],
                'gate': flight['gate'],
                'seat': passenger['seat']
            }
            qr_data = json.dumps(boarding_pass_details)
            qr_code_image = generate_qr_code(qr_data)
            try:
                qr_code_image_base64 = base64.b64encode(qr_code_image.getvalue()).decode('utf-8')
            except Exception as e:
                flash(f"Error encoding QR code image: {str(e)}", 'error')
                return redirect(url_for('index'))

            # Now pass qr_code_image_base64 to the template
            return render_template('boarding_pass.html', boarding_pass=boarding_pass_details, baggage_tags=baggage_tags, qr_code_image=qr_code_image_base64)
        else:
            flash("Booking Number not found for individual passenger.", 'error')
            return redirect(url_for('booking', passenger_type=passenger_type))
        
    elif passenger_type == 'group':
        group = fetch_group_passenger_details(booking_id)
        if group:
            boarding_passes = []
            baggage_tags_collected = set()  # To avoid duplicates
            qr_code_images = []

            for member in group['members']:
                for boarding_pass in data['boarding_passes']:
                    if boarding_pass.get_bookingID() == booking_id and isinstance(boarding_pass.get_passenger(), GroupPassenger):
                        group_passenger = boarding_pass.get_passenger()
                        for group_member in group_passenger.get_passengers():
                            for baggage in group_member.get_baggage_list():
                                if baggage.get_baggageID() not in baggage_tags_collected:
                                    screening_status = baggage.get_screening().get_status() if baggage.get_screening() else 'Not screened yet'
                                    if screening_status != 'Cleared':
                                        baggage_not_checked_in = True
                                    baggage_tags.append({
                                        'baggage_id': baggage.get_baggageID(),
                                        'weight': baggage.get_weight(),
                                        'dimensions': baggage.get_dimensions(),
                                        'screening_status': screening_status,
                                        'destination': boarding_pass.get_flight_details().get_destination(),
                                        'flight_number': boarding_pass.get_flight_details().get_flight_number(),
                                        'booking_id': boarding_pass.get_bookingID(),
                                        'passenger_name': group_member.get_name()
                                    })
                                    baggage_tags_collected.add(baggage.get_baggageID())
            if baggage_not_checked_in:
                flash("Some of your group's baggage has not been checked in.", 'warning')
            for member in group['members']:
                flight = member['flight']
                total_time = flight['arrival_datetime'] - flight['departure_datetime']
                boarding_passes.append({
                    'passenger': member['name'],
                    'origin': flight['origin'],
                    'destination': flight['destination'],
                    'flight': flight['flight_number'],
                    'depart_date': flight['departure_datetime'].strftime("%b %d, %Y"),
                    'depart_time': flight['departure_datetime'].strftime("%H:%M"),
                    'arrival_date': flight['arrival_datetime'].strftime("%b %d, %Y"),
                    'arrival_time': flight['arrival_datetime'].strftime("%H:%M"),
                    'total_time_seconds': int(total_time.total_seconds()),  # Ensure it's an integer
                    'boarding_time': flight['boarding_time'],
                    'gate': flight['gate'],
                    'seat': member['seat']
                })
            qr_data = json.dumps(boarding_passes)
            qr_code_image = generate_qr_code(qr_data)
            try:
                qr_code_image_base64 = base64.b64encode(qr_code_image.getvalue()).decode('utf-8')
            except Exception as e:
                flash(f"Error encoding QR code image: {str(e)}", 'error')
                return redirect(url_for('index'))
            return render_template('boarding_pass_group.html', boarding_passes=boarding_passes, baggage_tags=baggage_tags, qr_code_image=qr_code_image_base64)
        else:
            flash("Booking Number not found for group.", 'error')
            return redirect(url_for('booking', passenger_type=passenger_type))
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
