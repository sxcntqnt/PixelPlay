from flask import Blueprint, render_template

bp = Blueprint("reports", __name__, template_folder="templates", static_folder="static")

# Reports routes
@bp.route("/reports/incomeexpense", methods=["POST"])
def generate_inc_exp_report():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Retrieve the request data
    request_data = request.get_json()

    # Perform any necessary validation on the request data

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/reports/incomeexpense"

    # Make the API request
    response = requests.post(api_endpoint, headers=headers, json=request_data)

    if response.status_code == 200:
        # Successful request
        report_data = response.json().get("report_data")

        # Render the incomeExpe.html template with the report data
        return render_template("incomeExpe.html", report_data=report_data)
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/reports/incomeexpense/add", methods=["GET"])
def add_inc_exp_report():
    # Render the incomeExpeAdd.html template for adding an income/expense report
    return render_template("incomeExpeAdd.html")

@bp.route("/reports/booking", methods=["GET"])
def generate_booking_report():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/reports/booking"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        report_data = response.json().get("report_data")

        # Render the reportBooking.html template with the report data
        return render_template("reportBooking.html", report_data=report_data)
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/reports/fuel/<id>", methods=["GET"])
def generate_fuel_report(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/reports/fuel/{id}"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        report_data = response.json().get("report_data")

        # Render the reportFuel.html template with the report data
        return render_template("reportFuel.html", report_data=report_data)
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500
