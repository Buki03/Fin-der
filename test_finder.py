import unittest
from finder import users


class TestFinder(unittest.TestCase):

    # mock_input.side_effect = ['John', 'Doe', 
    #'johndoe@gmail.com', '1', '2', '3']
    def test_data(self):
        self.mock_input_values = [
            'John', 'Doe', 'johndoe@gmail.com', '1', '2', '3']
        self.assertEqual(users['first_name'][-1], 'John')
        self.assertEqual(users['last_name'][-1], 'Doe')
        self.assertEqual(users['email'][-1], 'johndoe@gmail.com')
        self.assertEqual(users['city'][-1], 'Ashburn')
        self.assertEqual(users['interest1'][-1], 'Sports')
        self.assertEqual(users['interest2'][-1], 'Food')
        self.assertEqual(users['interest3'][-1], 'Entertainment')
