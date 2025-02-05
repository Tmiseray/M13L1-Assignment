import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from services.customerService import find_customers, customers_loyalty_value


class CustomerServiceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('TestingConfig')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch('services.customerService.db.session.execute')
    def test_find_customers(self, mock_customers):
        # Arrange
        faker = Faker()
        expected_customers = [faker.word(), faker.word()]

        # Mock query chain
        mock_customers.return_value.scalars.return_value.all.return_value = expected_customers

        # Act
        result = find_customers()

        # Assert
        self.assertEqual(result, expected_customers)

    @patch('services.customerService.db.session.execute')
    def test_customers_loyalty_value(self, mock_execute):
        # Arrange
        faker = Faker()
        expected_loyalty_customers = [
            {'customerName': faker.name(), 'lifetimeLoyaltyValue': round(faker.random_number(digits=3), 2)},
            {'customerName': faker.name(), 'lifetimeLoyaltyValue': round(faker.random_number(digits=3), 2)}
        ]

        # Mock query chain
        mock_execute.return_value.all.return_value = expected_loyalty_customers

        # Act
        result = customers_loyalty_value()

        # Assert
        self.assertEqual(result, expected_loyalty_customers)


if __name__ == '__main__':
    unittest.main()