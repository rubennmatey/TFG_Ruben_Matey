from app.db.credentials_repository import list_credentials
from app.blockchain.web3_client import get_contract
from app.blockchain.hashing import hash_uid


def get_all_credential_events_from_blockchain():
    _, contract = get_contract()

    count = contract.functions.getCredentialEventsCount().call()
    events = []

    for index in range(count):
        event = contract.functions.getCredentialEvent(index).call()

        events.append({
            "id": event[0],
            "uid_hash": event[1],
            "action_type": event[2],
            "role": event[3],
            "active": event[4],
            "timestamp": event[5],
        })

    return events


def verify_credentials_against_blockchain():
    credentials = list_credentials()
    blockchain_events = get_all_credential_events_from_blockchain()

    results = []

    for credential in credentials:
        uid = credential["uid"]
        uid_hash = hash_uid(uid)

        credential_events = [
            event for event in blockchain_events
            if event["uid_hash"] == uid_hash
        ]

        if not credential_events:
            results.append({
                "uid": uid,
                "status": "INVALID",
                "reason": "NO_BLOCKCHAIN_REGISTER_EVENT",
                "local_role": credential["role"],
                "local_active": bool(credential["active"]),
                "blockchain_role": None,
                "blockchain_active": None,
            })
            continue

        valid_register_events = [
            event for event in credential_events
            if event["action_type"] in ("INITIAL_REGISTER", "REGISTER")
        ]

        if not valid_register_events:
            results.append({
                "uid": uid,
                "status": "INVALID",
                "reason": "NO_VALID_REGISTER_EVENT",
                "local_role": credential["role"],
                "local_active": bool(credential["active"]),
                "blockchain_role": None,
                "blockchain_active": None,
            })
            continue

        last_event = credential_events[-1]

        local_role = credential["role"]
        local_active = bool(credential["active"])

        blockchain_role = last_event["role"]
        blockchain_active = bool(last_event["active"])

        if local_role != blockchain_role or local_active != blockchain_active:
            results.append({
                "uid": uid,
                "status": "INVALID",
                "reason": "LOCAL_STATE_DOES_NOT_MATCH_BLOCKCHAIN",
                "local_role": local_role,
                "local_active": local_active,
                "blockchain_role": blockchain_role,
                "blockchain_active": blockchain_active,
                "last_blockchain_action": last_event["action_type"],
                "last_blockchain_timestamp": last_event["timestamp"],
            })
        else:
            results.append({
                "uid": uid,
                "status": "VALID",
                "reason": "LOCAL_STATE_MATCHES_BLOCKCHAIN",
                "local_role": local_role,
                "local_active": local_active,
                "blockchain_role": blockchain_role,
                "blockchain_active": blockchain_active,
                "last_blockchain_action": last_event["action_type"],
                "last_blockchain_timestamp": last_event["timestamp"],
            })

    return results