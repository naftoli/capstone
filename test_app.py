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
        self.admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkszNUZFZE9PSkR4TlRKQjRxRU8xcyJ9.eyJpc3MiOiJodHRwczovL3R6aXZvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjQ2NTJhMzhjMmI4MzgwZDliZGJlMjUwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2ODQ0MjkyNDQsImV4cCI6MTY4NDUxNTY0NCwiYXpwIjoiSlZrdjRjZmlvREkzNFVVOU0xMktuNlFzZUluWklHZFoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpmYXZvcml0ZSIsImRlbGV0ZTp1c2VyIiwiZ2V0OmFsbCIsImdldDp1c2VyIiwiZ2V0OnVzZXJzIiwicGF0Y2g6ZmF2b3JpdGUiLCJwYXRjaDp1c2VyIiwicG9zdDpmYXZvcml0ZSIsInBvc3Q6dXNlciJdfQ.tLSK6oNFDUdrZ_xBo3iwKAZXkAwsw6liRq3rNg44T8yDnB_GocjSY5XjsumPl4t0kBc2eKFtQTc1Xs8eA9cNVCRi9kY-7_NVrOxYXQWSEpuiPIsEy2xsXpbIvwl-xoEyupqeOkYSQZA-riwUHUx550A8kWAzVsiowTpW-Aeg3dL-GYcljSh000q4cxYkE4fslfnOwmwfIQlZho37ucD5P8rqsrEYEdN9ZOfFjHUdd8u5mIhwNpClcok4yNxVS57zZjBeG_UPomo5hXnY1lOo23nOZTE5XXHQQxFNI6L-I8HJryZ-u0nleaLe68oGX9-VbFuFMYxL09U87-Em7cmrZw'
        self.user_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkszNUZFZE9PSkR4TlRKQjRxRU8xcyJ9.eyJpc3MiOiJodHRwczovL3R6aXZvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjQ2NTJhNTE3NDQ2Yzc0ZDY0YTllYTc1IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2ODQ0Mjk0NzQsImV4cCI6MTY4NDUxNTg3NCwiYXpwIjoiSlZrdjRjZmlvREkzNFVVOU0xMktuNlFzZUluWklHZFoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphbGwiLCJnZXQ6dXNlciIsImdldDp1c2VycyJdfQ.sxfn4NvYWbJqHuL8BYveOePd81F0s6iDH33qd6DszeO8ULcjouGSFETyYCEH7pTo4N03ObUELHHXf8ukO4_98G8PMdC_u4GfE5bjS_B7NpKFbtbywpxGwzp6bl9W_6Sv8njHftBrInfos_hMLCKrolTTrMU8UlzgQplJfBkGmnQoUttqyUYFdCNsqyVToItuG2j_iGZ_ckPhmiiYj9PUak84VLdZORbl7wPqW4TDjDhZwJh9KK5EcgW5LyWtbudUZesQkJ3Yfgpqo7CHusuMX7_hSc8B3o8Ag2pf7GDTGj52eLU7ZrmLy2NQLrhxUS05JJeYj6ZsrE1u1xV90He9xQ'
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