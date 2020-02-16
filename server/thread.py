import io
import logging
import os
import re
import threading
from socket import socket
from typing import Dict, Tuple, List

from application.application import WSGIApplication
from consts import DEFAULT_DOCUMENT
from env import DEBUG


class ServerThread(threading.Thread):
    sequence: int = 0

    def __init__(self, client_socket: socket, *args, **kwargs):
        if DEBUG:
            logging.basicConfig(level=logging.DEBUG)

        self.socket: socket = client_socket
        self.instance_id: int = ServerThread.sequence
        ServerThread.sequence += 1
        self.request: Dict = {
            "method": "",
            "path": "",
            "version": "",
            "headers": {},
            "content": b"",
        }
        self.response: Dict = {
            "status_code": 0,
            "status_message": "",
            "headers": {},
            "content": "",
        }

        super().__init__(*args, **kwargs)

    def run(self) -> None:
        print(f"run thread({self.instance_id})")
        try:
            recv_msg = self.receive_msg()
            self.request = self.parse_request(recv_msg)

            # Call WSGI Application
            env = self.get_wsgi_env()

            application = WSGIApplication()
            response_content_iterable = application(env, self.start_response)

            status_line = f"HTTP/1.1 {self.response['status_message']}"
            header_part = "\r\n".join(
                f"{header_name}: {header_value}"
                for header_name, header_value in self.response["headers"].items()
            )
            response_content = b"".join(response_content_iterable)

            send_msg = (
                status_line + "\r\n" + header_part + "\r\n\r\n"
            ).encode() + response_content

            self.socket.send(send_msg)
            logging.debug(
                f"server({self.instance_id}): send server's message.\n"
                "-------------(header only)----------------------\n"
                f"{status_line}\r\n"
                f"{header_part}\r\n\r\n"
                f"{response_content}"
                "-----------------------------------\n"
            )
        except Exception as e:
            logging.exception(f"server({self.instance_id}): fuck error! error: %s", e)
        finally:
            self.socket.close()
            logging.debug(f"server({self.instance_id}): closed.")

    def receive_msg(self) -> bytes:
        try:
            raw_msg = self.socket.recv(4096)
            with open("./server_recv", "bw") as f:
                f.write(raw_msg)
            logging.debug(
                f"server({self.instance_id}): received client's messages.\n"
                "-----------------------------------\n"
                f"{raw_msg.decode()}\n"
                "-----------------------------------\n"
            )
            return raw_msg
        except Exception as e:
            logging.exception(f"server({self.instance_id}): fuck error! error: %s", e)

    @staticmethod
    def parse_request(msg: bytes) -> Dict:
        """
        parse request message and return dict of
        {
            "method": http method
            "path": request path
            "protocol": request protocol
            "headers": dict of headers
            "content": request content
        }
        """
        raw_request_line, remain_part = msg.split(b"\r\n", 1)
        raw_header_part, content_part = remain_part.split(b"\r\n\r\n", 1)

        request_line = raw_request_line.decode()
        method, raw_path, protocol = request_line.split()
        if raw_path.find("?") != -1:
            path, query = raw_path.split("?", 1)
        else:
            path, query = raw_path, ""

        header_part = raw_header_part.decode()
        header_lines = header_part.splitlines()
        headers = {}
        for header_line in header_lines:
            key, value = re.split(r":\S*", header_line, 1)
            headers[key] = value

        return {
            "method": method,
            "path": path,
            "query": query,
            "protocol": protocol,
            "headers": headers,
            "content": content_part,
        }

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        normalize path
        """
        # delete trailing slash
        path = re.sub(r"\*$", "", path)

        # make path absolute (deal with directory traversal)
        if not os.path.isabs(path):
            path = "/" + path
        path = os.path.abspath(path)

        logging.debug(f"path: {path}")

        # set default if path is empty
        if path == "/":
            path = DEFAULT_DOCUMENT

        return path

    def get_wsgi_env(self) -> Dict:
        path = self.normalize_path(self.request["path"])

        http_host = self.request["headers"].get("Host")
        if http_host.find(":") != -1:
            server_name, server_port = http_host.split(":", 1)
        else:
            server_name, server_port = http_host, ""

        env = {
            "REQUEST_METHOD": self.request["method"],
            "SCRIPT_NAME": "",  # TODO: should be implemented ?
            "PATH_INFO": path,
            "QUERY_STRING": self.request["query"],
            "SERVER_NAME": server_name,
            "SERVER_PORT": server_port,
            "SERVER_PROTOCOL": self.request["protocol"],
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",  # NOTE: http only now
            "wsgi.input": io.BytesIO(self.request["content"]),
            "wsgi.errors": io.StringIO(),
            "wsgi.multithread": True,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
        }

        content_type = self.request["headers"].get("Content-Type")
        if content_type:
            env["CONTENT_TYPE"] = content_type

        content_length = self.request["headers"].get("Content-Length")
        if content_length:
            env["CONTENT_LENGTH"] = content_length

        for header_name, header_value in self.request["headers"].items():
            key = "HTTP_" + header_name.replace("-", "_").upper()
            env[key] = header_value

        return env

    def start_response(
        self, status_message: str, headers: List[Tuple[str, str]]
    ) -> None:
        self.response["status_code"] = int(status_message.split(maxsplit=1)[0])
        self.response["status_message"] = status_message
        self.response["headers"] = {header[0]: header[1] for header in headers}
