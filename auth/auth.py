import os
import json
from flask import request, _request_ctx_stack, abort, session, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from urllib.error import HTTPError


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
ALGORITHMS = os.environ.get("AUTH0_ALGORITHM").split(",")
API_IDENTIFIER = os.environ["API_IDENTIFIER"]

## AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            return parts[1]
        else:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must be in the format Bearer token.'
            }, 401)
    elif session.get('jwt_token'):
        return session.get('jwt_token')
    else:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)


def check_permissions(permission, payload):
    # Check if permissions are included in the payload
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    # Check if the requested permission is in the payload permissions array
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def verify_decode_jwt(token):
    # Get the header from the token
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    # Verify the token is an Auth0 token with key id (kid)
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # Get the public key from Auth0
    try:
        jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
        jwks = json.loads(urlopen(jwks_url).read())
    except HTTPError as e:
        raise AuthError({
            'code': 'invalid_header',
            'description': f'Unable to find appropriate key: {str(e)}'
        }, 401)
    except Exception as e:
        raise AuthError({
            'code': 'connection_error',
            'description': f'Could not connect to JWKS URL: {str(e)}'
        }, 500)

    # Find the key that matches the kid
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Verify and decode the token
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims, please check the audience and issuer.'
            }, 401)
        except Exception as e:
            raise AuthError({
                'code': 'invalid_header',
                'description': f'Unable to parse authentication token: {str(e)}'
            }, 401)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find appropriate key.'
    }, 403)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as err:
                return jsonify({
                    'success': False,
                    'error': err.status_code,
                    'message': err.error['description']
                }), err.status_code
            except Exception as e:
                abort(401)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator