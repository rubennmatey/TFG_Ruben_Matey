// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AccessRegistry {
    struct AdminAction {
        uint256 id;
        string actionType;
        string targetUid;
        string timestamp;
    }

    AdminAction[] private adminActions;

    event AdminActionRegistered(
        uint256 indexed id,
        string actionType,
        string targetUid,
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
}