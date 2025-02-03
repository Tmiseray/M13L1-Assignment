import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import bcrypt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.userService import login


class TestUserEndpoints(unittest.TestCase):

    @patch('services.userService.db.session.execute')
    def test_login(self, mock_user):
        faker = Faker()
        mock_account = MagicMock()
        mock_account.id = 1
        mock_account.role = 'admin'
        password = faker.password()
        hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            )
        mock_account.username = faker.user_name()
        mock_account.password = hashed_password
        mock_user.return_value.scalar_one_or_none.return_value = mock_account

        response = login(mock_account.username, password)

        self.assertEqual(response['status'], 'success')

    
    @patch('services.userService.db.session.execute')
    def test_fail_login(self, mock_user):
        faker = Faker()
        mock_account = MagicMock()
        mock_account.id = 1
        mock_account.role = [MagicMock(role='admin')]
        password = faker.password()
        hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            )
        mock_account.username = faker.user_name()
        mock_account.password = hashed_password
        mock_user.return_value.scalar_one_or_none.return_value = mock_account

        incorrect_password = faker.password()
        # incorrect_hashed_password = bcrypt.hashpw(
        #         incorrect_password.encode('utf-8'), 
        #         bcrypt.gensalt()
        #     )

        response = login(mock_account.username, incorrect_password)

        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
