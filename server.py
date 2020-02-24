import logging
import sys

from env import DEBUG

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    from server import main

    if len(sys.argv) != 2:
        print(
            "please command bellow. You can use only 'serve' yet.\n"
            "'python server.py serve'"
        )
        exit()

    method = sys.argv[1]
    if method != "serve":
        print(
            "please command bellow. You can use only 'serve' yet.\n"
            "'python server.py serve'"
        )

    getattr(main.Main, method)()
