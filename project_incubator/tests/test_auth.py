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

    def test_register_login_logout(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('main.register'), data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password',
                'password2': 'password'
            })
            self.assertEqual(response.status_code, 200)
