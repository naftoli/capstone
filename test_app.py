import os
import unittest
import json
from api import api
from app import create_app
from models import db, User, Favorite

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.register_blueprint(api)
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.admin_token = os.environ.get('ADMIN_TOKEN')
        self.user_token = os.environ.get('USER_TOKEN')
        db.create_all()
        # make sure we have at least one user
        users = User.query.all()
        if len(users) == 0:
            user = User(
                first_name='naftoli',
                last_name='rapoport',
                email='naftolir@gmail.com',
                password='1234'
            )
            user.insert()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_as_user(self):
        res = self.client().get('/', headers={'Authorization': 'Bearer ' + self.user_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['users']))

    def test_get_all_as_admin(self):
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

        res = self.client().get('/', headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['users']))

    def test_get_all_no_auth(self):
        # make sure we have at least one user
        users = User.query.all()
        if len(users) == 0:
            user = User(
                first_name='naftoli',
                last_name='rapoport',
                email='naftolir@gmail.com',
                password='1234'
            )
            user.insert()

        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_users_as_user(self):
        res = self.client().get('/users', headers={'Authorization': 'Bearer ' + self.user_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['users']))

    def test_get_users_as_admin(self):
        res = self.client().get('/users', headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['users']))

    def test_get_users_no_auth(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_user_by_id(self):
        res = self.client().get('/users/1', headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['id'], 1)

    def test_create_user(self):
        res = self.client().post('/users', headers={'Authorization': 'Bearer ' + self.admin_token},
                                 json={"first_name": "Jane", "last_name": "Doe", "email": "jane@doe.com", "password": "1234"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['user'])

    def test_add_favorite(self):
        res = self.client().post('/users/1/favorites', headers={'Authorization': 'Bearer ' + self.user_token},
                                 json={"user_id": 1, "link": "https://www.google.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_user(self):
        res = self.client().patch('/users/1', headers={'Authorization': 'Bearer ' + self.admin_token},
                                  json={"first_name": "Jane"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['first_name'], "Jane")

    def test_update_favorite(self):
        res = self.client().patch('/users/1/favorites/1', headers={'Authorization': 'Bearer ' + self.user_token},
                                  json={"link": "https://www.updatedlink.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_user(self):
        res = self.client().delete('/users/1', headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

if __name__ == "__main__":
    unittest.main()