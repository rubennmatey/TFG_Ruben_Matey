from web3 import Web3
from app.config import BLOCKCHAIN_ACCOUNT, BLOCKCHAIN_PRIVATE_KEY, CHAIN_ID
from app.blockchain.web3_client import get_web3, get_contract


def send_admin_action_to_blockchain(action_type, target_uid, timestamp):
    web3, contract = get_contract()

    account = Web3.to_checksum_address(BLOCKCHAIN_ACCOUNT)
    nonce = web3.eth.get_transaction_count(account)

    transaction = contract.functions.registerAdminAction(
        action_type,
        target_uid,
        timestamp
    ).build_transaction({
        "chainId": CHAIN_ID,
        "from": account,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": web3.to_wei("2", "gwei"),
    })

    signed_tx = web3.eth.account.sign_transaction(
        transaction,
        private_key=BLOCKCHAIN_PRIVATE_KEY
    )

    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex(), receipt