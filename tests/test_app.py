import unittest
from app import app, db
from models import User

class UserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def setUp(self):
        with app.app_context():
            db.session.query(User).delete()
            db.session.commit()

    def test_register_user_success(self):
        res = self.app.post('/user/register', json={
            "name": "Test User",
            "email": "test@gmail.com",
            "password": "password123",
            "age": 25
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("id", res.json)
        self.assertIn("username", res.json)

    def test_register_user_short_password(self):
        res = self.app.post('/user/register', json={
            "name": "Test User",
            "email": "test2@gmail.com",
            "password": "short",
            "age": 25
        })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json["error"], "Password must be at least 8 characters long.")

    def test_register_user_email_already_used(self):
        self.app.post('/user/register', json={
            "name": "Test User",
            "email": "test3@gmail.com",
            "password": "password123",
            "age": 25
        })
        res = self.app.post('/user/register', json={
            "name": "Another User",
            "email": "test3@gmail.com",
            "password": "password123",
            "age": 30
        })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json["error"], "Email already in use.")

    def test_get_all_users(self):
        self.app.post('/user/register', json={
            "name": "Test User",
            "email": "test4@gmail.com",
            "password": "password123",
            "age": 25
        })
        res = self.app.get('/users')
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json), 0)

    def test_get_user_by_id_success(self):
        self.app.post('/user/register', json={
            "name": "Mujahid",
            "email": "mujahid@gmail.com",
            "password": "password123",
            "age": 30
        })
    

        response = self.app.get('/users/1')  
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.json)
        self.assertEqual(response.json["name"], "Mujahid")

if __name__ == '__main__':
    unittest.main()

