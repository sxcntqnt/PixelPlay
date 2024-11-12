from flask import Blueprint, render_template
from wtforms import IntegerField
bp = Blueprint(
    "incomExpe", __name__, template_folder="templates", static_folder="static"
)
# Income and Expense routes
@bp.route("/incomexpense", methods=["POST"])
def add_income_expense():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Validate the request data
    form = IncomeExpenseForm(request.json)

    if form.validate_on_submit():
        # Valid data
        ie_v_id = form.ie_v_id.data
        ie_date = datetime.strptime(form.ie_date.data, "%Y-%m-%d").date()
        ie_type = form.ie_type.data
        ie_description = form.ie_description.data
        ie_amount = form.ie_amount.data
        is_income = form.is_income.data
        is_expense = form.is_expense.data

        # Construct the JSON payload for the API request
        payload = {
            "ie_v_id": ie_v_id,
            "ie_date": ie_date,
            "ie_type": ie_type,
            "ie_description": ie_description,
            "ie_amount": ie_amount,
            "is_income": is_income,
            "is_expense": is_expense
        }

        # Construct the API endpoint URL
        api_endpoint = f"{base_api_url}/incomes-expenses"

        # Make the API request
        response = requests.post(api_endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            # Successful request
            return jsonify({"message": "Add Income/Expense"}), 200
        else:
            # Request failed
            return jsonify({"message": "Failed to add income/expense"}), 500
    else:
        # Invalid data
        errors = form.errors
        return jsonify({"message": "Invalid request data", "errors": errors}), 400

@bp.route("/incomexpense", methods=["GET"])
def get_incomes():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Get the filter parameter from the request query string
    filter_param = request.args.get("filter")  # e.g., "1 month"

    # Calculate the start and end dates based on the filter parameter
    if filter_param == "1 month":
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
    elif filter_param == "3 months":
        start_date = datetime.now() - timedelta(days=90)
        end_date = datetime.now()
    elif filter_param == "1 year":
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
    else:
        # Invalid or no filter provided, return an error response
        return jsonify({"message": "Invalid filter parameter"}), 400

    # Construct the API endpoint URL with the start and end dates as query parameters
    api_endpoint = f"{base_api_url}/incomes?start_date={start_date}&end_date={end_date}"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        incomes = response.json()
        return jsonify({"message": "Get Incomes", "incomes": incomes}), 200
    else:
        # Request failed
        return jsonify({"message": "Failed to fetch incomes"}), 500

@bp.route("/incomexpense/<id>", methods=["GET"])
def get_income(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/incomes/{id}"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        income = response.json()
        return jsonify({"message": f"Get Income for ID: {id}", "income": income}), 200
    else:
        # Request failed
        return jsonify({"message": "Failed to fetch income"}), 500

@bp.route("/incomexpense/<id>", methods=["PUT"])
def edit_income(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Retrieve the updated income data from the request JSON
    updated_income_data = request.json

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/incomes/{id}"

    # Make the API request with the updated income data
    response = requests.put(api_endpoint, headers=headers, json=updated_income_data)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": f"Edit Income for ID: {id}"}), 200
    else:
        # Request failed
        return jsonify({"message": "Failed to edit income"}), 500
