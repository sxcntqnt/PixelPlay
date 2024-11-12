from flask import Blueprint, render_template

bp = Blueprint("mail", __name__, template_folder="templates", static_folder="static")

# mailendpoints
@bp.route("/send-booking-email", methods=["POST"])
def smtp_config_save():
    # Validate the request data
    form = SMTPConfigForm(request.json)

    if form.validate_on_submit():
        # Valid data
        smtp_host = form.smtp_host.data
        smtp_auth = form.smtp_auth.data
        smtp_uname = form.smtp_uname.data
        smtp_pwd = form.smtp_pwd.data
        smtp_is_secure = form.smtp_is_secure.data
        smtp_port = form.smtp_port.data
        smtp_email_from = form.smtp_email_from.data
        smtp_reply_to = form.smtp_reply_to.data

        # Perform the necessary operations to save the SMTP configuration
        # Replace the following code with your implementation
        save_smtp_configuration(smtp_host, smtp_auth, smtp_uname, smtp_pwd, smtp_is_secure, smtp_port, smtp_email_from, smtp_reply_to)

        # Retrieve JWT token from the session
        jwt_token = session.get('jwt_token')

        # Include JWT token in the headers of the request
        headers = {"Authorization": f"Bearer {jwt_token}"}

        # Construct the API endpoint URL
        api_endpoint = f"{base_api_url}/smtp/save"

        # Make the API request
        response = requests.post(api_endpoint, headers=headers, json=request.json)

        if response.status_code == 200:
            # Successful request
            return jsonify({"message": "SMTP configuration saved"}), 200
        else:
            # Request failed
            return jsonify({"message": "Internal Server Error"}), 500

    else:
        # Invalid data
        errors = form.errors
        return jsonify({"message": "Invalid request data", "errors": errors}), 400

# Wrap the function with the smtpSettings.html template
@bp.route("/smtp-settings", methods=["GET"])
def smtp_settings():
    return render_template("smtpSettings.html")


@bp.route("/emailtemplate/<id>", methods=["GET"])
def get_email_template(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/emailtemplate/{id}"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        template_data = response.json()

        # Further processing of the template data

        return jsonify({"message": f"Get email template with ID: {id}", "template_data": template_data}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/emailtemplate/<id>", methods=["PUT"])
def update_email_template(id):
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/emailtemplate/{id}"

    # Make the API request
    response = requests.put(api_endpoint, headers=headers, json=request.json)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": f"Update email template with ID: {id}"}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/email-test", methods=["POST"])
def email_test():
    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/email-test"

    # Make the API request
    response = requests.post(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        response_data = response.json()
        inbox_email_address = response_data.get("address")
        return jsonify({"message": "Inbox created for testing.", "address": inbox_email_address}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500
