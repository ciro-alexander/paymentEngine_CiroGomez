class Client:

    __id = 0
    __available = 0.0
    __held = 0.0
    __total = 0.0
    __is_locked = False
    __transaction_history = {}
    __u16_max = pow(2, 16)
    __u32_max = pow(2, 32)

    def __init__(self, client_id):
        assert client_id is not None, "client id is None"
        assert client_id < self.__u16_max
        self.__id = client_id

    def process_transaction(self, csv_row):
        if self.__is_locked:
            # client account is locked - unable to process transaction
            return

        try:
            tx_type = csv_row['type']
            if tx_type is not None and isinstance(tx_type, str) and self.__is_tx_valid(csv_row):
                tx_type = tx_type.lower()
                if tx_type == 'deposit':
                    self.__process_deposit(csv_row)
                elif tx_type == 'withdrawal':
                    self.__process_withdrawal(csv_row)
                elif tx_type == 'dispute':
                    self.__process_dispute(csv_row)
                elif tx_type == 'resolve':
                    self.__process_resolve(csv_row)
                elif tx_type == 'chargeback':
                    self.__process_chargeback(csv_row)
                else:
                    # unsupported transaction type - transaction failed
                    return
        except Exception as error:
            print('error:', error)

    def __process_deposit(self, csv_row):
        amount = csv_row['amount']
        if amount is not None and isinstance(amount, float):
            self.__available = self.__available + amount
            self.__update_total_amount()
            self.__store_transaction(csv_row)

    def __process_withdrawal(self, csv_row):
        amount = csv_row['amount']
        if amount is not None and isinstance(amount, float):
            if self.__available - amount < 0:
                # insufficient funds - transaction failed
                return
            else:
                self.__available = self.__available - amount
                self.__update_total_amount()
                self.__store_transaction(csv_row)

    def __process_dispute(self, csv_row):
        tx_id = csv_row['tx']
        if tx_id not in self.__transaction_history:
            # transaction id does not exist - ignore
            return
        else:
            transaction = self.__transaction_history.get(tx_id)
            if transaction is not None:
                amount_to_hold = transaction.get('amount')
                if amount_to_hold is not None and isinstance(amount_to_hold, float):
                    self.__held = self.__held + amount_to_hold
                    self.__available = self.__available - amount_to_hold

    def __process_resolve(self, csv_row):
        tx_id = csv_row['tx']
        if tx_id not in self.__transaction_history:
            # transaction id does not exist - ignore
            return
        else:
            transaction = self.__transaction_history.get(tx_id)
            if transaction is not None:
                amount_resolved = transaction.get('amount')
                if amount_resolved is not None and isinstance(amount_resolved, float):
                    self.__held = self.__held - amount_resolved
                    self.__available = self.__available + amount_resolved

    def __process_chargeback(self, csv_row):
        tx_id = csv_row['tx']
        if tx_id not in self.__transaction_history:
            # transaction with id %s does not exist - ignoring chargeback
            return
        else:
            transaction = self.__transaction_history.get(tx_id)
            if transaction is not None:
                chargeback_amount = transaction.get('amount')
                if chargeback_amount is not None and isinstance(chargeback_amount, float):
                    self.__held = self.__held - chargeback_amount
                    self.__total = self.__total - chargeback_amount
                    self.__is_locked = True

    def __update_total_amount(self):
        self.__total = self.__available + self.__held

    def __store_transaction(self, csv_row):
        tx_id = csv_row['tx']
        tx_type = csv_row['type']
        amount = csv_row['amount']
        if tx_id is not None and tx_type is not None and amount is not None:
            self.__transaction_history[tx_id] = {'tx_id': tx_id, 'tx_type': tx_type, 'amount': amount}
        else:
            # transaction fields are None - unable to store transaction
            return

    def __is_tx_valid(self, csv_row):
        tx_id = csv_row['tx']
        if tx_id is None or not isinstance(tx_id, int) or tx_id < 0 or tx_id > self.__u32_max:
            return False
        else:
            return True

    def to_string(self):
        return str('%s,%s,%s,%s,%s' % (self.__id, float("{:.4f}".format(self.__available)),
                                       float("{:.4f}".format(self.__held)), float("{:.4f}".format(self.__total)),
                                       str(self.__is_locked).lower()))
