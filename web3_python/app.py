import pandas as pd
import json
import solc
from flask import Flask, render_template, request, Response, request, jsonify
from flask_web3 import current_web3, FlaskWeb3
from web3 import Web3
from os import getenv
from dotenv import load_dotenv
from .models import get_balance


load_dotenv()

# web3.py instance
w3 = Web3(Web3.HTTPProvider(getenv('INFURA')))

 
def create_app():
    app = Flask(__name__)

    @app.route("/", methods = ["GET", "POST"]) 
    def about():
        """ 
        Our about us page.
        """
        
        if request.method == "GET":
            return render_template('base.html')
            
        if request.method == "POST":
            input = request.form.get("input_song")
            message = get_balance(str(input))
            return render_template('main.html', recommended_song=message)
        
    return app
