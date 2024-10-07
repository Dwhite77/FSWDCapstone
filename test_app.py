import unittest
import json
from app import create_app  # Assuming you have a function to create your Flask app
from models import setup_db  # Assuming you have a function to set up your database

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"  # Use a test database
        setup_db(self.app, self.database_name)

        self.new_actor = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male'
        }

        self.auth_header = {
            'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRWQjBmdkRLcUNfLS1CampYbU1QcCJ9.eyJpc3MiOiJodHRwczovL2Rldi1uMmIzYzIxNnZ2aHd3NWplLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmZmZGNlMzg2MTg3M2JkNjcwN2MyZWMiLCJhdWQiOiJDYXBzdG9uZSIsImlhdCI6MTcyODMwMjA1MSwiZXhwIjoxNzI4MzA5MjUxLCJzY29wZSI6IiIsImF6cCI6ImprcGxZYTd3Sk5EWUFrQ0I4MlJxZEVybmpSUjdOYWV4IiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiYWRkOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwidXBkYXRlOmFjdG9yIiwidXBkYXRlOm1vdmllIl19.ay52h519dCPAUxCdl7VsdKOumLF0M6GAhZO0Z7qOq72Alxf9crVZ5cw1LQYWquNMhDvj9dvPxv7KbnBgy3_VWyzyXCk5p1UI-_S8V0XkdjfMPHdn7JxdDKXW8fPCh0geYyYJQBzbjmFm-xYWWqf-X71EHQ6tUU2raWsJOFnfdtn_qTKlxZx52bQG_372GSzZv9Gk-ElQj3EThewn33al7drf9w605oGAeoG_C6g27Po_zJo1sEO8iIr0xK4nrh2SLneEjfaZ3SR5LiDnpbrnWoYiYxsCMuHK_8riM8tGI54KRZ_NaZMEZyOBsZAEQ8yAha4lboKshnuiGKc1AKGRtQ&expires_in=7200&token_type=Bearer'  # Replace with a valid token for testing
        }

    def test_get_actors(self):
        """Test getting actors."""
        res = self.client().get('/actors', headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']) > 0)  # Check if there are actors returned

    def test_add_actor_success(self):
        """Test adding an actor successfully."""
        res = self.client().post('/actors', json=self.new_actor, headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])  # Check if an actor ID is returned

    def test_add_actor_error(self):
        """Test adding an actor with missing data."""
        incomplete_actor = {
            'name': 'Jane Doe'
            # Missing 'age' and 'gender'
        }
        res = self.client().post('/actors', json=incomplete_actor, headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)  # Bad request
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')  # Adjust based on your error handling

    def test_rbac(self):
        """Test RBAC for different roles."""
        # Test with a role that has permission
        res = self.client().post('/actors', json=self.new_actor, headers=self.auth_header)
        self.assertEqual(res.status_code, 201)

        # Test with a role that does not have permission
        # You may need to create a different token for a role without permission
        unauthorized_header = {
            'Authorization': 'Bearer YOUR_UNAUTHORIZED_TEST_JWT_TOKEN'
        }
        res = self.client().post('/actors', json=self.new_actor, headers=unauthorized_header)
        self.assertEqual(res.status_code, 403)  # Forbidden

if __name__ == '__main__':
    unittest.main()