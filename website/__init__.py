from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
from uuid import UUID
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
from .models import User


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'

    app.config["SECRET_KEY"] = str(os.urandom(256))
    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp, url_prefix="/")

    from . import bookings

    app.register_blueprint(bookings.bp,url_prefix="/bookings")

    from . import customer

    app.register_blueprint(customer.bp, url_prefix="/customer")

    from . import dash

    app.register_blueprint(dash.bp, url_prefix="/dashboard")

    from . import drivers

    app.register_blueprint(drivers.bp, url_prefix="/drivers")

    from . import fuels

    app.register_blueprint(fuels.bp, url_prefix="/fuels")

    from . import geofence

    app.register_blueprint(geofence.bp, url_prefix="/geofence")

    from . import incomExpe

    app.register_blueprint(incomExpe.bp, url_prefix="/incomExpe")

    from . import reminder

    app.register_blueprint(reminder.bp, url_prefix="/reminder")

    from . import reports

    app.register_blueprint(reports.bp, url_prefix="/reports")

    from . import settings

    app.register_blueprint(settings.bp, url_prefix="/settings")

    from . import tracking

    app.register_blueprint(tracking.bp, url_prefix="/tracking")

    from . import users

    app.register_blueprint(users.bp, url_prefix="/users")

    from . import vehicles

    app.register_blueprint(vehicles.bp, url_prefix="/vehicles")

    from . import mail

    app.register_blueprint(mail.bp, url_prefix="/mail")

    from . import chgpswd

    app.register_blueprint(chgpswd.bp, url_prefix="/rest-pass")

    from . import models

    create_database(app)
    setup_login_manager(app)
    return app


def setup_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            # Parse the UUID string and retrieve the user
            user = User.query.get(user_id)
            return user
        except (ValueError, TypeError):
            return None


def create_database(app):
    from . import db
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("DB Created")
