from flask import Blueprint, render_template

bp = Blueprint("drivers", __name__, template_folder="templates", static_folder="static")

# Drivers routes
@bp.route("/drivers", methods=["POST"])
def create_driver():
    # Get the JSON data from the request
    data = request.get_json()

    # Validate the request data
    validation_rules = {
        "d_name": {"required": True},
        "d_mobile": {"required": True},
        "d_address": {"required": True},
        "d_age": {"required": True, "type": "integer"},
        "d_licenseno": {"required": True},
        "d_licenceexpdate": {"required": True},
        "d_totalexperience": {"required": True, "type": "integer"},
        "d_dateofjoining": {"required": True},
        "d_reference": {"required": True},
        "d_is_active": {"required": True, "type": "integer"},
        "d_created_by": {"required": True, "type": "integer"}
    }

    validation_messages = {
        "d_name": {"required": "Driver name is required"},
        "d_mobile": {"required": "Mobile number is required"},
        "d_address": {"required": "Driver address is required"},
        "d_age": {"required": "Driver age is required", "type": "Driver age must be an integer"},
        "d_licenseno": {"required": "Driver license number is required"},
        "d_licenceexpdate": {"required": "Driver license expiration date is required"},
        "d_totalexperience": {"required": "Total experience is required", "type": "Total experience must be an integer"},
        "d_dateofjoining": {"required": "Date of joining is required"},
        "d_reference": {"required": "Reference is required"},
        "d_is_active": {"required": "Active status is required", "type": "Active status must be an integer"},
        "d_created_by": {"required": "Created by is required", "type": "Created by must be an integer"}
    }

    validate_data(data, validation_rules, validation_messages)

    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Make the API request
    response = requests.post(api_endpoint, headers=headers, json=data)

    if response.status_code == 201:
        # Successful creation
        return jsonify({"message": "Driver created"})
    elif response.status_code == 400:
        # Validation error
        return jsonify({"message": "Invalid request data"}), 400
    else:
        # Request failed
        return jsonify({"message": "Failed to create driver"}), 500

@bp.route("/drivers", methods=["GET"])
def get_driver():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        drivers = response.json()

        # Handle get driver logic
        return jsonify({"message": "Get drivers", "drivers": drivers})
    else:
        # Request failed
        return jsonify({"message": "Failed to retrieve drivers"}), 500


@bp.route("/drivers/<id>", methods=["GET"])
def get_driver_by_id(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL with the driver ID
    api_endpoint = f"{base_api_url}/drivers/{id}"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        driver = response.json()

        # Handle get driver by ID logic
        return jsonify({"message": f"Get Driver by ID: {id}", "driver": driver})
    else:
        # Request failed
        return jsonify({"message": "Failed to retrieve driver"}), 500

@bp.route("/drivers/<id>", methods=["PUT"])
def update_driver(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL with the driver ID
    api_endpoint = f"{base_api_url}/drivers/{id}"

    # Get the request data from the JSON payload
    data = request.json

    # Make the API request
    response = requests.put(api_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        # Successful request
        updated_driver = response.json()

        # Handle update driver logic
        return jsonify({"message": f"Update Driver: {id}", "driver": updated_driver})
    else:
        # Request failed
        return jsonify({"message": "Failed to update driver"}), 500

@bp.route("/drivers/<id>", methods=["DELETE"])
def delete_driver(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL with the driver ID
    api_endpoint = f"{base_api_url}/drivers/{id}"

    # Make the API request
    response = requests.delete(api_endpoint, headers=headers)

    if response.status_code == 204:
        # Successful request
        return jsonify({"message": f"Delete Driver: {id}"})
    else:
        # Request failed
        return jsonify({"message": "Failed to delete driver"}), 500
