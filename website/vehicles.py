from flask import Blueprint, render_template, flash, session
import jsonify
bp = Blueprint(
    "vehicles", __name__, template_folder="templates", static_folder="static"
)


@bp.route("/vehicles", methods=["POST"])
def vehicle_add():
    if request.method == "POST":
        # Retrieve the data from the request
        data = request.json
        # Generate a random hexadecimal ID for v_id
        v_id = secrets.token_hex(8)

        # Perform the relevant checks
        if (
            "v_registration_no" in data
            and "v_name" in data
            and "v_model" in data
            and "v_chassis_no" in data
            and "v_engine_no" in data
            and "v_manufactured_by" in data
            and "v_type" in data
            and "v_color" in data
            and "v_mileageperlitre" in data
            and "v_is_active" in data
            and "v_group" in data
            and "v_reg_exp_date" in data
            and "v_api_url" in data
            and "v_api_username" in data
            and "v_api_password" in data
            and "v_created_by" in data
            and "v_created_date" in data
            and "v_modified_date" in data
        ):
            # Retrieve JWT token from the session
            jwt_token = session.get("jwt_token")

            if jwt_token:
                # Include JWT token in the headers of the request
                headers = {
                    "Authorization": f"Bearer {jwt_token}",
                    "Content-Type": "application/json",
                }

                # Call the API endpoint
                api_url = "http://api.example.com:3420/createvehicle"
                response = requests.post(api_url, json=data, headers=headers)

                # Check the response from the API
                if response.status_code == 200:
                    flash("Vehicle created successfully", "success")
                    return redirect(url_for("your_route"))  # Replace "your_route" with the appropriate route name
                else:
                    flash("Failed to create vehicle. API request failed.", "error")
                    return redirect(url_for("your_route"))  # Replace "your_route" with the appropriate route name
            else:
                flash("JWT token not found in session", "error")
                return redirect(url_for("your_route"))  # Replace "your_route" with the appropriate route name
        else:
            flash("Missing required data fields", "error")
            return redirect(url_for("your_route"))  # Replace "your_route" with the appropriate route name

    return render_template("vehicleAdd.html")

@bp.route("/vehicles", methods=["GET"])
def get_all_vehicles():
    # Retrieve JWT token from the session
    jwt_token = session.get("jwt_token")

    if jwt_token:
        # Include JWT token in the headers of the request
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        # Make the API request to get all vehicles
        api_url = "http://api.example.com:3420/vehicles"
        response = requests.get(api_url, headers=headers)

        # Check the response and handle accordingly
        if response.status_code == 200:
            vehicles = response.json()
            return render_template("viewVehicle.html", vehicles=vehicles)
        else:
            flash("Failed to retrieve vehicles", "error")  # Flash an error message

    else:
        flash("JWT token not found in session", "error")  # Flash an error message

    return render_template("viewVehicle.html")  # Render the template

@bp.route("/vehicles/<id>", methods=["GET"])
def view_vehicle(id):
    # Retrieve JWT token from the session
    jwt_token = session.get("jwt_token")

    if jwt_token:
        # Include JWT token in the headers of the request
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        # Make the API request to get the vehicle by ID
        api_url = f"http://api.example.com:3420/vehicles/{id}"
        response = requests.get(api_url, headers=headers)

        # Check the response and handle accordingly
        if response.status_code == 200:
            vehicle = response.json()
            return render_template("viewVehicle.html", vehicle=vehicle)
        else:
            flash(f"Failed to retrieve vehicle with ID: {id}", "error")
            return redirect(url_for("your_route"))  # Replace "your_route" with the appropriate route name

    else:
        flash("JWT token not found in session", "error")
        return redirect(url_for("your_route"))  # Replace "your_route" with the appropriate route name


@bp.route("/vehicles/<id>", methods=["PUT"])
def update_vehicle_group(id):
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

    # Get the updated data from the request body
    updated_data = request.get_json()

    # Make a request to the API endpoint to update the vehicle group
    api_url = f"http://api.example.com:3420/vehicle-groups/{id}"
    response = requests.put(api_url, headers=headers, json=updated_data)

    # Check the response status code
    if response.status_code == 200:
        # Request successful, return the response data
        data = response.json()
        return jsonify(data)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to update vehicle group"}), response.status_code

    # Render the "vehicleMngt.html" template
    return render_template("vehicleMngt.html")

@bp.route("/vehicles/<id>", methods=["DELETE"])
def delete_vehicle(id):
    # Retrieve JWT token from the session
    jwt_token = session.get("jwt_token")

    if jwt_token:
        # Include JWT token in the headers of the request
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        # Make the API request to delete the vehicle
        api_url = f"http://api.example.com:3420/vehicles/{id}"
        response = requests.delete(api_url, headers=headers)

        # Check the response and handle accordingly
        if response.status_code == 200:
            return jsonify({"message": f"Deleted vehicle with ID: {id}"})
        else:
            return jsonify({"error": f"Failed to delete vehicle with ID: {id}"})

    else:
        return jsonify({"error": "JWT token not found in session"})

    # Render the "vehicleMngt.html" template
    return render_template("vehicleMngt.html")

