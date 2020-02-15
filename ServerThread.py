import datetime
import os
import threading
import traceback
from socket import socket
from urllib import parse

from consts import NOT_FOUND_FILE, STATUS_NOT_FOUND, STATUS_OK, HTTP_STATUS_MESSAGE
from env import DOCUMENT_ROOT


class ServerThread(threading.Thread):
    sequence = 0

    def __init__(self, client_socket: socket, *args, **kwargs):
        self.socket = client_socket
        super().__init__(*args, **kwargs)
        self.instance_id = ServerThread.sequence
        ServerThread.sequence += 1

    def run(self) -> None:
        print(f"run thread({self.instance_id})")
        try:
            recv_msg = self.socket.recv(4096)
            with open("./server_recv", "bw") as f:
                f.write(recv_msg)
            decoded_recv_msg = recv_msg.decode()
            print(f"server({self.instance_id}): received client's messages.\n")
            print("-----------------------------------\n")
            print(decoded_recv_msg)
            print("-----------------------------------\n")

            request_path = parse.unquote(decoded_recv_msg.splitlines()[0].split(" ")[1])
            path = os.path.abspath(DOCUMENT_ROOT + request_path)

            # ディレクトリトラバーサル対策
            if not path.startswith(DOCUMENT_ROOT):
                print(
                    f"Suspicious! A request could be intended to traverse directory. path: {path}"
                )
                with open(DOCUMENT_ROOT + NOT_FOUND_FILE, "br") as f:
                    content = f.read()
                status = STATUS_NOT_FOUND
                mime_type = "text/html"
            else:
                # pathの正規化（文末のスラッシュを削除し、pathが空の場合はindex.htmlを表示
                while path.endswith("/"):
                    path = path[:-1]
                if path == "":
                    path = "/index.html"
                ext = path.split(".")[-1]
                mime_type = self.get_mime_types(ext)

                try:
                    with open(path, "br") as f:
                        content = f.read()
                    status = STATUS_OK
                except (FileNotFoundError, IsADirectoryError) as e:
                    print(f"file detecting error. path:{path}, error:{e}")
                    with open(DOCUMENT_ROOT + NOT_FOUND_FILE, "br") as f:
                        content = f.read()
                    status = STATUS_NOT_FOUND

            header = self.get_header(status=status, mime_type=mime_type)

            send_msg = header.encode("utf-8") + content
            self.socket.send(send_msg)
            print(f"server({self.instance_id}): send server's messages.")
            print("-----------------------------------\n")
            print(header)
            print("-----------------------------------\n")
        except Exception as e:
            print(f"fuck error! error: {e}")
            traceback.print_exc()
        finally:
            self.socket.close()
            print(f"server({self.instance_id}): closed.")

    def get_header(self, status: int, mime_type: str) -> str:
        header = self.get_header_status(status) + "\n"
        header += "Date: " + datetime.datetime.utcnow().strftime(
            "%a, %d %b %Y %H:%M:%S GMT\n"
        )
        header += "Server: oreore-web-server v0.1\n"
        header += "Connection: Close\n"
        header += f"ContentType: {mime_type}\n"
        header += "\n"
        return header

    @staticmethod
    def get_header_status(status: int) -> str:
        return f"HTTP/1.1 {str(status)} {HTTP_STATUS_MESSAGE[status]}"

    @staticmethod
    def get_mime_types(ext: str = "") -> str:
        return {
            "txt": "text/plain",
            "html": "text/html",
            "css": "text/css",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
        }.get(ext.lower(), "application/octet-stream")
