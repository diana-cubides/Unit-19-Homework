# Import dependencies
import os
import subprocess
import json
from coincurve.keys import PrivateKey
from dotenv import load_dotenv
# Import constants.py and necessary functions from bit and web3
from constants import *
from bit import wif_to_key
from web3 import Web3
from web3.middleware import geth_poa_middleware
# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545")) 
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

 
# Create a function called `derive_wallets`
def derive_wallets(coin=BTC, mnemonic=mnemonic, depth=3):
    command = f'php ./hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --cols=all --coin={coin} --numderive={depth} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return json.loads(output)
  

# Create a dictionary object called coins to store the output from `derive_wallets`.
print(derive_wallets(BTCTEST, mnemonic, depth=3))

coins = {BTCTEST: derive_wallets(BTC, mnemonic, depth=3)}
print(coins)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(bit.wallet.PrivateKey):
    return(PrivateKey)
    

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(account, recipient, amount):
    #gasEstimate
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(account, recipient, amount):
    tx = create_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()
