import socket

from ServerThread import ServerThread


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8001))
    print("server: a socket was bound.")
    server_socket.listen(5)
    print(f"server: listening.")
    while True:
        client_socket, address = server_socket.accept()
        print("server: accepted.")
        thread = ServerThread(client_socket)
        thread.start()


if __name__ == "__main__":
    main()
