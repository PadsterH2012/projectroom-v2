import unittest
from app import create_app, db
from app.models import Config
from flask import url_for

class ConfigTestCase(unittest.TestCase):
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

    def test_settings(self):
        with self.app.app_context():
            # Create a config entry
            response = self.client.post(url_for('main.settings'), data={
                'name': 'test_config',
                'value': 'test_value'
            }, follow_redirects=True)
            self.assertIn(b'Configuration saved!', response.data)

            # Check if the config entry was saved in the database
            config = Config.query.filter_by(name='test_config').first()
            self.assertIsNotNone(config)
            self.assertEqual(config.value, 'test_value')

if __name__ == '__main__':
    unittest.main()
