import socket
import datetime

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8001))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    try:
        recv_msg = client_socket.recv(4096)
        with open("./server_recv", "w") as f:
            f.write(recv_msg.decode("utf-8"))

        with open("./server_send") as f:
            send_msg = f.read()
        client_socket.send(send_msg.encode("utf-8"))
    finally:
        client_socket.close()
        server_socket.close()


if __name__ == '__main__':
    main()
