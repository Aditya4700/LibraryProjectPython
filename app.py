from flask import Flask,request, jsonify
from sqlobject import *
from datetime import datetime
import os 
from routes import route

app = Flask(__name__)
app.register_blueprint(route)

if __name__=="__main__":
    app.run()
    