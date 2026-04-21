import json
from web3 import Web3
from app.config import BLOCKCHAIN_RPC_URL, CONTRACT_ADDRESS


def get_web3():
    web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_RPC_URL))
    return web3


def get_contract():
    web3 = get_web3()

    with open("app/blockchain/abi/access_registry_abi.json", "r", encoding="utf-8") as f:
        abi = json.load(f)

    contract = web3.eth.contract(
        address=Web3.to_checksum_address(CONTRACT_ADDRESS),
        abi=abi
    )
    return web3, contract