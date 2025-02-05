import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from services.orderService import find_orders, paginate_orders

class OrderServiceTests(unittest.TestCase):

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

    @patch('services.orderService.db.session.execute')
    def test_find_orders(self, mock_orders):
        # Arrange
        faker = Faker()
        expected_orders = [faker.word(), faker.word()]

        # Mock query chain
        mock_orders.return_value.scalars.return_value.all.return_value = expected_orders

        # Act
        result = find_orders()

        # Assert
        self.assertEqual(result, expected_orders)

    @patch('services.orderService.db.session.query')
    def test_paginate_orders(self, mock_query):
        # Arrange
        faker = Faker()
        page = faker.random_int(1, 10)
        per_page = faker.random_int(5, 50, step=5)
        expected_orders = [faker.word() for _ in range(per_page)]

        # Mock query chain
        mock_query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = expected_orders
        mock_query.return_value.count.return_value = len(expected_orders)

        # Act
        result = paginate_orders(page, per_page)

        # Assert
        self.assertEqual(result['orders'], expected_orders)
        self.assertEqual(result['totalItems'], len(expected_orders))


if __name__ == '__main__':
    unittest.main()