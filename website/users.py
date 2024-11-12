from flask import Blueprint, render_template,session
from .schemas import UserSchema
import re,requests
bp = Blueprint("users", __name__, template_folder="templates", static_folder="static")

# Users routes
def get_user(user_id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"https://api.example.com/users/{user_id}"

    # Make the API request with the appropriate headers
    response = requests.get(api_endpoint, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Retrieve the user data from the response
        user_data = response.json()

        # Exclude the "id" field from the user data if needed
        user_data.pop("id", None)

        # Return the user data as JSON
        return jsonify(user_data)
    else:
        # Handle the case when the user is not found or the request fails
        return jsonify({"message": "User not found"}), 404

@bp.route("/users", methods=["GET"])
def users_list():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = "https://api.example.com/users"

    # Make the API request with the appropriate headers
    response = requests.get(api_endpoint, headers=headers)
    data = response.json()

    # Extract the 'results' property
    results = data.get("results", [])

    # Create a new dictionary
    user_dict = {}
    for result in results:
        user_id = result.get("id")
        user_name = result.get("name")
        user_dict[user_id] = user_name

    # Render the userMngt.html template with the user dictionary
    return render_template("userMngt.html", users=user_dict)

@bp.route("/add_user",methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Regular expression pattern for email validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        # Check if the email matches the pattern
        if not re.match(email_pattern, email):
            flash("Not a valid email", category="error")
            return False
        # Check if firstName contains only letters
        if not firstName.isalpha():
            flash("First name should only contain letters", category="error")
            return False

        # Check if the passwords match
        if password1 != password2:
            flash("Passwords do not match", category="error")
            return False

        # Check password requirements
        if (
            len(password1) < 8
            or not any(char.isupper() for char in password1)
            or not any(char.islower() for char in password1)
            or not any(char.isdigit() for char in password1)
        ):
            flash(
                "Password should have a length of 8 characters and contain at least one uppercase letter, one lowercase letter, and one digit",
                category="error",
            )
            return False

        # All checks passed, make API call to add a user
        url = "https://api.example.com/addUsers"
        payload = {
            "email": email,
            "firstName": firstName,
            "password": password1
        }

        # Retrieve JWT token from the session
        jwt_token = session.get('jwt_token')

        # Include JWT token in the headers of the request
        headers = {"Authorization": f"Bearer {jwt_token}"}

        # Send the request to the API endpoint with the JWT token in the headers
        response = requests.post(url, json=payload, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # User was added successfully
            success_message = response.json().get("message")
            return jsonify({"success": True, "message": success_message})
        else:
            # Error occurred while adding the user
            error_message = response.json().get("error")
            return jsonify({"success": False, "error": error_message})
    else:
        # Render the userAdd.html template
        return render_template("userAdd.html")

@bp.route("/change-password", methods=["POST"])
def change_password():
    if request.method == "POST":
        # Get the password data from the request
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Check if the new passwords match
        if new_password != confirm_password:
            return "Error: New passwords do not match"

        # Retrieve JWT token from the session
        jwt_token = session.get('jwt_token')

        # Include JWT token in the headers of the request
        headers = {"Authorization": f"Bearer {jwt_token}"}

        # Make a request to the API with the JWT token in the headers
        url = "https://api.example.com/change-pass"
        payload = {"current_password": current_password, "new_password": new_password}
        response = requests.post(url, headers=headers, json=payload)

        # Check the response status code
        if response.status_code == 200:
            # Request was successful, return the response content
            return response.json()
        else:
            # Request failed, return an error message
            return "Error: Failed to change password"
    else:
        # Render the chngPswd.html template
        return render_template("chngPswd.html")

