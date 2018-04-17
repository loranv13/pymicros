from flask import Flask, request
from flask_restful import Resource, Api
from threading import current_thread
import sys
import pymicros.mservice.service


class interface(Resource):
    
    def get(self):
        
        pymicros.mservice.service.qrcv.put(message)    
        

class COMWs():

    def __init__(self, ip, port):
        
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.port = port
        self.ip = ip

        self.api.add_resource(interface,'/')

    def listen(self):
        
        self.app.run(host=self.ip,port=self.port,debug=True)
