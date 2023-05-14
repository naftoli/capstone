import unittest
import json
import requests
from api import api
from app import create_app
from models import db, setup_db, User, Favorite
import jwt

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.register_blueprint(api)
        self.client = self.app.test_client
        self.manager_token = None
        self.reg_user_token = None
        self.set_tokens()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def set_tokens(self):
        secret_key = 'capstone'
        if self.manager_token == None:
            payload = {
                'user_id': 1,
                'username': 'naftoli@gmail.com',
                'password': 'Naftoli8770!',
                'permissions': ['get:all', 'get:user', 'get:users', 'post:favorite', 'delete:favorite']
            }
            self.manager_token = jwt.encode(payload, secret_key, algorithm='HS256')
        if self.reg_user_token == None:
            payload = {
                'user_id': 2,
                'username': 'user@mashpia.com',
                'password': 'Naftoli8770!',
                'permissions': ['get:all', 'get:user', 'get:users']
            }
            self.reg_user_token = jwt.encode(payload, secret_key, algorithm='HS256')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all(self):
        #make sure we have at least one user
        users = User.query.all()
        if len(users) == 0:
            user = User(
                first_name='naftoli',
                last_name='rapoport',
                email='naftolir@gmail.com',
                password='1234'
            )
            user.insert()

        res = self.client().get('/', headers={'Authorization': f'Bearer {self.manager_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['users']))

    def test_get_users(self):
        res = self.client().get('/users', headers={'Authorization': f'Bearer {self.manager_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['users']))

    def test_get_user(self):
        res = self.client().get('/users/1', headers={'Authorization': f'Bearer {self.manager_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['id'], 1)

    def test_create_user(self):
        res = self.client().post('/users', headers={'Authorization': f'Bearer {self.manager_token}'},
                                 json={"first_name": "Jane", "last_name": "Doe", "email": "jane@doe.com", "password": "1234"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['user'])

    def test_add_favorite(self):
        res = self.client().post('/users/1/favorites', headers={'Authorization': f'Bearer {self.reg_user_token}'},
                                 json={"user_id": 1, "link": "https://www.google.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['favorite'])

    def test_update_user(self):
        res = self.client().patch('/users/1', headers={'Authorization': f'Bearer {self.manager_token}'},
                                  json={"first_name": "Jane"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['first_name'], "Jane")

    def test_update_favorite(self):
        res = self.client().patch('/users/1/favorites/1', headers={'Authorization': f'Bearer {self.reg_user_token}'},
                                  json={"link": "https://www.updatedlink.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['favorite']['link'], "https://www.updatedlink.com")

    def test_delete_user(self):
        res = self.client().delete('/users/1', headers={'Authorization': f'Bearer {self.manager_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

if __name__ == "__main__":
    unittest.main()