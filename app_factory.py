from flask_restplus import Api
from flask_jwt import JWT
from flask import Flask
import os

from controllers.category import api as category_api
from controllers.article import api as article_api
from controllers.user import api as user_api
from security import authenticate, identity
from config import app_config
from db import db


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.secret_key = os.getenv('SECRET_KEY') or 'keep it in ur pocket!'

    api = Api(app, title="Restful API", description="Blogging App")
    register_api(api)

    init_extensions(app)

    return app


def register_api(api):
    api.add_namespace(article_api)
    api.add_namespace(category_api)
    api.add_namespace(user_api)


def init_extensions(app):
    jwt = JWT(app, authenticate, identity)
    db.init_app(app)