import unittest
import payment_engine


class TestChargeback(unittest.TestCase):

    def test_chargeback(self):
        expected = "client,available,held,total,locked\n1,79.1235,0.0,79.1235,true"
        payment_engine.main('test_chargeback.csv')
        payment_engine.write_clients_to_file()
        with open('clients_accounts.csv', 'r') as file:
            data = file.read()
            self.assertEqual(data, expected)