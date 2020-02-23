import sys

from server import main

if __name__ == "__main__":
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
