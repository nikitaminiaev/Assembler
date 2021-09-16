def start():
    import wifi_mod
    wifi_mod.do_connect()
    from client_socket.client_for_esp import Client
    client = Client()
    client.set_up()


if __name__ == '__main__':
    start()
