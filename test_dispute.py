import unittest
import payment_engine


class TestDispute(unittest.TestCase):

    def test_dispute(self):
        expected = "client,available,held,total,locked\n1,79.1235,10.5,89.6235,false"
        payment_engine.main('test_dispute.csv')
        payment_engine.write_clients_to_file()
        with open('clients_accounts.csv', 'r') as file:
            data = file.read()
            self.assertEqual(data, expected)