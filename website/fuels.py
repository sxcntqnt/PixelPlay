from flask import Blueprint, render_template

bp = Blueprint("fuels", __name__, template_folder="templates", static_folder="static")

# Fuels routes
@bp.route("/fuel", methods=["POST"])
def create_fuel_entry():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Retrieve data from the request
    data = request.json

    # Validate the request data
    fuel_price = data.get('v_fuelprice')
    fuel_quantity = data.get('v_fuel_quantity')
    odometer_reading = data.get('v_odometerreading')
    fuel_fill_date = data.get('v_fuelfilldate')
    fleet_added_by = data.get('v_fleetaddedby')
    vehicle_id = data.get('v_id')
    fleet_comments = data.get('v_fleetcomments')

    # Perform data validation using the provided rules
    if not fuel_price:
        return jsonify({"error": "Fuel price is required"}), 400
    elif not isinstance(fuel_price, (int, float)):
        return jsonify({"error": "Fuel price should be a number"}), 400
    elif len(str(fuel_price)) < 3 or len(str(fuel_price)) > 6:
        return jsonify({"error": "Fuel price should be between 3 and 6 digits"}), 400

    if not fuel_quantity:
        return jsonify({"error": "Fuel quantity is required"}), 400
    elif not isinstance(fuel_quantity, (int, float)):
        return jsonify({"error": "Fuel quantity should be a number"}), 400
    elif len(str(fuel_quantity)) < 1 or len(str(fuel_quantity)) > 6:
        return jsonify({"error": "Fuel quantity should be between 1 and 6 digits"}), 400

    if not odometer_reading:
        return jsonify({"error": "Odometer reading is required"}), 400
    elif not isinstance(odometer_reading, int):
        return jsonify({"error": "Odometer reading should be an integer"}), 400
    elif len(str(odometer_reading)) < 1:
        return jsonify({"error": "Odometer reading should be at least 1 digit"}), 400

    if not fuel_fill_date:
        return jsonify({"error": "Fuel fill date is required"}), 400

    if not fleet_added_by:
        return jsonify({"error": "Fleet added by is required"}), 400

    if not vehicle_id:
        return jsonify({"error": "Vehicle ID is required"}), 400

    if fleet_comments and len(fleet_comments) > 30:
        return jsonify({"error": "Fleet comments should not exceed 30 characters"}), 400

    # Construct the payload for the API request
    payload = {
        "v_fuelprice": fuel_price,
        "v_fuel_quantity": fuel_quantity,
        "v_odometerreading": odometer_reading,
        "v_fuelfilldate": fuel_fill_date,
        "v_fueladdedby": fleet_added_by,
        "v_id": vehicle_id,
        "v_fleetcomments": fleet_comments
    }

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/fuel"

    # Make the API request
    response = requests.post(api_endpoint, json=payload, headers=headers)

    if response.status_code == 201:
        # Successful request
        return jsonify({"message": "Create Fuel Entry"})
    else:
        # Request failed
        return jsonify({"message": "Failed to create fuel entry"}), 500

@bp.route("/fuel", methods=["GET"])
def edit_fuel_entry():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/fuel"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": "Edit Fuel Entry"})

@bp.route("/fuel/<id>", methods=["GET"])
def list_fuel_entries(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/fuel/{id}"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": f"List Fuel Entries for ID: {id}"})
    else:
        # Request failed
        return jsonify({"message": "Failed to list fuel entries"}), 500


@bp.route("/expense", methods=["POST"])
@bp.route("/expense", methods=["POST"])
def add_to_expenses():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/expenses/add"

    # Call the AddToExpense function with the required argument(s)
    err = routes.AddToExpense(request)

    if err is not None:
        # Error occurred in AddToExpense function
        return jsonify({"message": "Internal Server Error"}), 500

    # Make the API request
    response = requests.post(api_endpoint, headers=headers, json=request.json)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": "Fuel entry added to expenses successfully"}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

