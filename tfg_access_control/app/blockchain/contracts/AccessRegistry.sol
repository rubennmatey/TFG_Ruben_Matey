// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessRegistry {
    struct AdminAction {
        uint256 id;
        string actionType;
        string targetUid;
        string timestamp;
    }

    struct LogBatch {
        uint256 id;
        string batchHash;
        string timestamp;
    }

    struct Credential {
        uint256 id;
        string uid;
        string aliasName;
        string role;
        bool active;
        string timestamp;
    }

    AdminAction[] private adminActions;
    LogBatch[] private logBatches;
    Credential[] private credentials;

    event AdminActionRegistered(
        uint256 indexed id,
        string actionType,
        string targetUid,
        string timestamp
    );

    event LogBatchRegistered(
        uint256 indexed id,
        string batchHash,
        string timestamp
    );

    event CredentialRegistered(
        uint256 indexed id,
        string uid,
        string aliasName,
        string role,
        bool active,
        string timestamp
    );

    event CredentialStatusUpdated(
        uint256 indexed id,
        string uid,
        bool active,
        string timestamp
    );

    function registerAdminAction(
        string memory actionType,
        string memory targetUid,
        string memory timestamp
    ) public {
        uint256 actionId = adminActions.length;

        adminActions.push(
            AdminAction({
                id: actionId,
                actionType: actionType,
                targetUid: targetUid,
                timestamp: timestamp
            })
        );

        emit AdminActionRegistered(
            actionId,
            actionType,
            targetUid,
            timestamp
        );
    }

    function getAdminAction(uint256 index)
        public
        view
        returns (
            uint256 id,
            string memory actionType,
            string memory targetUid,
            string memory timestamp
        )
    {
        require(index < adminActions.length, "Invalid index");

        AdminAction memory action = adminActions[index];

        return (
            action.id,
            action.actionType,
            action.targetUid,
            action.timestamp
        );
    }

    function getAdminActionsCount() public view returns (uint256) {
        return adminActions.length;
    }

    function registerLogBatch(
        string memory batchHash,
        string memory timestamp
    ) public {
        uint256 batchId = logBatches.length;

        logBatches.push(
            LogBatch({
                id: batchId,
                batchHash: batchHash,
                timestamp: timestamp
            })
        );

        emit LogBatchRegistered(
            batchId,
            batchHash,
            timestamp
        );
    }

    function getLogBatch(uint256 index)
        public
        view
        returns (
            uint256 id,
            string memory batchHash,
            string memory timestamp
        )
    {
        require(index < logBatches.length, "Invalid index");

        LogBatch memory batch = logBatches[index];

        return (
            batch.id,
            batch.batchHash,
            batch.timestamp
        );
    }

    function getLogBatchesCount() public view returns (uint256) {
        return logBatches.length;
    }

    function registerCredential(
        string memory uid,
        string memory aliasName,
        string memory role,
        bool active,
        string memory timestamp
    ) public {
        require(!credentialExists(uid), "Credential already exists");

        uint256 credentialId = credentials.length;

        credentials.push(
            Credential({
                id: credentialId,
                uid: uid,
                aliasName: aliasName,
                role: role,
                active: active,
                timestamp: timestamp
            })
        );

        emit CredentialRegistered(
            credentialId,
            uid,
            aliasName,
            role,
            active,
            timestamp
        );
    }

    function updateCredentialStatus(
        string memory uid,
        bool active,
        string memory timestamp
    ) public {
        bool found = false;
        uint256 credentialIndex = 0;

        for (uint256 i = 0; i < credentials.length; i++) {
            if (
                keccak256(bytes(credentials[i].uid)) ==
                keccak256(bytes(uid))
            ) {
                found = true;
                credentialIndex = i;
                break;
            }
        }

        require(found, "Credential not found");

        credentials[credentialIndex].active = active;
        credentials[credentialIndex].timestamp = timestamp;

        emit CredentialStatusUpdated(
            credentials[credentialIndex].id,
            uid,
            active,
            timestamp
        );
    }

    function getCredential(uint256 index)
        public
        view
        returns (
            uint256 id,
            string memory uid,
            string memory aliasName,
            string memory role,
            bool active,
            string memory timestamp
        )
    {
        require(index < credentials.length, "Invalid index");

        Credential memory credential = credentials[index];

        return (
            credential.id,
            credential.uid,
            credential.aliasName,
            credential.role,
            credential.active,
            credential.timestamp
        );
    }

    function getCredentialsCount() public view returns (uint256) {
        return credentials.length;
    }

    function credentialExists(string memory uid) public view returns (bool) {
        for (uint256 i = 0; i < credentials.length; i++) {
            if (
                keccak256(bytes(credentials[i].uid)) ==
                keccak256(bytes(uid))
            ) {
                return true;
            }
        }

        return false;
    }
}