@bp.route("/vehicle-groups", methods=["POST"])
def create_vehicle_group():
    data = request.get_json()
    gr_id = secrets.token_hex(8)

    # Check if the required data structure is present in the request
    if "gr_name" in data and "gr_desc" in data and "gr_created_date" in data:
        # Retrieve the JWT token from the session
        jwt_token = session.get("jwt_token")

        # Check if the JWT token is present
        if jwt_token:
            # Set the API endpoint URL
            api_url = "http://api.example.com:3420/createvehiclegroup"

            # Set the headers with the JWT token
            headers = {"Authorization": f"Bearer {jwt_token}"}

            # Make the API request to create the vehicle group
            response = requests.post(api_url, headers=headers, json=data)

            # Check the response status code
            if response.status_code == 200:
                return jsonify({"message": "Create Vehicle Group"})
            else:
                return jsonify({"error": "Failed to create vehicle group"})

        else:
            return jsonify({"error": "JWT token not found"})

    else:
        return jsonify({"error": "Invalid request data structure"})

    # Render the "vehicleGrp.html" template
    return render_template("vehicleGrp.html")

@bp.route("/vehicle-groups", methods=["POST"])
def add_vehicles_to_group():
    data = request.get_json()

    # Check if the required data structure is present in the request
    if "group_id" in data and "vehicle_ids" in data:
        # Retrieve the JWT token from the session
        jwt_token = session.get("jwt_token")

        # Check if the JWT token is present
        if jwt_token:
            # Set the API endpoint URL
            api_url = "http://api.example.com:3420/addvehiclestogroup"

            # Set the headers with the JWT token
            headers = {"Authorization": f"Bearer {jwt_token}"}

            # Make the API request to add vehicles to the group
            response = requests.post(api_url, headers=headers, json=data)

            # Check the response status code
            if response.status_code == 200:
                return jsonify({"message": "Add Vehicles to Group"})
            else:
                return jsonify({"error": "Failed to add vehicles to group"})

        else:
            return jsonify({"error": "JWT token not found"})

    else:
        return jsonify({"error": "Invalid request data structure"})

    # Render the "vehicleGrp.html" template
    return render_template("vehicleGrp.html")

@bp.route("/vehicle-groups", methods=["GET"])
def get_vehicle_groups():
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

    # Make a request to the API endpoint to get all vehicle groups
    api_url = "http://api.example.com:3420/vehicle-groups"
    response = requests.get(api_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Request successful, return the response data
        data = response.json()
        return jsonify(data)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to get vehicle groups"}), response.status_code

    # Render the "vehicleGrp.html" template
    return render_template("vehicleGrp.html")

@bp.route("/vehicle-groups/<id>", methods=["GET"])
def get_vehicle_group(group_id):
    # Retrieve the JWT token from the session
    jwt_token = session.get("jwt_token")

    # Check if the JWT token is present
    if jwt_token:
        # Set the API endpoint URL
        api_url = f"http://api.example.com:3420/vehiclegroups/{group_id}"

        # Set the headers with the JWT token
        headers = {"Authorization": f"Bearer {jwt_token}"}

        # Make the API request to get the vehicle group
        response = requests.get(api_url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            vehicle_group = response.json()
            return render_template("vehicleGrp.html", vehicle_group=vehicle_group)
        else:
            return jsonify({"error": "Failed to get vehicle group"})

    else:
        return jsonify({"error": "JWT token not found"})

@bp.route("/vehicle-groups/<name>", methods=["GET"])
def get_vehicle_group_by_name(name):
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

    # Make a request to the API endpoint to get the vehicle group by name
    api_url = f"http://api.example.com:3420/vehicle-groups/{name}"
    response = requests.get(api_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        vehicle_group = response.json()
        return render_template("vehicleGrp.html", vehicle_group=vehicle_group)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to get vehicle group"}), response.status_code

@bp.route("/vehicle-groups/<id>", methods=["PUT"])
def updateVehicleGroup(id):
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

    # Get the updated data from the request body
    updated_data = request.get_json()

    # Make a request to the API endpoint to update the vehicle group
    api_url = f"http://api.example.com:3420/vehicle-groups/{id}"
    response = requests.put(api_url, headers=headers, json=updated_data)

    # Check the response status code
    if response.status_code == 200:
        vehicle_group = response.json()
        return render_template("vehicleMngt.html", vehicle_group=vehicle_group)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to update vehicle group"}), response.status_code

@bp.route("/vehicle-groups/<id>", methods=["DELETE"])
def delete_vehicles_from_group(id):
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

    # Make a request to the API endpoint to delete vehicles from the group
    api_url = f"http://api.example.com:3420/vehicle-groups/{id}/vehicles"
    response = requests.delete(api_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        group_data = response.json()
        return render_template("vehicleMngt.html", group_data=group_data)
    else:
        # Request failed, return an error message
        return jsonify({"error": "Failed to delete vehicles from group"}), response.status_code
