import unittest
import json
import requests
from app import create_app
from models import setup_db, User, Favorite
from flask_sqlalchemy import SQLAlchemy

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_api"
        self.database_path = "sqlite://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        #binds app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #create all tables
            self.db.create_all()

        self.set_tokens()

    def set_tokens(self):
        manager_url = "https://dev-inm1j600yp4jk16p.us.auth0.com/authorize/?audience=capstone&client_id=U2SPlOSDU4AWFmxPsnYro73MRTQPtGl7&client_secret=drZDTXsmbgapjoJjxyTgkTyBYaQO-oG-h7Fbz1u35KAk-pcTe8MzZRMKeT7FEw6M&response_type=token&redirect_uri=https://mashpia.com/udacity_login"
        reg_user_url = "https://dev-inm1j600yp4jk16p.us.auth0.com/authorize/?audience=capstone&client_id=U2SPlOSDU4AWFmxPsnYro73MRTQPtGl7&client_secret=drZDTXsmbgapjoJjxyTgkTyBYaQO-oG-h7Fbz1u35KAk-pcTe8MzZRMKeT7FEw6M&response_type=token&redirect_uri=https://mashpia.com/udacity_login"

        if not self.manager_token:
            # set the user credentials
            username = "naftolir@gmail.com"
            password = "Naftoli8770!"

            # send a POST request to the authentication endpoint
            response = requests.post(manager_url, json={"username": username, "password": password})
            data = json.loads(response.text)
            self.manager_token = data['access_token']

        if not self.reg_user_token:
            # set the user credentials
            username = "user@mashpia.com"
            password = "Naftoli8770!"

            # send a POST request to the authentication endpoint
            response = requests.post(reg_user_url, json={"username": username, "password": password})
            data = json.loads(response.text)
            self.reg_user_token = data['access_token']

    def tearDown(self):
        pass

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
                                 json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['user'])

    def test_add_favorite(self):
        res = self.client().post('/users/1/favorites', headers={'Authorization': f'Bearer {self.user_token}'},
                                 json=self.new_favorite)
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
        res = self.client().patch('/users/1/favorites/1', headers={'Authorization': f'Bearer {self.user_token}'},
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