"""Flask App configuration."""
"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config."""

    SECRET_KEY = environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


class ProdConfig(Config):
    """Production config."""

    FLASK_ENV = "production"
    FLASK_DEBUG = False
    DATABASE_URI = environ.get("PROD_DATABASE_URI")


class DevConfig(Config):
    """Development config."""

    FLASK_ENV = "development"
    FLASK_DEBUG = True
    DATABASE_URI = environ.get("DEV_DATABASE_URI")


SECRET_KEY = str(os.urandom(256))
DB_NAME = "database_db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

apiEndP = "192.168.100.150:3420"
