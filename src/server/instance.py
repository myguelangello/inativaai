import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

PORT_API = os.getenv("PORT_API")

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, supports_credentials=True)
    
    def run(self):
        return self.app.run(host='0.0.0.0', port=PORT_API, debug=True)
    
server = Server()
