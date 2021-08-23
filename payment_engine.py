import sys

from resource_reader import ResourceLoader
from client_factory import ClientFactory

__client_factory = ClientFactory()


def main(argv):
    file_reader = ResourceLoader()
    data_frame = file_reader.read_file(argv)
    if data_frame is not None:
        for index, row in data_frame.iterrows():
            client_id = row['client']
            if client_id is not None and isinstance(client_id, int) and 0 < client_id < pow(2, 16):
                client = __client_factory.get_or_create_client(client_id)
                client.process_transaction(row)
        print(__client_factory.client_records_str())


# used for testing
def write_clients_to_file():
    file = open('clients_accounts.csv', 'w+')
    file.write(__client_factory.client_records_str())
    file.close()


if __name__ == '__main__':
    try:
        total_args = len(sys.argv)
        if total_args == 2:
            main(sys.argv[1])
        else:
            print("error - incorrect num of vars. ex: python payment_engine.py file_to_read.csv")
    except Exception as error:
        print('error:', error)
