# This file is part of Tryton web user react project.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from flask import request, Response, current_app
from app import tryton, wu
from app.main import bp
from trytond.modules.web_user_routes.web_user_routes import WebUserRoutes


@bp.route('/<database_name>/web-user-register', methods=['OPTIONS', 'POST'])
@wu.route()
@tryton.transaction()
def web_user_register():
    wur = WebUserRoutes(Response, current_app.logger)
    return wur.web_user_register(request, tryton.pool)


@bp.route('/<database_name>/web-user-tokens',
        methods=['OPTIONS', 'POST', 'PUT', 'DELETE'])
@wu.route()
@tryton.transaction()
def web_user_token():
    wur = WebUserRoutes(Response, current_app.logger)
    return wur.web_user_token(request, tryton.pool)


@bp.route('/<database_name>/web-user-me', methods=['OPTIONS', 'GET'])
@wu.route()
@tryton.transaction()
def web_user_me():
    wur = WebUserRoutes(Response, current_app.logger)
    return wur.web_user_me(request, tryton.pool)
