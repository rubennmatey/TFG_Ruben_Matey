from datetime import datetime
from web3 import Web3

from app.config import BLOCKCHAIN_ACCOUNT, BLOCKCHAIN_PRIVATE_KEY, CHAIN_ID
from app.blockchain.web3_client import get_contract

# Send a credential with all its data to the blockchain
def register_credential_on_blockchain(uid, alias, role, active):
    

    web3, contract = get_contract()

    timestamp = datetime.utcnow().isoformat()
    account = Web3.to_checksum_address(BLOCKCHAIN_ACCOUNT)
    nonce = web3.eth.get_transaction_count(account)

    transaction = contract.functions.registerCredential(
        uid,
        alias,
        role,
        bool(active),
        timestamp
    ).build_transaction({
        "chainId": CHAIN_ID,
        "from": account,
        "nonce": nonce,
        "gas": 400000,
        "gasPrice": web3.to_wei("2", "gwei"),
    })

    signed_tx = web3.eth.account.sign_transaction(
        transaction,
        private_key=BLOCKCHAIN_PRIVATE_KEY
    )

    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return {
        "tx_hash": tx_hash.hex(),
        "block": receipt.blockNumber,
        "uid": uid,
        "alias": alias,
        "role": role,
        "active": bool(active),
        "timestamp": timestamp,
    }

# Update the status of a credential already registered in blockchain
def update_credential_status_on_blockchain(uid, active):
   

    web3, contract = get_contract()

    timestamp = datetime.utcnow().isoformat()
    account = Web3.to_checksum_address(BLOCKCHAIN_ACCOUNT)
    nonce = web3.eth.get_transaction_count(account)

    transaction = contract.functions.updateCredentialStatus(
        uid,
        bool(active),
        timestamp
    ).build_transaction({
        "chainId": CHAIN_ID,
        "from": account,
        "nonce": nonce,
        "gas": 400000,
        "gasPrice": web3.to_wei("2", "gwei"),
    })

    signed_tx = web3.eth.account.sign_transaction(
        transaction,
        private_key=BLOCKCHAIN_PRIVATE_KEY
    )

    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return {
        "tx_hash": tx_hash.hex(),
        "block": receipt.blockNumber,
        "uid": uid,
        "active": bool(active),
        "timestamp": timestamp,
    }

# Get all credentials from the blockchain
def get_all_credentials_from_blockchain():
   
    _, contract = get_contract()

    count = contract.functions.getCredentialsCount().call()
    credentials = []

    for index in range(count):
        credential = contract.functions.getCredential(index).call()

        credentials.append({
            "id": credential[0],
            "uid": credential[1],
            "alias": credential[2],
            "role": credential[3],
            "active": bool(credential[4]),
            "timestamp": credential[5],
        })

    return credentials