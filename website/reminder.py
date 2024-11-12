from flask import Blueprint, render_template

bp = Blueprint(
    "reminder", __name__, template_folder="templates", static_folder="static"
)
# Reminder routes
@bp.route("/reminders", methods=["POST"])
def create_reminder():
    # Validate the request data
    data = request.json
    if not data:
        return jsonify({"message": "Invalid request data"}), 400

    # Check if the required fields exist in the request data
    required_fields = ["r_id", "r_date", "r_message", "r_isread"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400

    # Perform additional validation based on the rules
    r_id = data["r_id"]
    r_date = data["r_date"]
    r_message = data["r_message"]
    r_isread = data["r_isread"]

    if not isinstance(r_id, int):
        return jsonify({"message": "Invalid data type for r_id"}), 400

    if not isinstance(r_date, str):
        return jsonify({"message": "Invalid data type for r_date"}), 400

    if not isinstance(r_message, str):
        return jsonify({"message": "Invalid data type for r_message"}), 400

    if r_isread not in ["true", "false"]:
        return jsonify({"message": "Invalid value for r_isread"}), 400

    # Process the reminder data and send the request using session and API endpoint
    # Replace the following code with your actual implementation

    # Assuming you have session and endpoint variables set
    session = get_session()
    endpoint = "http://example.com/api/reminders"

    # Send the request
    response = session.post(endpoint, json=data)
    if response.status_code == 200:
        return jsonify({"message": "Create Reminder"}), 200
    else:
        return jsonify({"message": "Failed to create reminder"}), 500

@bp.route("/reminder/<id>", methods=["GET"])
def get_reminder(id):
    # Perform any necessary validation on the ID parameter
    if not id:
        return jsonify({"message": "Invalid reminder ID"}), 400

    # Process the request to get the reminder data using session and API endpoint
    # Replace the following code with your actual implementation

    # Assuming you have session and endpoint variables set
    session = get_session()
    endpoint = f"http://example.com/api/reminders/{id}"

    # Send the request
    response = session.get(endpoint)
    if response.status_code == 200:
        # Extract the reminder data from the response
        reminder_data = response.json()

        return jsonify({"message": f"Get Reminder for ID: {id}", "data": reminder_data}), 200
    else:
        return jsonify({"message": "Failed to get reminder"}), 500

@bp.route("/reminder/<id>", methods=["PUT"])
def edit_reminder(id):
    # Perform any necessary validation on the ID parameter
    if not id:
        return jsonify({"message": "Invalid reminder ID"}), 400

    # Get the request data
    request_data = request.get_json()

    # Validate the request data
    schema = ReminderSchema()
    errors = schema.validate(request_data)
    if errors:
        return jsonify({"message": "Invalid request data", "errors": errors}), 400

    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Set the request headers with the JWT token
    headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}

    # Send the request to the API endpoint
    api_endpoint = f"{base_api_url}/reminders/{id}"
    response = requests.put(api_endpoint, json=request_data, headers=headers)

    # Check the response status code and handle the result accordingly
    if response.status_code == 200:
        # Handle successful edit logic if needed

        return jsonify({"message": f"Edit Reminder for ID: {id}"}), 200
    else:
        return jsonify({"message": "Failed to edit reminder"}), 500

@bp.route("/reminders", methods=["GET"])
def list_reminders():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Retrieve the filter parameter from the query string
    filter_param = request.args.get("filter")

    # Construct the API endpoint URL with the filter parameter
    api_endpoint = f"{base_api_url}/reminders"
    if filter_param:
        api_endpoint += f"?filter={filter_param}"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        reminders = response.json().get("reminders")
        return jsonify({"message": "List Reminders", "reminders": reminders}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500
