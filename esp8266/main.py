def start():
    from client_socket.client_for_esp import Client
    client = Client()
    client.set_up()


if __name__ == '__main__':
    start()
