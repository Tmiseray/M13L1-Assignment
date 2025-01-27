import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import bcrypt
from services.userService import login


class TestUserEndpoints(unittest.TestCase):

    @patch('services.userService.db.session.execute')
    def test_login(self, mock_user):
        faker = Faker()
        mock_account = MagicMock()
        mock_account.id = 1
        mock_account.role = [MagicMock(role='admin')]
        password = faker.password()
        mock_account.username = faker.user_name()
        mock_account.password = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            )
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
        mock_account.username = faker.user_name()
        mock_account.password = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            )
        mock_user.query.filter.return_value.scalar_one_or_none.return_value = mock_account

        response = login(mock_account.username, faker.password())

        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
