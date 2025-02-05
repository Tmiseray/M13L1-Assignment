import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from services.productService import  find_products, paginate_products, top_selling_products


class ProductServiceTests(unittest.TestCase):

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

    @patch('services.productService.db.session.execute')
    def test_find_products(self, mock_products):
        # Arrange
        faker = Faker()
        expected_products = [faker.word(), faker.word()]

        # Mock query chain
        mock_products.return_value.scalars.return_value.all.return_value = expected_products

        # Act
        result = find_products()

        # Assert
        self.assertEqual(result, expected_products)

    @patch('services.productService.db.session.query')
    def test_paginate_products(self, mock_query):
        # Arrange
        faker = Faker()
        page = faker.random_int(1, 10)
        per_page = faker.random_int(5, 50, step=5)
        expected_products = [faker.word() for _ in range(per_page)]

        # Mock query chain
        mock_query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = expected_products
        mock_query.return_value.count.return_value = len(expected_products)

        # Act
        result = paginate_products(page, per_page)

        # Assert
        self.assertEqual(result['products'], expected_products)
        self.assertEqual(result['totalItems'], len(expected_products))

    @patch('services.productService.db.session.execute')
    def test_top_selling_products(self, mock_execute):
        # Arrange
        faker = Faker()
        expected_products = [faker.word() for _ in range(5)]
        mock_execute.return_value.all.return_value = expected_products

        # Act
        result = top_selling_products()

        # Assert
        self.assertEqual(result, expected_products)

if __name__ == '__main__':
    unittest.main()