from app.constants import (ACCESS_GRANTED, ACCESS_DENIED, REASON_AUTHORIZED, REASON_NOT_FOUND, REASON_REVOKED)
from app.db.credentials_actions import get_credential_by_uid
from app.db.access_logs_actions import create_access_log

# Checks if a UID has access permission and logs the result
def check_access(uid):
    credential = get_credential_by_uid(uid)

    if credential is None:
        result = ACCESS_DENIED
        reason = REASON_NOT_FOUND
        create_access_log(uid, result, reason)
        return {"uid": uid, "result": result, "reason": reason}
    
    if credential["active"] == 0:
        result = ACCESS_DENIED
        reason = REASON_REVOKED
        create_access_log(uid, result, reason)
        return {"uid": uid, "result": result, "reason": reason, "alias": credential["alias"], "role": credential["role"]}
    else:
        result = ACCESS_GRANTED
        reason = REASON_AUTHORIZED
        create_access_log(uid, result, reason)
        return {"uid": uid, "result": result, "reason": reason, "alias": credential["alias"], "role": credential["role"]}