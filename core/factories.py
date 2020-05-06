import sys
import os.path as op
import logging

import prance
from pathlib import Path
from flask import jsonify, g, session
from connexion import FlaskApp
from connexion.resolver import RestyResolver
from flask.logging import default_handler
from app.client import client

from core.extensions import db, ma, migrator, jwt, login_manager, babel, cors
from app.data.models import Customer


settings = {
    "development": "core.settings.DevelopmentConfig",
    "production": "core.settings.ProductionConfig",
    "testing": "core.settings.TestingConfig",
    "default": "core.settings.DevelopmentConfig",
}


class SettingsError(Exception):
    pass


class SwaggerError(Exception):
    pass


def get_config(setting_name):
    if settings.get(setting_name):
        return settings.get(setting_name)
    else:
        raise SettingsError("Given settings name does not exists: %s" % setting_name)


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrator.init_app(app)
    jwt.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.blueprint_login_views = {
        'client': 'client.login'
    }
    cors.init_app(app)
    # socket.init_app(app)

    return None


def get_bundled_specs(main_file):
    parser = prance.ResolvingParser(url=str(main_file.absolute()),
                                    lazy=True, backend='openapi-spec-validator')
    parser.parse()
    return parser.specification


def register_api(app):
    app.add_api(get_bundled_specs(Path('api_specs/admin-api.yaml')),
                resolver=RestyResolver('app.admin_api.controllers'))
    return None


def register_logger(app):
    log_formatter = logging.Formatter(
        "[%(asctime)s] - %(levelname)s - %(name)s - %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(log_formatter)
    if app.config["DEBUG"]:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)
    app.logger.removeHandler(default_handler)

    return None


def register_error_handlers(app):
    def create_error_handler(status_code, message):
        def error_handler(error):
            return jsonify(message=message), status_code

        return error_handler

    app.register_error_handlers(400, create_error_handler(400, "Bad request"))
    app.register_error_handlers(401, create_error_handler(401, "Unathorized"))
    app.register_error_handlers(403, create_error_handler(403, "Forbidden"))
    app.register_error_handlers(404, create_error_handler(404, "Not found"))


def create_app(config_name):
    config_obj = get_config(config_name)
    swagger_dir = op.abspath(op.join(op.dirname(__name__), 'api_specs'))
    print(swagger_dir)
    cnnx_app = FlaskApp(__name__, specification_dir=swagger_dir)
    flask_app = cnnx_app.app

    flask_app.config.from_object(config_obj)
    flask_app.app_context().push()

    login_manager.init_app(flask_app)
    flask_app.register_blueprint(client, url_prefix='/')

    register_logger(flask_app)
    register_extensions(flask_app)
    register_api(cnnx_app)

    return flask_app


@babel.localeselector
def get_locale():
    if session.get('locale') is None:
        session['locale'] = 'az'
    return session.get('locale')


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


@login_manager.user_loader
def load_user(user_id):
    return Customer.get(id=user_id)
