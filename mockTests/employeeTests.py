import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from services.employeeService import find_employees, employees_total_productions


class EmployeeServiceTests(unittest.TestCase):

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

    @patch('services.employeeService.db.session.execute')
    def test_find_employees(self, mock_employees):
        # Arrange
        faker = Faker()
        expected_employees = [faker.word(), faker.word()]

        # Mock query chain
        mock_employees.return_value.scalars.return_value.all.return_value = expected_employees

        # Act
        result = find_employees()

        # Assert
        self.assertEqual(result, expected_employees)

    @patch('services.employeeService.db.session.execute')
    def test_employees_total_productions(self, mock_productions):
        # Arrange
        faker = Faker()
        expected_productions = [
            {'employeeName': faker.name(), 'totalItemsProduced': faker.random_int(min=1, max=100)},
            {'employeeName': faker.name(), 'totalItemsProduced': faker.random_int(min=1, max=100)}
        ]

        # Mock query chain
        mock_productions.return_value.all.return_value = expected_productions

        # Act
        result = employees_total_productions()

        # Assert
        self.assertEqual(result, expected_productions)


if __name__ == '__main__':
    unittest.main()