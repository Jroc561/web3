import pandas as pd
from flask import Flask, render_template, request, Response, request, jsonify
import json
from flask_web3 import current_web3, FlaskWeb3
from web3 import Web3


# Declare a custom Web3 class
class CustomWeb3(Web3):
     def customBlockNumber():
         return self.eth.blockNumber

# Associate a custom FlaskWeb3 extension
class CustomFlaskWeb3(FlaskWeb3):
     web3_class = CustomWeb3



def create_app():
    app = Flask(__name__)
    app.config.update({'ETHEREUM_PROVIDER': 'http', 'ETHEREUM_ENDPOINT_URI': 'http://localhost:8545'})

    # Declare customized web3 extension
    web3 = CustomFlaskWeb3(app=app)
    isinstance(web3, CustomWeb3)

    @app.route("/") 
    def about():
        """ 
        Our about us page.
        """
        return render_template('base.html')
    
    # Declare route
    @app.route('/customBlockNumber')
    def last_odd_block_number():
        return jsonify({'data': current_web3.customBlockNumber()})