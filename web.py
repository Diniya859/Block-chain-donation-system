from web3 import Web3
from django.conf import settings

# Connect to Web3 provider
web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))

# Validate and load contract
if not web3.isAddress(settings.CONTRACT_ADDRESS):
    raise ValueError(f"Invalid Ethereum address: {settings.CONTRACT_ADDRESS}")

contract = web3.eth.contract(
    address=settings.CONTRACT_ADDRESS,
    abi=settings.CONTRACT_ABI
)
