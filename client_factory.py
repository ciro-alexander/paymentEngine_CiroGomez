from client import Client


class ClientFactory:

    __clients = {}
    __u16_max = pow(2, 16)

    def get_or_create_client(self, client_id):
        if client_id is None or client_id < 0 or client_id > self.__u16_max:
            # invalid client id type
            return

        if isinstance(client_id, int):
            if client_id in self.__clients:
                return self.__clients.get(client_id)
            else:
                # client not found - creating new client
                client = Client(client_id)
                self.__clients[client_id] = client
                return client

    def client_records_str(self):
        str_out = "client,available,held,total,locked\n"
        size = len(self.__clients)
        for client in self.__clients.values():
            str_out += str(client.to_string())
            if size > 1:
                str_out += "\n"
            size -= 1
        return str_out
