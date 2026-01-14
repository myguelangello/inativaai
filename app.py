from src.server.instance import server
from src.controller import *
app = server.app

if __name__ == '__main__':
    server.run()