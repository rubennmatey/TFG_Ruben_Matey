from app.blockchain.web3_client import get_contract


# Retrieves a log batch from the blockchain by its index
def get_log_batch_from_blockchain(batch_index):
    _, contract = get_contract()

    result = contract.functions.getLogBatch(batch_index).call()

    return {
        "id": result[0],
        "batch_hash": result[1],
        "timestamp": result[2],
    }