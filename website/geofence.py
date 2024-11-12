from flask import Blueprint, render_template

bp = Blueprint(
    "geofence", __name__, template_folder="templates", static_folder="static"
)

# Geofence routes
@bp.route("/geofences", methods=["POST"])
def create_geofence():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/geofences/create"

    # Extract latitude, longitude, and radius from the request JSON
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    radius = request.json.get('radius')
    name = request.json.get('name')

    # Validate that latitude, longitude, and radius are present
    if latitude is None or longitude is None or radius is None:
        return jsonify({"message": "Latitude, longitude, name, and radius are required"}), 400

    # Construct the payload for the API request
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "name":name
        # Add any other required fields for geofence creation
    }

    # Make the API request
    response = requests.post(api_endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": "Create Geofence"}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/Geofence/<id>", methods=["GET"])
def vehicle_enter_geofence(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/geofences/vehicle/{id}/enter"

    # Extract any required data from the request JSON
    # Adjust the code based on the data required for vehicle enter geofence

    # Make the API request
    response = requests.post(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": f"Vehicle Enter Geofence ID: {id}"}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/Geofence/<id>", methods=["GET"])
def get_geo_events(id):
    if request.method == "POST":
        # Retrieve JWT token from the session
        jwt_token = session.get('jwt_token')

        # Include JWT token in the headers of the request
        headers = {"Authorization": f"Bearer {jwt_token}"}

        # Construct the API endpoint URL
        api_endpoint = f"{base_api_url}/geofences/{id}/events"

        # Make the API request
        response = requests.get(api_endpoint, headers=headers)

        if response.status_code == 200:
            # Successful request
            data = response.json()
            return render_template('geofenceEvents.html', data=data)
        else:
            # Request failed
            return jsonify({"message": "Internal Server Error"}), 500
    else:
        return render_template('geofenceEvents.html')

@bp.route("/Geofence/<name>", methods=["GET"])
def get_vehicle_for_geofence(name):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/geofence/{name}/vehicles"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        data = response.json()
        results = data.get("results", [])

        # Process the results and create a new list
        processed_results = []
        for result in results:
            # Process each result as needed
            # ...

            processed_results.append(result)

        # Create the JSON response
        json_response = {"message": f"Get Vehicles for Geofence Name: {name}", "data": processed_results}

        # Return the JSON response
        return jsonify(json_response), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/Geofence/<id>", methods=["DELETE"])
def delete_geofence_by_id(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/geofence/{id}"

    # Make the API request
    response = requests.delete(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": f"Geofence with ID {id} deleted successfully"}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500
