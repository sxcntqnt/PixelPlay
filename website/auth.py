import requests, re, jwt, uuid, datetime, base64
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from .models import User

from . import db

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/")
def landing():
    return render_template("landing.html", user=current_user)


@bp.route("/index")
@login_required
def index():
    return render_template("index.html", user=current_user)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        number = request.form.get("number")
        email = request.form.get(
            "email"
        )  # Input field for phone number, email, or username
        password = request.form["password"]
        role = request.form["role"]
        apikey = "your_api_key_here"

        if number.startswith("+254"):
            # Phone number with +254 prefix
            number = request.form.get("number")
            user = User.query.filter_by(number=number).first()
        else:
            # Email or username
            user = User.query.filter(
                (User.email == email) & (User.role == role)
            ).first()

        if user and check_password_hash(user.password, password):
            # Make API call to authenticate user
            api_url = "http://192.168.100.150:3420/api/GenJwt"
            headers = {"Content-Type": "application/json"}
            data = {
                "number": number,
                "email": email,
                "password": password,
                "role": role,
                "apikey": apikey,
            }

            # Send request and retrieve JWT token
            response = requests.post(api_url, headers=headers, json=data)
            results = None
            if response.status_code == 200:
                try:
                    # Retrieve JWT token from the response
                    jwt_token = response.json()["token"]

                    # Include JWT token in the headers of the next request
                    headers["Authorization"] = f"Bearer {jwt_token}"
                    session["jwt_token"] = jwt_token

                    # Make the next request with the JWT token in the headers
                    next_api_url = "http://192.168.100.150:3420/api"
                    next_response = requests.get(next_api_url, headers=headers)

                    # Process the response of the next request
                    if next_response.status_code == 200:
                        # Convert response to dictionary
                        response_data = next_response.text
                        # Convert results to base64 and compare with the given string
                        encoded_results = base64.b64encode(
                            str(response_data).encode("utf-8")
                        ).decode("utf-8")
                        expected_string = "V2VsY29tZSB0byBzeGNudGNucXVudG5z"
                        print(encoded_results, expected_string)

                        if encoded_results == expected_string:
                            print(encoded_results, expected_string)
                            # User is authenticated, process the role
                            if user.role == "admin":
                                flash(
                                    "Logged in Successfully as admin",
                                    category="success",
                                )
                                login_user(user, remember=True)
                                return redirect(url_for("dashboard"))
                            elif user.role == "customer":
                                flash(
                                    "Logged in Successfully as customer",
                                    category="success",
                                )
                                login_user(user, remember=True)
                                return redirect(
                                    url_for("auth.index", user=current_user)
                                )
                            else:
                                flash(
                                    "Unknown role, please contact support",
                                    category="error",
                                )
                                return redirect(url_for("login"))
                        else:
                            flash("Authentication failed", category="error")
                            return redirect(url_for("login"))

                except KeyError:
                    # Handle Key error if 'jwt_token' is not present in the response
                    flash("Invalid response format", category="error")
                    return redirect(url_for("error_page"))
                else:
                    error_message = response.json().get("error", "Unknown error")
                    flash(error_message, category="error")
                    return render_template("login.html", error_message=error_message)
            else:
                flash(
                    "Incorrect identifier or password, please try again",
                    category="error",
                )
                return redirect(url_for("auth.login"))
    else:
        return render_template("login.html", user=current_user)


def refresh_jwt(data, current_token):
    # Define the secret key
    secret_key = "d779bb9cb37697c541987d1c9c46157afcc9712d1288043a8c67da89f186cafe"

    # Decode the existing JWT token to retrieve the expiration time
    decoded_token = jwt.decode(current_token, secret_key, algorithms=["HS256"])
    expiration_time = datetime.datetime.fromtimestamp(decoded_token["exp"])

    # Check if the token is about 30 minutes from expiration
    refresh_threshold = datetime.timedelta(minutes=30)
    if expiration_time - datetime.datetime.utcnow() <= refresh_threshold:
        # Set the new expiration time
        new_exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)

        # Update the payload with the new expiration time
        data["exp"] = new_exp_time.timestamp()

        # Generate the new JWT token
        new_token = jwt.encode(data, secret_key, algorithm="HS256")

        return new_token

    # If the token doesn't need to be refreshed, return the existing token
    return current_token


@bp.route("/register", methods=["POST", "GET"])
def register():
    email = (
        "youremail@yourprovider.com"  # Provide a default value for the email variable
    )
    firstName = "mejja"
    lastName = "genge"
    number = "+254770000000"
    password = "Has to be a sentence with a number"
    role = "Admin/Customer"

    if request.method == "POST":
        number = request.form.get("number")
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        role = request.form.get("role")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Regular expression pattern for email validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        # Check if the email matches the pattern
        if not re.match(email_pattern, email):
            flash("Not a valid email", category="error")
            # Add a return statement here to exit the function
            return redirect(url_for("auth.register"))

        # Check if firstName and lastName contain only letters
        if not firstName.isalpha() or not lastName.isalpha():
            flash(
                "First name and last name should only contain letters", category="error"
            )
            # Add a return statement here to exit the function
            return redirect(url_for("auth.register"))

        # Check if the number starts with "+254"
        if not number.startswith("+254"):
            flash("Number should start with '+254'", category="error")
            # Add a return statement here to exit the function
            return redirect(url_for("auth.register"))

        if role != "customer" and role != "admin":
            flash("Invalid role!", category="error")
            return redirect(url_for("auth.register"))

        if len(number) < 8 or len(number) > 15:
            flash(
                "Number should have a length between 8 and 15 characters",
                category="error",
            )
            # Add a return statement here to exit the function
            return redirect(url_for("auth.register"))

        # Check if the password has a length of 8 and contains mixed characters
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
            # Add a return statement here to exit the function
            return redirect(url_for("auth.register"))

        # All checks passed, proceed with user registration
        new_user = User(
            number=number,
            email=email,
            firstName=firstName,
            lastName=lastName,
            role=role,
            password=generate_password_hash(password1, method="pbkdf2:sha256"),
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully", category="success")
        return redirect(url_for("auth.login"))

    # Render the registration form
    return render_template("register.html", user=current_user)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
