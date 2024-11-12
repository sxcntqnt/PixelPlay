from flask import Blueprint, render_template
from flask_wtf import FlaskForm
#from wtforms import StringField
#from wtforms.validators import DataRequired, Email, NumberRange, Length
import requests, jsonify

bp = Blueprint(
    "customer", __name__, template_folder="templates", static_folder="static"
)


# Customers routes
@bp.route("/customer", methods=["POST"])
def create_customer():
    form = CreateCustomerForm(request.form)
    if form.validate():
        # Valid data, proceed with creating the customer
        data = {
            "c_id": generate_random_hex_id(),
            "c_name": form.c_name.data,
            "c_mobile": form.c_mobile.data,
            "c_email": form.c_email.data,
            "c_address": form.c_address.data,
            "c_created_date": get_current_date(),
            # Add other fields if necessary
        }
        
        # Include JWT token in the headers of the request
        headers = {"Authorization": f"Bearer {session.get('jwt_token')}"}
        
        # Make the API request
        response = requests.post(api_endpoint, headers=headers, json=data)
        
        if response.status_code == 200:
            # Customer creation successful
            return jsonify({"message": "Create Customer"})
        else:
            # Customer creation failed
            return jsonify({"message": "Failed to create customer"}), 500
    else:
        # Invalid data, return the validation errors as a response
        errors = form.errors
        return jsonify({"errors": errors}), 400


@bp.route("/customer", methods=["GET"])
def get_customer():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful response
        customers = response.json()["customers"]
        return jsonify({"customers": customers})
    else:
        # Request failed
        return jsonify({"message": "Failed to get customers"}), 500

@bp.route("/customer/<id>", methods=["GET"])
def get_customer_by_id(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Make the API request
    response = requests.get(f"{api_endpoint}/{id}", headers=headers)

    if response.status_code == 200:
        # Successful response
        customer = response.json()
        return jsonify(customer)
    elif response.status_code == 404:
        # Customer not found
        return jsonify({"message": "Customer not found"}), 404
    else:
        # Request failed
        return jsonify({"message": "Failed to get customer"}), 500

@bp.route("/customer/<id>", methods=["PUT"])
def update_customer(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Make the API request
    response = requests.put(f"{api_endpoint}/{id}", headers=headers, json=request.json)

    if response.status_code == 200:
        # Successful response
        updated_customer = response.json()
        return jsonify(updated_customer)
    elif response.status_code == 404:
        # Customer not found
        return jsonify({"message": "Customer not found"}), 404
    else:
        # Request failed
        return jsonify({"message": "Failed to update customer"}), 500

@bp.route("/customer", methods=["DELETE"])
def delete_customer(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Make the API request
    response = requests.delete(f"{api_endpoint}/{id}", headers=headers)

    if response.status_code == 204:
        # Successful deletion
        return jsonify({"message": "Customer deleted"})
    elif response.status_code == 404:
        # Customer not found
        return jsonify({"message": "Customer not found"}), 404
    else:
        # Request failed
        return jsonify({"message": "Failed to delete customer"}), 500
