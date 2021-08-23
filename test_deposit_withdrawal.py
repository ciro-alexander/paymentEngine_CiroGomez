import unittest
import payment_engine


class TestDepositWithdrawal(unittest.TestCase):

    def test_valid_deposit_and_withdrawal(self):
        expected = "client,available,held,total,locked\n1,110.2468,0.0,110.2468,false\n2,10.0,0.0,10.0,false"
        payment_engine.main('test_deposit_withdrawal.csv')
        payment_engine.write_clients_to_file()
        with open('clients_accounts.csv', 'r') as file:
            data = file.read()
            self.assertEqual(data, expected)


if __name__ == '__main__':
    unittest.main()
