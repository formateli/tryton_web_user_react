# This file is part of Tryton web user react project.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from functools import wraps
from trytond.config import config
from flask import current_app, request, Response, json

__all__ = ["WebUser", "wu_route"]

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

                current_app.logger.info('ORIGIN: ' + request.origin)
                current_app.logger.info('METHOD: ' + request.method)

                headers = {}
                if request.origin in wu.cors:
                    headers['Access-Control-Allow-Origin'] = request.origin
                    #headers['Access-Control-Max-Age'] = wu.timeout
                current_app.logger.info(str(headers))
                if request.method == 'OPTIONS':
                    #headers['Vary'] = 'Origin'
                    #method = request.headers.get('Access-Control-Request-Method')
                    #if method:
                    #    headers['Access-Control-Allow-Methods'] = method
                    headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
                    headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
                    #headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorizatio'
                    current_app.logger.info('PREFLIGHT HEADERS: ' + str(headers))
                    return Response('preflight ok', 200, headers)
                res = func()
                if isinstance(res, dict):
                    res = Response(json.dumps(res), 200)
                if isinstance(res, Response):
                    res.headers = headers
                    current_app.logger.info('RES HEADERS: ' + str(res.headers))
                return res
            return wrapper
        return decorator

wu_route = WebUser.route
