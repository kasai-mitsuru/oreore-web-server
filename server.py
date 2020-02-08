import datetime
import socket
import traceback

from env import DOCUMENT_ROOT


def get_header(ext: str) -> str:
    header = "HTTP/1.1 200 OK\n"
    header += "Date: " + datetime.datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT\n"
    )
    header += "Server: oreore-web-server v0.1\n"
    header += "Connection: Close\n"
    header += f"ContentType: {get_mime_types(ext)}\n"
    header += "\n"
    return header


def get_mime_types(ext: str) -> str:
    return {
        "txt": "text/plain",
        "html": "text/html",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
    }.get(ext.lower(), "application/octet-stream")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8001))
    print("server: a socket was bound.")
    server_socket.listen(1)
    print(f"server: listening.")
    while True:
        client_socket, address = server_socket.accept()
        print("server: accepted.")
        try:
            recv_msg = client_socket.recv(4096)
            with open("./server_recv", "bw") as f:
                f.write(recv_msg)
            decoded_recv_msg = recv_msg.decode()
            print("server: received client's messages.\n")
            print("-----------------------------------\n")
            print(decoded_recv_msg)
            print("-----------------------------------\n")

            path = decoded_recv_msg.splitlines()[0].split(" ")[1]
            ext = path.split(".")[-1]

            header = get_header(ext)
            with open(DOCUMENT_ROOT + path, 'br') as f:
                content = f.read()
            send_msg = header.encode("utf-8") + content
            client_socket.send(send_msg)
            print("server: send server's messages.")
            print("-----------------------------------\n")
            print(send_msg.decode())
            print("-----------------------------------\n")
        except Exception as e:
            print(f"fuck error! error: {e}")
            traceback.print_exc()
        finally:
            client_socket.close()
            print("server: closed.")


if __name__ == "__main__":
    main()
