import json
from flask import request
from functools import wraps
from urllib.request import urlopen
from jose import jwt

AUTH0_DOMAIN = 'dev-inm1j600yp4jk16p.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'
CLIENT_ID = 'U2SPlOSDU4AWFmxPsnYro73MRTQPtGl7'
CLIENT_SECRET = 'drZDTXsmbgapjoJjxyTgkTyBYaQO-oG-h7Fbz1u35KAk-pcTe8MzZRMKeT7FEw6M'

## AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'auth_missing',
            'description': 'Authorization header is missing.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Missing Bearer Token.'
        }, 401)

    numParts = len(parts)
    if numParts == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Missing Token.'
        }, 401)
    elif numParts > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Auth Header must be Bearer token.'
        }, 401)

    token = parts[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'missing_permissions',
            'description': 'No permissions found in token.'
        }, 403)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'No permission.'
        }, 403)

    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
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
                'description': 'Incorrect claims. Please check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse the authentication token.'
            }, 403)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 403)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator