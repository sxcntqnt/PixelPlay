from flask import Blueprint, render_template, session
import jsonify
bp = Blueprint(
    "bookings", __name__, url_prefix="/bookings"
)
# booking endpoints
@bp.route("<id>", methods=["GET"])
def get_booking(id):
    # Check if user is authenticated
    if "token" not in session:
        # User is not authenticated, return an error message
        return jsonify({"error": "User is not authenticated"}), 401

    # Get the JWT token from the session
    jwt_token = session["token"]

    # Set the headers for the API request
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # Make a request to the API endpoint to get the booking by ID
    api_url = f"http://api.example.com:3420/bookings/{id}"
    response = requests.get(api_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Request successful, return the response data
        data = response.json()
        return jsonify(data)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to get booking"}), response.status_code

@bp.route("bookVeh",methods=["POST"])
def book_vehicle():
    # Validate the request data
    data = request.get_json()
    errors = validate_booking_data(data)
    if errors:
        return jsonify(errors), 400

    # Check if user is authenticated
    if "token" not in session:
        # User is not authenticated, return an error message
        return jsonify({"error": "User is not authenticated"}), 401

    # Get the JWT token from the session
    jwt_token = session["token"]

    # Set the headers for the API request
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # Make a request to the API endpoint to book the vehicle
    api_url = "http://api.example.com:3420/bookings"
    response = requests.post(api_url, headers=headers, json=data)

    # Check the response status code
    if response.status_code == 200:
        # Request successful, return the response data
        data = response.json()
        return jsonify(data)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to book vehicle"}), response.status_code

def validate_booking_data(data):
    errors = {}

    # Validate required fields
    required_fields = {
        "t_customer_id": "Customer ID is required",
        "t_vechicle": "Choose a vehicle",
        "t_driver": "Choose a driver",
        "t_type": "Choose the type of trip",
        "t_trip_fromlocation": "Select the trip start location",
        "t_trip_tolocation": "Select the trip end location",
        "t_start_date": "Select the trip start date",
        "t_end_date": "Select the trip end date",
        "t_trip_amount": "Trip amount/rent is required",
    }
    for field, error_message in required_fields.items():
        if field not in data or not data[field]:
            errors[field] = error_message

    # Validate trip amount/rent
    if "t_trip_amount" in data:
        trip_amount = data["t_trip_amount"]
        if not trip_amount.isdigit():
            errors["t_trip_amount"] = "Please enter a valid number"
        elif len(trip_amount) < 3:
            errors["t_trip_amount"] = "Trip amount/rent should be at least 3 digits"
        elif len(trip_amount) > 6:
            errors["t_trip_amount"] = "Trip amount/rent should not exceed 6 digits"

    return errors

@bp.route("editBookn", methods=["GET"])
def edit_booking(booking_id):
    # Validate the request data
    data = request.get_json()
    errors = validate_booking_data(data)
    if errors:
        return jsonify(errors), 400

    # Check if user is authenticated
    if "token" not in session:
        # User is not authenticated, return an error message
        return jsonify({"error": "User is not authenticated"}), 401

    # Get the JWT token from the session
    jwt_token = session["token"]

    # Set the headers for the API request
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # Make a request to the API endpoint to edit the booking
    api_url = f"http://api.example.com:3420/bookings/{booking_id}"
    response = requests.put(api_url, headers=headers, json=data)

    # Check the response status code
    if response.status_code == 200:
        # Request successful, return the response data
        data = response.json()
        return jsonify(data)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to edit booking"}), response.status_code

@bp.route("listBookn", methods=["GET"])
def list_bookings():
    # Check if user is authenticated
    if "token" not in session:
        # User is not authenticated, return an error message
        return jsonify({"error": "User is not authenticated"}), 401

    # Get the JWT token from the session
    jwt_token = session["token"]

    # Set the headers for the API request
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # Make a request to the API endpoint to list bookings
    api_url = "http://api.example.com:3420/bookings"
    response = requests.get(api_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Request successful, return the response data
        data = response.json()
        return jsonify(data)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to list bookings"}), response.status_code
