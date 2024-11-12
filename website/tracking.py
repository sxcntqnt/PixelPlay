from flask import Blueprint, render_template

bp = Blueprint(
    "tracking", __name__, template_folder="templates", static_folder="static"
)

# Tracking routes
@bp.route("/tracking/vehicles", methods=["POST"])
def track_vehicle():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Retrieve the necessary data from the request
    vehicle_id = request.form.get("vehicle_id")
    tracking_info = request.form.get("tracking_info")

    # Validate the data and perform any necessary checks

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/tracking/vehicles"

    # Construct the payload for the API request
    payload = {
        "vehicle_id": vehicle_id,
        "tracking_info": tracking_info
    }

    # Send the API request with the JWT token in the headers
    response = requests.post(api_endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        # Request succeeded, retrieve the response data
        response_data = response.json()
        # Render the liveloc.html template with the tracking information
        return render_template("liveloc.html", tracking_info=response_data["tracking_info"])
    else:
        # Request failed
        return jsonify({"message": "Failed to track vehicle"}), 500

@bp.route("/tracking/<id>/history", methods=["GET"])
def get_location_history(id):
    # Perform any necessary validation on the ID parameter
    if not id:
        return jsonify({"message": "Invalid vehicle ID"}), 400

    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/tracking/{id}/history"

    # Send the API request with the JWT token in the headers
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Request succeeded, retrieve the response data
        response_data = response.json()
        # Handle the location history data if needed
        return jsonify({"message": f"Get Location History for Vehicle ID: {id}", "data": response_data}), 200
    else:
        # Request failed
        return jsonify({"message": "Failed to get location history"}), 500
