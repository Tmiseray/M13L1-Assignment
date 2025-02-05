import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from services.productionService import find_productions, production_efficiency


class ProductionServiceTests(unittest.TestCase):

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

    @patch('services.productionService.db.session.execute')
    def test_find_productions(self, mock_productions):
        # Arrange
        faker = Faker()
        expected_productions = [faker.word(), faker.word()]

        # Mock query chain
        mock_productions.return_value.scalars.return_value.all.return_value = expected_productions

        # Act
        result = find_productions()

        # Assert
        self.assertEqual(result, expected_productions)

    @patch('services.productionService.db.session.execute')
    def test_production_efficiency(self, mock_efficiency):
        # Arrange
        faker = Faker()
        date = faker.date()
        expected_efficiency = [
            {'productName': faker.word(), 'quantityProducedOnDate': faker.random_int(min=1, max=100), 'productionDate': date},
            {'productName': faker.word(), 'quantityProducedOnDate': faker.random_int(min=1, max=100), 'productionDate': date}
        ]

        # Mock query chain
        mock_efficiency.return_value.all.return_value = expected_efficiency

        # Act
        result = production_efficiency(date)

        # Assert
        self.assertEqual(result, expected_efficiency)


if __name__ == '__main__':
    unittest.main()