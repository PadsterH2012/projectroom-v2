import unittest
from flask import url_for
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        response = self.client.post(url_for('main.register'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful!', response.data)

    def test_login(self):
        # First, register the user
        self.client.post(url_for('main.register'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'confirm_password': 'password'
        })

        # Then, log in with the registered user
        response = self.client.post(url_for('main.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_logout(self):
        # First, register the user
        self.client.post(url_for('main.register'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'confirm_password': 'password'
        })

        # Then, log in with the registered user
        self.client.post(url_for('main.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

        # Simulate a logout (assuming you have a logout route, if not, create one)
        response = self.client.get(url_for('main.index'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You were logged out', response.data)

if __name__ == '__main__':
    unittest.main()
