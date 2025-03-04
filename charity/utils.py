from web3 import Web3
from django.conf import settings

web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))
contract = web3.eth.contract(
    address=settings.CONTRACT_ADDRESS,
    abi=settings.CONTRACT_ABI,
)

def make_donation(sender_address, private_key, amount):
    transaction = contract.functions.donate().buildTransaction({
        'from': sender_address,
        'value': web3.toWei(amount, 'ether'),
        'gas': 2000000,
        'nonce': web3.eth.getTransactionCount(sender_address),
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(tx_hash)
