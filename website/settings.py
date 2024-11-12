from flask import Blueprint, render_template

bp = Blueprint(
    "settings", __name__, template_folder="templates", static_folder="static"
)
# Settings routes
@bp.route("/upload", methods=["POST"])
def upload_file():
    # Get the uploaded file from the request
    form_file = request.files.get("file")
    if form_file is None:
        return jsonify({"message": "No file provided"}), 400

    # Get the file details
    filename = form_file.filename
    file_extension = filename.rsplit(".", 1)[-1].lower()

    # Validate the file type
    allowed_types = ["jpg", "png"]
    if file_extension not in allowed_types:
        return jsonify({"message": "Invalid file type"}), 400

    # Validate the file size
    max_size = 1024 * 1024 * 5  # 5MB
    if len(form_file.read()) > max_size:
        return jsonify({"message": "File size exceeds the limit"}), 400
    form_file.seek(0)  # Reset the file pointer after reading

    # Validate the file dimensions
    max_width = 1024
    max_height = 1024
    # Replace the following code with your actual implementation
    # Check the file dimensions and return an error if they exceed the limits

    # Handle the upload file logic using routes.UploadFile
    # Replace the following code with your actual implementation
    # Retrieve JWT token from the session
    jwt_token = session.get("jwt_token")

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/upload"

    # Make the API request
    files = {"file": (filename, form_file)}
    response = requests.post(api_endpoint, headers=headers, files=files)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": "File uploaded"}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/settings", methods=["GET"])
def get_website_setting():
    # Perform validation on the request data
    request_data = request.get_json()
    if request_data is None:
        return jsonify({"message": "Invalid request data"}), 400

    # Check if the required fields exist in the request data
    required_fields = ["s_id", "s_companyname", "s_address", "s_inovice_prefix", "s_logo", "s_price_prefix",
                       "s_inovice_termsandcondition", "s_inovice_servicename", "s_googel_api_key"]
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields:
        return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Validate the request data using a schema or custom validation logic
    # Replace the following code with your actual implementation
    # ...

    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/settings"

    # Make the API request
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        # Successful request
        website_setting = response.json().get("website_setting")

        # Return the website setting as JSON response
        return jsonify(website_setting)
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/settings", methods=["POST"])
def save_web_setting():
    # Perform validation on the request data
    request_data = request.get_json()
    if request_data is None:
        return jsonify({"message": "Invalid request data"}), 400

    # Check if the required fields exist in the request data
    required_fields = ["s_id", "s_companyname", "s_address", "s_inovice_prefix", "s_logo", "s_price_prefix",
                       "s_inovice_termsandcondition", "s_inovice_servicename", "s_googel_api_key"]
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields:
        return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Validate the request data using a schema or custom validation logic
    # Replace the following code with your actual implementation
    # ...

    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/settings"

    # Make the API request
    response = requests.post(api_endpoint, headers=headers, json=request_data)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": "Web setting saved"}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500

@bp.route("/settings", methods=["DELETE"])
def delete_logo():
    # Perform validation on the request data
    request_data = request.get_json()
    if request_data is None:
        return jsonify({"message": "Invalid request data"}), 400

    # Check if the required fields exist in the request data
    required_fields = ["s_id", "s_logo"]
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields:
        return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Validate the request data using a schema or custom validation logic
    # Replace the following code with your actual implementation
    # ...

    # Retrieve JWT token from the session
    jwt_token = session.get('jwt_token')

    # Include JWT token in the headers of the request
    headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}

    # Construct the API endpoint URL
    api_endpoint = f"{base_api_url}/settings"

    # Make the API request
    response = requests.delete(api_endpoint, headers=headers, json=request_data)

    if response.status_code == 200:
        # Successful request
        return jsonify({"message": "Logo deleted"}), 200
    else:
        # Request failed
        return jsonify({"message": "Internal Server Error"}), 500
