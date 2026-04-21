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

    AdminAction[] private adminActions;
    LogBatch[] private logBatches;

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

        emit AdminActionRegistered(actionId, actionType, targetUid, timestamp);
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

        emit LogBatchRegistered(batchId, batchHash, timestamp);
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
}