import unittest
from app import app, db
from models import User

class UserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()


    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_register_user_success(self):
        res = self.app.test_client().post('/user/register', json={
            "name": "Test User",
            "email": "test@gmail.com",
            "password": "password123",
            "age": 25
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("id", res.json)
        self.assertIn("username", res.json)

    def test_register_user_short_password(self):
        res = self.app.test_client().post('/user/register', json={
            "name": "Test User",
            "email": "test2@gmail.com",
            "password": "short",
            "age": 25
        })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json["error"], "Password must be at least 8 characters long.")

    def test_register_user_email_already_used(self):
        self.app.test_client().post('/user/register', json={
            "name": "Test User",
            "email": "test3@gmail.com",
            "password": "password123",
            "age": 25
        })
        res = self.app.test_client().post('/user/register', json={
            "name": "Another User",
            "email": "test3@gmail.com",
            "password": "password123",
            "age": 30
        })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json["error"], "Email already in use.")

    def test_get_all_users(self):
        self.app.test_client().post('/user/register', json={
            "name": "Test User",
            "email": "test4@gmail.com",
            "password": "password123",
            "age": 25
        })
        res = self.app.test_client().get('/users')
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json), 0)

    def test_get_user_by_id_success(self):
    # First, register a user to ensure there is a user to retrieve
        self.app.test_client().post('/user/register', json={
            "name": "Mujahid",
            "email": "mujahid@gmail.com",
            "password": "password123",
            "age": 30
        })
    
    # Now, attempt to get the user by ID
        response = self.app.test_client().get('/users/1')  # Use the test client
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.json)
        self.assertEqual(response.json["name"], "Mujahid")
    

if __name__ == "__main__":
    unittest.main()


