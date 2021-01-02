from client_socket.client_for_esp import Client


# pin0  - D3
# pin2  - D4
# pin12 - D6
# pin13 - D7

class Mine:

    def __init__(self):
        self.client = Client()
        self.client.set_up()


if __name__ == '__main__':
    client = Client()
    client.set_up()
