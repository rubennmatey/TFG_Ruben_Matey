from app.db.credentials_actions import list_credentials
from app.blockchain.credential_chain_service import get_all_credentials_from_blockchain


# Compares local credentials against blockchain records and reports mismatches
def verify_credentials_against_blockchain():
    local_credentials = list_credentials()
    blockchain_credentials = get_all_credentials_from_blockchain()

    results = []

    for local_credential in local_credentials:
        uid = local_credential["uid"]

        matching_blockchain_credentials = [
            credential for credential in blockchain_credentials
            if credential["uid"] == uid
        ]

        if not matching_blockchain_credentials:
            results.append({
                "uid": uid,
                "status": "INVALID",
                "reason": "CREDENTIAL_NOT_REGISTERED_ON_CHAIN",
                "local_alias": local_credential["alias"],
                "local_role": local_credential["role"],
                "local_active": bool(local_credential["active"]),
                "blockchain_alias": None,
                "blockchain_role": None,
                "blockchain_active": None,
            })
            continue

        blockchain_credential = matching_blockchain_credentials[-1]

        local_alias = local_credential["alias"]
        local_role = local_credential["role"]
        local_active = bool(local_credential["active"])

        blockchain_alias = blockchain_credential["alias"]
        blockchain_role = blockchain_credential["role"]
        blockchain_active = bool(blockchain_credential["active"])

        if (
            local_alias != blockchain_alias
            or local_role != blockchain_role
            or local_active != blockchain_active
        ):
            results.append({
                "uid": uid,
                "status": "INVALID",
                "reason": "LOCAL_STATE_DOES_NOT_MATCH_BLOCKCHAIN",
                "local_alias": local_alias,
                "local_role": local_role,
                "local_active": local_active,
                "blockchain_alias": blockchain_alias,
                "blockchain_role": blockchain_role,
                "blockchain_active": blockchain_active,
                "blockchain_timestamp": blockchain_credential["timestamp"],
            })
        else:
            results.append({
                "uid": uid,
                "status": "VALID",
                "reason": "LOCAL_STATE_MATCHES_BLOCKCHAIN",
                "local_alias": local_alias,
                "local_role": local_role,
                "local_active": local_active,
                "blockchain_alias": blockchain_alias,
                "blockchain_role": blockchain_role,
                "blockchain_active": blockchain_active,
                "blockchain_timestamp": blockchain_credential["timestamp"],
            })

    return results