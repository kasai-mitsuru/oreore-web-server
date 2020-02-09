import datetime
import socket
import traceback

from env import DOCUMENT_ROOT

STATUS_OK = 200
STATUS_NOT_FOUND = 404
STATUS_INTERNAL_SERVER_ERROR = 500

HTTP_STATUS_MESSAGE = {
    STATUS_OK: "OK.",
    STATUS_NOT_FOUND: "File Not Found.",
    STATUS_INTERNAL_SERVER_ERROR: "Internal Server Error."
}

NOT_FOUND_FILE = '/404.html'


def get_header(status: int, ext: str) -> str:
    header = get_header_status(status) + "\n"
    header += "Date: " + datetime.datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT\n"
    )
    header += "Server: oreore-web-server v0.1\n"
    header += "Connection: Close\n"
    header += f"ContentType: {get_mime_types(ext)}\n"
    header += "\n"
    return header

def get_header_status(status: int) -> str:
    return f"HTTP/1.1 {str(status)} {HTTP_STATUS_MESSAGE[status]}"

def get_mime_types(ext: str="") -> str:
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
            while path.endswith('/'):
                path = path[:-1]
            if path == "":
                path = "/index.html"
            ext = path.split(".")[-1]

            try:
                with open(DOCUMENT_ROOT + path, 'br') as f:
                    content = f.read()
                status = STATUS_OK
            except (FileNotFoundError, IsADirectoryError) as e:
                print(f'file detecting error. path:{path}, error:{e}')
                with open(DOCUMENT_ROOT + NOT_FOUND_FILE, 'br') as f:
                    content = f.read()
                status = STATUS_NOT_FOUND

            header = get_header(status=status, ext=ext)

            send_msg = header.encode("utf-8") + content
            client_socket.send(send_msg)
            print("server: send server's messages.")
            print("-----------------------------------\n")
            print(header)
            print("-----------------------------------\n")
        except Exception as e:
            print(f"fuck error! error: {e}")
            traceback.print_exc()
        finally:
            client_socket.close()
            print("server: closed.")


if __name__ == "__main__":
    main()
