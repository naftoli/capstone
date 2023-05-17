import unittest
import json
from api import api
from app import create_app
from models import db, setup_db, User, Favorite
import jwt

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.register_blueprint(api)
        self.client = self.app.test_client
        #self.set_tokens()
        self.manager_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklyM0xEVTFLaGVsTkt4X2Ytd2h6MCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pbm0xajYwMHlwNGprMTZwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDRhYTE0MGFhMWQyOGI3NmFkMzIyOGIiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY4NDMzODgxMCwiZXhwIjoxNjg0MzQ2MDEwLCJhenAiOiJVMlNQbE9TRFU0QVdGbXhQc25Zcm83M01SVFFQdEdsNyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmZhdm9yaXRlIiwiZGVsZXRlOnVzZXIiLCJnZXQ6YWxsIiwiZ2V0OnVzZXIiLCJnZXQ6dXNlcnMiLCJwYXRjaDpmYXZvcml0ZSIsInBhdGNoOnVzZXIiLCJwb3N0OmZhdm9yaXRlIiwicG9zdDp1c2VyIl19.fsSpI5OtLXyQr7BdBMDnorNbPGcSSOCwMXlJZpCyISupmp5g5kBe-Cdwt9EW3Ro2ZBBt0LbeAM4Ie5yyL4oot4_1ItETIhhvv9RIH_wpZ77DnsPnh0qvx9CIRPbwvIkPmg1ezI28o3DAvFdujYbrzYNuMWA53HpVe-mj7KwwFqaY96Vxq0cWQ09wWSjhcgxvi3THa80W0bBZgqUX7bNC1pLoULGGVBJxbSHVK2FdGVT3ydjNZHo4XwpIofIvMVSNF7iLl57RIUMfVe0ie9K7tL_LMUjcmRHSMiZ4Od5tQjMftoYHQEx46IMeaBDWTAzSw1qPiaGoUpyi5XfQsD4L7w'
        self.reg_user_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklyM0xEVTFLaGVsTkt4X2Ytd2h6MCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pbm0xajYwMHlwNGprMTZwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDRhYTE1ZTlhYmQwMzg2NGJmZDFlZGYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY4NDMzODk3NywiZXhwIjoxNjg0MzQ2MTc3LCJhenAiOiJVMlNQbE9TRFU0QVdGbXhQc25Zcm83M01SVFFQdEdsNyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFsbCIsImdldDp1c2VyIiwiZ2V0OnVzZXJzIl19.KirCR58klT1TUUZq9vmf0GdX_rNx-y50cIOVVtVxiO9-zNGGQpqxE6zJ0ZnKxAxd7qNOxF5zGdelq4g4Lw0ACRDmz1aIumRzbHyMOnnK4sHea_FGWXPRl4DeUGi0HezvsTET46XPzxPKk-hp7qAjjQdiETKAL-VP_TTY8HLnflqvR7XIYhlmBVZj3XpUroY1DE1JkZs_st1Ld1MR7lRFStOUZq5SR5kTAAMZUVQycOPLOmEScHG8jVEcqhjrk9LMxGyqHiBPBTpir8jp-uDIyAB0IgruDlI6l5zn0wCXWe0RHjFt_Gr4_C4Uu08CP3TCCFNitBJWTcjEvlbtxICInA'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def set_tokens(self):
        secret_key = 'capstone'
        ''' create token for manager '''
        payload = {
            'user_id': 1,
            'username': 'naftoli@gmail.com',
            'password': '123456',
            'permissions': ['get:all', 'get:user', 'get:users', 'post:favorite', 'delete:favorite']
        }
        self.manager_token = jwt.encode(payload, secret_key, algorithm='HS256')

        ''' create token for regular user '''
        payload = {
            'user_id': 2,
            'username': 'user@mashpia.com',
            'password': '123456',
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

        res = self.client().get('/', headers={'Authorization': 'Bearer ' + self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['users']))

    def test_get_users(self):
        res = self.client().get('/users', headers={'Authorization': 'Bearer ' + self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['users']))

    def test_get_user(self):
        res = self.client().get('/users/1', headers={'Authorization': 'Bearer ' + self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['id'], 1)

    def test_create_user(self):
        res = self.client().post('/users', headers={'Authorization': 'Bearer ' + self.manager_token},
                                 json={"first_name": "Jane", "last_name": "Doe", "email": "jane@doe.com", "password": "1234"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['user'])

    def test_add_favorite(self):
        res = self.client().post('/users/1/favorites', headers={'Authorization': 'Bearer ' + self.reg_user_token},
                                 json={"user_id": 1, "link": "https://www.google.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_user(self):
        res = self.client().patch('/users/1', headers={'Authorization': 'Bearer ' + self.manager_token},
                                  json={"first_name": "Jane"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['first_name'], "Jane")

    def test_update_favorite(self):
        res = self.client().patch('/users/1/favorites/1', headers={'Authorization': 'Bearer ' + self.reg_user_token},
                                  json={"link": "https://www.updatedlink.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_user(self):
        res = self.client().delete('/users/1', headers={'Authorization': 'Bearer ' + self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

if __name__ == "__main__":
    unittest.main()