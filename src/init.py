import time

from Server.server import HTTPServer

if __name__ == "__main__":
    time.sleep(10)
    server = HTTPServer()
    server.init_server()
