import os
import random
from web3 import Web3
from dotenv import load_dotenv
import time
import signal
import sys

load_dotenv()
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
INFURA_URL = os.getenv('INFURA_URL')

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not web3.is_connected():
    raise Exception("Tidak dapat terhubung ke jaringan Ethereum")

account = web3.eth.account.from_key(PRIVATE_KEY)
sender_address = account.address

def get_dynamic_gas_price():
    return web3.eth.gas_price

def send_transaction(to_address, value_ether, gas_price=None):
    nonce = web3.eth.get_transaction_count(sender_address)
    
    if gas_price is None:
        gas_price = get_dynamic_gas_price()
    
    transaction = {
        'to': Web3.to_checksum_address(to_address),
        'value': web3.to_wei(value_ether, 'ether'),
        'gas': 21000,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': 2810  
    }
    
    signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash.hex()
    except ValueError as e:
        time.sleep(10)
        return None

def load_addresses(filename):
    with open(filename, 'r') as file:
        addresses = file.read().splitlines()
    return addresses

def signal_handler(sig, frame):
    print("\nEksekusi dihentikan.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    addresses = load_addresses('address.txt')
    value_ether = 0.0001
    
    for i in range(200):
        to_address = addresses[i % len(addresses)]
        gas_price = get_dynamic_gas_price() + web3.to_wei(10, 'gwei')
        tx_hash = send_transaction(to_address, value_ether, gas_price)
        if tx_hash:
            print(f"Transaksi {i+1} berhasil dikirim ke {to_address} dengan hash: {tx_hash}")
        else:
            print(f"Transaksi {i+1} gagal dikirim ke {to_address}")
