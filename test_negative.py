import unittest
import payment_engine


class TestNegative(unittest.TestCase):

    def test_resolve(self):
        expected = "client,available,held,total,locked\n1,89.6235,0.0,89.6235,false\n2,5000.0,0.0,5000.0,false"
        payment_engine.main('test_negative.csv')
        payment_engine.write_clients_to_file()
        with open('clients_accounts.csv', 'r') as file:
            data = file.read()
            self.assertEqual(data, expected)