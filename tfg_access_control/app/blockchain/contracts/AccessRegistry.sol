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

    struct CredentialEvent {
        uint256 id;
        string uidHash;
        string actionType;
        string role;
        bool active;
        string timestamp;
    }

    AdminAction[] private adminActions;
    LogBatch[] private logBatches;
    CredentialEvent[] private credentialEvents;

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

    event CredentialEventRegistered(
        uint256 indexed id,
        string uidHash,
        string actionType,
        string role,
        bool active,
        string timestamp
    );

    function registerAdminAction(string memory actionType, string memory targetUid, string memory timestamp) public {
        uint256 actionId = adminActions.length;

        adminActions.push(
            AdminAction({
                id: actionId,
                actionType: actionType,
                targetUid: targetUid,
                timestamp: timestamp
            })
        );

        emit AdminActionRegistered(actionId, actionType, targetUid, timestamp);
    }

    function getAdminAction(uint256 index) public view returns (uint256 id, string memory actionType, string memory targetUid, string memory timestamp) {
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

    function registerLogBatch(string memory batchHash, string memory timestamp) public {
        uint256 batchId = logBatches.length;

        logBatches.push(
            LogBatch({
                id: batchId,
                batchHash: batchHash,
                timestamp: timestamp
            })
        );

        emit LogBatchRegistered(batchId, batchHash, timestamp);
    }

    function getLogBatch(uint256 index) public view returns (uint256 id, string memory batchHash, string memory timestamp) {
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

    function registerCredentialEvent(string memory uidHash, string memory actionType, string memory role, bool active, string memory timestamp) public {
        uint256 eventId = credentialEvents.length;

        credentialEvents.push(
            CredentialEvent({
                id: eventId,
                uidHash: uidHash,
                actionType: actionType,
                role: role,
                active: active,
                timestamp: timestamp
            })
        );

        emit CredentialEventRegistered(
            eventId,
            uidHash,
            actionType,
            role,
            active,
            timestamp
        );
    }

    function getCredentialEvent(uint256 index) public view returns (uint256 id, string memory uidHash, string memory actionType, string memory role, bool active, string memory timestamp) {
        require(index < credentialEvents.length, "Invalid index");

        CredentialEvent memory credentialEvent = credentialEvents[index];

        return (
            credentialEvent.id,
            credentialEvent.uidHash,
            credentialEvent.actionType,
            credentialEvent.role,
            credentialEvent.active,
            credentialEvent.timestamp
        );
    }

    function getCredentialEventsCount() public view returns (uint256) {
        return credentialEvents.length;
    }
    
}