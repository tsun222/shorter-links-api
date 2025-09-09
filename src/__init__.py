from flask import Flask
from .extensions import db
from .models import Url
from .routes import bp
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    