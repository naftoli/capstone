import os
import jwt

def create_tokens():
    secret_key = 'capstone'
    ''' create token for manager '''
    payload = {
        'user_id': 1,
        'username': 'naftoli@gmail.com',
        'password': '123456',
        'permissions': ['get:all', 'get:user', 'get:users', 'post:favorite', 'delete:favorite']
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    os.environ['MANAGER_TOKEN'] = token

    ''' create token for regular user '''
    payload = {
        'user_id': 2,
        'username': 'user@mashpia.com',
        'password': '123456',
        'permissions': ['get:all', 'get:user', 'get:users']
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    os.environ['REG_USER_TOKEN'] = token