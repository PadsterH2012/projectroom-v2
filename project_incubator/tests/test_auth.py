import unittest
from app import create_app, db
from app.models import User
from flask import url_for

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_login_logout(self):
        with self.app.app_context():
            # Register
            response = self.client.post(url_for('main.register'), data={
                'username': 'testuser',
                'email': 'test@test.com',
                'password': 'password',
                'confirm_password': 'password'
            })
            self.assertIn(b'Your account has been created!', response.data)

            # Login
            response = self.client.post(url_for('main.login'), data={
                'email': 'test@test.com',
                'password': 'password'
            }, follow_redirects=True)
            self.assertIn(b'Welcome to the Project Incubator!', response.data)

            # Logout
            response = self.client.get(url_for('main.logout'), follow_redirects=True)
            self.assertIn(b'Welcome to the Project Incubator!', response.data)

if __name__ == '__main__':
    unittest.main()
