# This file is part of Tryton web user react project.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from functools import wraps
from trytond.config import config
from flask import current_app, request, Response, json

__all__ = ["WebUser"]


class WebUser:

    def __init__(self):
        self.cors = []
        self.timeout = None

    def init_app(self, app):
        cors = filter(None, config.get(
            'web', 'cors', default='').splitlines())
        for c in cors:
            self.cors.append(c)
        self.timeout = config.getint('web', 'cache_timeout')
        app.extensions['WebUser'] = self

    @staticmethod
    def route():
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                wu = current_app.extensions['WebUser']

                headers = {}
                if request.origin in wu.cors:
                    headers['Access-Control-Allow-Origin'] = request.origin
                    headers['Vary'] = 'Origin'
                if request.method == 'OPTIONS':
                    headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
                    headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
                    headers['Access-Control-Max-Age'] = wu.timeout
                    return Response('preflight ok', 200, headers)
                res = func()
                if isinstance(res, dict):
                    res = Response(json.dumps(res), 200)
                if isinstance(res, Response):
                    res.headers = headers
                return res
            return wrapper
        return decorator
