from flask import Blueprint, jsonify, abort, request, redirect, session
from models import User, Favorite
from auth import AuthError, requires_auth
import requests
import urllib

api = Blueprint('api', __name__)

AUTH0_DOMAIN = 'tzivos.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'
CLIENT_ID = 'JVkv4cfioDI34UU9M12Kn6QseInZIGdZ'
CLIENT_SECRET = 'LEuarqV8ADC38eXI4t6SWOU_C_1zbqQqq61z9-antoM7RKhupBh6bMpcO-oxrPfs'

# ROUTES
@api.route('/login')
def login():
    return redirect('https://' + AUTH0_DOMAIN + '/authorize?audience=' + API_AUDIENCE + '&response_type=token&client_id=' + CLIENT_ID + '&redirect_uri=' + request.host_url + 'login-results')

@api.route('/login-results')
def callback_handling():
    pieces = urllib.parse.urlparse(request.url)
    print(pieces)
    return "Logged in"

@api.route('/logout')
def logout():
    return redirect('https://' + AUTH0_DOMAIN + '/v2/logout?audience=' + API_AUDIENCE + '&client_id=' + CLIENT_ID + '&returnTo=' + request.host_url + 'logout-results')

@api.route('/logout-results')
def loggedout():
    return "Logged out"

@api.route('/admin-login')
def admin_login():
    TMP_CLIENT_ID = 'uUKRtQr1XSC5ZGfwb1s5hYvLDfQ1BChT'
    TMP_CLIENT_SECRET = 'DmXVlcTPPqOeZbbPSK22RU--hplvVHdJ_PGjy0WkyOUGMkqh6eNTW6_6kwGY1YMA'
    username = 'admin@gmail.com'
    password = 'admin@5783!'
    access_token = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        data={
            "client_id": TMP_CLIENT_ID,
            "client_secret": TMP_CLIENT_SECRET,
            "audience": API_AUDIENCE,
            "username": username,
            "password": password,
            "grant_type": "client_credentials",
        },
    ).json()["access_token"]
    print(access_token)
    session['admin_token'] = 'Bearer ' + access_token
    return "Logged in"

@api.route('/user-login')
def user_login():
    TMP_CLIENT_ID = 'uUKRtQr1XSC5ZGfwb1s5hYvLDfQ1BChT'
    TMP_CLIENT_SECRET = 'DmXVlcTPPqOeZbbPSK22RU--hplvVHdJ_PGjy0WkyOUGMkqh6eNTW6_6kwGY1YMA'
    username = 'user@gmail.com'
    password = 'user@5783!'
    access_token = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        data={
            "client_id": TMP_CLIENT_ID,
            "client_secret": TMP_CLIENT_SECRET,
            "audience": API_AUDIENCE,
            "username": username,
            "password": password,
            "grant_type": "client_credentials",
        },
    ).json()["access_token"]
    session['token'] = 'Bearer ' + access_token
    print(access_token)
    return "Logged in"

@api.route('/', methods=['GET'])
@requires_auth('get:all')
def get_all(payload):
    ''' get all users and their favorite links '''
    users = User.query.all()
    if not users:
        abort(400)

    info = []
    for user in users:
        info.append({
            'user': user.format(),
            'favorites': [f.link for f in user.get_favorite_links()]
        })

    return jsonify({
        'success': True,
        'users': info
    }), 200

@api.route('/users', methods=['GET'])
@requires_auth('get:users')
def get_users(payload):
    ''' get users from database '''
    users = User.query.all()
    if not users:
        abort(400)

    return jsonify({
        'success': True,
        'users': [u.format() for u in users]
    }), 200

@api.route('/users/<int:user_id>', methods=['GET'])
@requires_auth('get:user')
def get_user(payload, user_id):
    ''' get user from database '''
    user = User.query.get(user_id)
    if not user:
        abort(400)

    return jsonify({
        'success': True,
        'user': user.format()
    }), 200

@api.route('/users', methods=['POST'])
@requires_auth('post:user')
def create_user(payload):
    ''' create user in database '''
    body = request.get_json()
    if not body:
        abort(400)

    try:
        user = User(
            first_name=body.get('first_name'),
            last_name=body.get('last_name'),
            email=body.get('email'),
            password=body.get('password')
        )
        user.insert()
    except:
        abort(400)

    return jsonify({
        'success': True,
        'user': user.format()
    }), 200

@api.route('/users/<int:user_id>/favorites', methods=['POST'])
@requires_auth('post:favorite')
def add_favorite(payload, user_id):
    ''' add user favorite link to database '''
    user = User.query.get(user_id)
    if not user:
        abort(400)

    body = request.get_json()
    if not body:
        abort(400)

    try:
        favorite = Favorite(
            user_id=user_id,
            link=body.get('link')
        )
        favorite.insert()
    except:
        abort(400)

    return jsonify({
        'success': True,
        'favorite': favorite.format()
    }), 200

@api.route('/users/<int:user_id>', methods=['PATCH'])
@requires_auth('patch:user')
def update_user(payload, user_id):
    ''' update user in database '''
    user = User.query.get(user_id)
    if not user:
        abort(400)

    body = request.get_json()
    if not body:
        abort(400)

    try:
        user.first_name = body.get('first_name', user.first_name)
        user.last_name = body.get('last_name', user.last_name)
        user.email = body.get('email', user.email)
        user.password = body.get('password', user.password)
        user.update()
    except:
        abort(400)

    return jsonify({
        'success': True,
        'user': user.format()
    }), 200

@api.route('/users/<int:user_id>/favorites/<int:favorite_id>', methods=['PATCH'])
@requires_auth('patch:favorite')
def update_favorite(payload, user_id, favorite_id):
    ''' update user favorite link in database '''
    user = User.query.get(user_id)
    if not user:
        abort(400)

    favorite = Favorite.query.get(favorite_id)
    if not favorite:
        abort(400)

    body = request.get_json()
    if not body:
        abort(400)

    try:
        favorite.link = body.get('link', favorite.link)
        favorite.update()
    except:
        abort(400)

    return jsonify({
        'success': True,
        'favorite': favorite.format()
    }), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
@requires_auth('delete:user')
def delete_user(payload, user_id):
    ''' delete user from database '''
    user = User.query.get(user_id)
    if not user:
        abort(400)

    try:
        user.delete()
    except:
        abort(400)

    return jsonify({
        'success': True
    }), 200

@api.route('/users/<int:user_id>/favorites/<int:favorite_id>', methods=['DELETE'])
@requires_auth('delete:favorite')
def delete_favorite(payload, user_id, favorite_id):
    ''' delete user favorite link from database '''
    user = User.query.get(user_id)
    if not user:
        abort(400)

    favorite = Favorite.query.get(favorite_id)
    if not favorite:
        abort(400)

    try:
        favorite.delete()
    except:
        abort(400)

    return jsonify({
        'success': True
    }), 200

''' setup error handling '''
@api.errorhandler(400)
def invalid_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'error executing request'
    }), 400

@api.errorhandler(401)
def invalid_auth(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'invalid authentication'
    }), 401

@api.errorhandler(403)
def no_permission(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'invalid permissions'
    }), 403

@api.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404

@api.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
        'success': False,
        'error': e.status_code,
        'message': e.error
    }), e.status_code