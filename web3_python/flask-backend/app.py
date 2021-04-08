import pandas as pd
from flask import Flask, render_template, request, Response, request, jsonify, redirect, url_for
from flask_restful import Api, Resource, reqparse
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
        request_method = request.method    
        if request.method == 'POST':
            address = request.form['address']
            return redirect(url_for('adr', address=address))
        return render_template('base.html', request_method=request_method)

    @app.route('/<string:address>')
    def adr(address):
        balance = get_balance(str(address))
        return render_template('main.html', balance=balance, address=address)

    @app.route('/connect')
    def connect():
        return render_template('test.html')
        
    return app
