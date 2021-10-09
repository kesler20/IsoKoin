pragma solidity ^0.8.9;

contract IskPlatform {

    uint public numberParticipants = 0;

    // update the state of the platform when changes are made
    enum State {sleeping, ready, active}
    State public state;

    constructor() {
        state = State.sleeping;
    }

    function activatePlatform() public {
        state = State.active;
    }

    // update the database of the participants when the accounts are requested
    struct Participant {
        int balance;
        string name;
    }

    Participant[] public people;

    function addParticipant(string memory _name, int _balance) public {
        people.push(Participant(_balance, _name));
        numberParticipants ++;
    }
}