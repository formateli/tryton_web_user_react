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
    return WebUserRoutes.web_user_register(
            Response, request, tryton.pool,
            current_app.logger, current_app.config['AUTH_EMAIL'])


@bp.route('/<database_name>/web-user-tokens',
        methods=['OPTIONS', 'POST', 'PUT', 'DELETE'])
@wu.route()
@tryton.transaction()
def web_user_token():
    return WebUserRoutes.web_user_token(
            Response, request, tryton.pool,
            current_app.logger, current_app.config['AUTH_EMAIL'])


@bp.route('/<database_name>/web-user-me', methods=['OPTIONS', 'GET'])
@wu.route()
@tryton.transaction()
def web_user_me():
    return WebUserRoutes.web_user_me(
            Response, request, tryton.pool, current_app.logger)


@bp.route('/<database_name>/web-user-password', methods=['OPTIONS', 'PUT'])
@wu.route()
@tryton.transaction()
def web_user_password():
    return WebUserRoutes.web_user_password(
            Response, request, tryton.pool, current_app.logger)


@bp.route('/<database_name>/web-user-avatar/<uuid>', methods={'OPTIONS', 'GET'})
@wu.route()
@tryton.transaction()
def web_user_avatar(uuid):
    return WebUserRoutes.web_user_avatar(
            Response, request, tryton.pool, current_app.logger, uuid)

@bp.route('/<database_name>/web-user-email-verify', methods={'OPTIONS', 'PUT'})
@wu.route()
@tryton.transaction()
def web_user_email_verify():
    return WebUserRoutes.web_user_email_verify(
            Response, request, tryton.pool, current_app.logger)
