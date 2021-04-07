# These imports are only used to facilitate annotation type: type, intelligent prompt function!
from requests import Timeout
from web3 import Web3
from web3.eth import Eth, Contract
from flask_web3 import FlaskWeb3
import json
import etherscan
from web3 import Web3
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def get_balance(wallet):
    w3 = Web3(Web3.HTTPProvider(getenv('INFURA')))
    wei = w3.eth.get_balance(wallet)
    return w3.fromWei(wei, 'ether')

