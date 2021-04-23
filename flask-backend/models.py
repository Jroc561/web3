import pandas as pd
from web3 import Web3
import etherscan
from datetime import datetime
import schedule
import time
from os import getenv
from dotenv import load_dotenv

load_dotenv()

es = etherscan.Client(api_key=getenv('ETHERSCAN'))
w3 = Web3(Web3.HTTPProvider(getenv('INFURA')))

rarible_contract = '0xcd4EC7b66fbc029C116BA9Ffb3e59351c20B5B06'
rarible = pd.read_csv('../rarible.csv', index_col=0)

def mp_transactions(address):
    columns = ['timestamp', 'block_number', 'from', 'to', 'input', 'hash', 'value', 'gas', 
                'gas_price', 'gas_used', 'nonce', 'confirmations', 'is_error', 'tx_receipt_status', 
                'transaction_index', 'cumulative_gas_used', 'block_hash']

    transactions = []

    start_block = rarible['block_number'].iloc[-1]

    for l in es.get_transactions_by_address(address, start_block=start_block, limit=9999):
        time.sleep(.2)
        transactions.append(l)

    df = pd.DataFrame(transactions, columns=columns)
    df['timestamp'] = df['timestamp'].apply(datetime.fromtimestamp)
    df = df[df['value'] != 0]
    df = df[df['is_error'] != True]
    df['value'] = [w3.fromWei(x, 'ether') for x in df['value']]
    df = df.reset_index(drop=True)
    df.to_csv('rarible.csv', header=None, mode='a')
    return df

schedule.every(15).to(30).seconds.do(mp_transactions(rarible_contract))