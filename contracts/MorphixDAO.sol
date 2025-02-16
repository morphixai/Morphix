// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MorphixDAO {
    struct Proposal {
        uint id;
        string description;
        uint voteCount;
    }

    mapping(uint => Proposal) public proposals;
    uint public nextProposalId;

    function createProposal(string memory _description) public {
        proposals[nextProposalId] = Proposal(nextProposalId, _description, 0);
        nextProposalId++;
    }

    function vote(uint _proposalId) public {
        proposals[_proposalId].voteCount++;
    }
}
