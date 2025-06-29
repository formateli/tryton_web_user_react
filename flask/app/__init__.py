# This file is part of Tryton web user react project.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import os
import logging
from logging.handlers import RotatingFileHandler
from config import Config
from flask import Flask
from flask_tryton import Tryton
from app.web_user import WebUser

tryton = Tryton()
wu = WebUser()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    tryton.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists(app.config['LOG_PATH']):
            os.mkdir(app.config['LOG_PATH'])
        file_handler = RotatingFileHandler(app.config['LOG_PATH'] + '/web-user.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Web User startup')

    wu.init_app(app)

    return app
