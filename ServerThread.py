import datetime
import logging
import os
import re
import textwrap
import threading
import traceback
from socket import socket
from typing import List, Tuple, NoReturn, Dict
from urllib import parse

from consts import (
    NOT_FOUND_DOCUMENT,
    STATUS_NOT_FOUND,
    STATUS_OK,
    HTTP_STATUS_MESSAGE,
    DEFAULT_DOCUMENT,
)
from env import DOCUMENT_ROOT, DEBUG


class ServerThread(threading.Thread):
    sequence: int = 0

    def __init__(self, client_socket: socket, *args, **kwargs):
        if DEBUG:
            logging.basicConfig(level=logging.DEBUG)

        self.socket: socket = client_socket
        self.instance_id: int = ServerThread.sequence
        ServerThread.sequence += 1
        self.request: Dict = {}

        super().__init__(*args, **kwargs)

    def run(self) -> None:
        print(f"run thread({self.instance_id})")
        try:
            recv_msg = self.receive_msg()
            self.request = self.parse_request(recv_msg)
            path = self.normalize_path(self.request["path"])

            # Application
            path = self.get_abs_path(path)

            # ディレクトリトラバーサル対策
            if not path.startswith(DOCUMENT_ROOT):
                logging.warning(
                    f"Suspicious! A request could be intended to traverse directory. path: {abs_path}"
                )
                with open(DOCUMENT_ROOT + NOT_FOUND_DOCUMENT, "br") as f:
                    content = f.read()
                status = STATUS_NOT_FOUND
                mime_type = "text/html"
            else:
                ext = path.split(".")[-1]
                mime_type = self.get_mime_types(ext)

                try:
                    with open(path, "br") as f:
                        content = f.read()
                    status = STATUS_OK
                except (FileNotFoundError, IsADirectoryError) as e:
                    logging.info(f"file detecting error. path:{path}, error:{e}")
                    with open(DOCUMENT_ROOT + NOT_FOUND_DOCUMENT, "br") as f:
                        content = f.read()
                    status = STATUS_NOT_FOUND

            header = self.get_header(status=status, mime_type=mime_type)

            send_msg = header.encode("utf-8") + content
            self.socket.send(send_msg)
            logging.debug(
                f"server({self.instance_id}): send server's messages.\n"
                "-----------------------------------\n"
                f"{header}\n"
                "-----------------------------------\n"
            )
        except Exception as e:
            logging.exception(f"server({self.instance_id}): fuck error! error: %s", e)
        finally:
            self.socket.close()
            logging.debug(f"server({self.instance_id}): closed.")

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
        return f"HTTP/1.1 {HTTP_STATUS_MESSAGE[status]}"

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

    def receive_msg(self) -> str:
        try:
            recv_msg_raw = self.socket.recv(4096)
            with open("./server_recv", "bw") as f:
                f.write(recv_msg_raw)
            recv_msg_decoded = recv_msg_raw.decode()
            logging.debug(
                f"server({self.instance_id}): received client's messages.\n"
                "-----------------------------------\n"
                f"{recv_msg_decoded}\n"
                "-----------------------------------\n"
            )
            return recv_msg_decoded
        except Exception as e:
            self.log_error(e)

    def log_error(self, e: Exception) -> NoReturn:
        logging.error(f"server({self.instance_id}): Exception! message: %s", e)

    @staticmethod
    def parse_request(msg: str) -> Dict:
        """
        parse request message and return dict of
        {
            "method": http method
            "path": request path
            "version": http version
            "headers": dict of headers
            "content": request content
        }
        """
        request_line, remain_lines = msg.split("\r\n", 1)
        header_part, content_part = remain_lines.split("\r\n\r\n", 1)

        method, path, version = request_line.split()

        header_lines = header_part.splitlines()
        headers = {}
        for header_line in header_lines:
            key, value = re.split(r":\S*", header_line, 1)
            headers[key] = value

        return {
            "method": method,
            "path": path,
            "version": version,
            "headers": headers,
            "content": content_part,
        }

    @staticmethod
    def get_abs_path(path: str) -> str:
        """
        absolute request path from raw request path
        """
        return os.path.abspath(DOCUMENT_ROOT + path)

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        normalize path
        """
        # delete trailing slash
        path = re.sub(r"\*$", "", path)

        # set default if path is empty
        if path == "":
            path = DEFAULT_DOCUMENT

        return path
