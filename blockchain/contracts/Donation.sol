// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DonationContract {
    address public owner;
    mapping(address => uint256) public donations;

    event DonationReceived(address indexed donor, uint256 amount);
    event FundsWithdrawn(address indexed owner, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function donate() public payable {
        require(msg.value > 0, "Donation must be greater than 0");
        donations[msg.sender] += msg.value;
        emit DonationReceived(msg.sender, msg.value);
    }

    function withdraw() public {
        require(msg.sender == owner, "Only owner can withdraw");
        uint256 balance = address(this).balance;
        (bool success, ) = owner.call{value: balance}("");
        require(success, "Transfer failed.");
        emit FundsWithdrawn(owner, balance);
    }

    receive() external payable {
        donations[msg.sender] += msg.value;
        emit DonationReceived(msg.sender, msg.value);
    }

    fallback() external payable {
        donations[msg.sender] += msg.value;
        emit DonationReceived(msg.sender, msg.value);
    }
}
