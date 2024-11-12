from flask import Blueprint, render_template

bp = Blueprint("chgpswd", __name__, template_folder="templates", static_folder="static")


@bp.route("/users/<id>/reset-password", methods=["POST"])
def reset_password(id):
    # Retrieve the new password from the request form data
    new_password = request.form.get("new_password")

    # Retrieve JWT token from the session
    jwt_token = session.get("jwt_token")

    if jwt_token:
        # Include JWT token in the headers of the request
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        # Make the API request to reset the password
        api_url = f"http://api.example.com:3420/users/{id}/reset-password"
        payload = {"new_password": new_password}
        response = requests.post(api_url, headers=headers, json=payload)

        # Check the response and handle accordingly
        if response.status_code == 200:
            # Password reset successful
            flash(f"Password reset for user with ID: {id} was successful!", "success")
        else:
            # Password reset failed
            flash(f"Failed to reset password for user with ID: {id}", "error")
    else:
        # JWT token not found in session
        flash("JWT token not found in session", "error")

    # Render the template
    return render_template("chngPswd.html")
