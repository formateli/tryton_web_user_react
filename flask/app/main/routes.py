# This file is part of Tryton web user react project.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import functools
from flask import request, current_app, json, Response
from app import tryton, wu
from app.main import bp
from trytond.res.user import PasswordError
from trytond.modules.web_user.exceptions import UserValidationError

#def tryton_route(func):
#    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
#        args_repr = [repr(a) for a in args]
#        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
#        signature = ", ".join(args_repr + kwargs_repr)
#        #raise Exception('Database name: ' + signature)
#        #return func(*args, **kwargs)
#        if request.method == 'OPTIONS':
#            return Response('preflight ok', 200, {
#                'Access-Control-Allow-Origin':'*',
#                'Access-Control-Allow-Methods':'GET,POST,PUT,DELETE',
#                'Access-Control-Allow-Headers':'Origin, X-Requested-With, Content-Type, Accept, Authorization'
#                })
#        #raise Exception('METHOD: ' + request.method)
#        return func()
#    return wrapper


@bp.route('/<database_name>/web-user-register', methods=['OPTIONS', 'POST'])
@wu.route()
@tryton.transaction()
def web_user_register():
    User = tryton.pool.get('res.user')
    WebUser = tryton.pool.get('web.user')
    args = request.get_json(False)
    current_app.logger.info(str(args))
    try:
        user = WebUser.search([('email', '=', args['username'])])
        if user:
            return Response('User already exists.', 403)
        user = WebUser.create_web_user(tryton.pool, args)
        User.validate_password(args['password'], [user])
        user.save()
        return user.to_json()

        #TODO Send confirmation email

    except (PasswordError, UserValidationError) as e:
        return Response(e, 403)
    except Exception as e:
        current_app.logger.info(str(e))
        return Response(e, 500)


@bp.route('/<database_name>/web-user-tokens',
        methods=['OPTIONS', 'POST', 'PUT', 'DELETE'])
@wu.route()
@tryton.transaction()
def web_user_token():
    WebUser = tryton.pool.get('web.user')
    UserSession = tryton.pool.get('web.user.session')

    auth = request.authorization

    try:
        if request.method == 'DELETE':
            #logger.info('DELETE %s', auth.token)
            UserSession.remove(auth.token)
            return Response(None, 204)

        if request.method == 'POST':
            user = WebUser.authenticate(auth['username'], auth['password'])
            if user is None:
                #logger.info('POST not found %s', auth['username'])
                return Response('Not found.', 401)
            #logger.info("POST user found: %s", user.email)
            key = user.new_session()
            return {'access_token': key}

        if request.method == 'PUT':
            sessions = UserSession.search([('key', '=', auth.token)])
            session = None
            if sessions:
                session = sessions[0]
            if session is None:
                return Response('Session not found.', 404)
            key = session.key
            if session.expired:
                #logger.info('PUT session expired %s', key)
                if not user.stay_logged_in:
                    return Response('Session expired.', 401)
                user = session.user
                UserSession.remove(session.key)
                key = user.new_session()
                #logger.info('PUT renew session %s', key)
            return {'access_token': key}

        return Response('Invalid request method.', 405)

    except Exception as e:
        return Response(e, 500)


@bp.route('/<database_name>/web-user-me', methods=['OPTIONS', 'GET'])
@wu.route()
@tryton.transaction()
def web_user_me():
    WebUser = tryton.pool.get('web.user')
    auth = request.authorization
    try:
        user = WebUser.get_user(auth.token)
        if user is None:
            return Response('Invalid', 401)
        current_app.logger.info(user.to_json())
        return user.to_json()
    except Exception as e:
        current_app.logger.info(str(e))
        return Response(str(e), 500)

    #return Response('ok', 200, {'Access-Control-Allow-Origin':'*'})
