pragma solidity ^0.8;

contract MyContract {
    bool public myBool = true;
    int public myInt = -1;
    uint public myUint = 1; // unsigned integers are like the absolute values so they cannot be negative 
    // you can also specify how many bytes can the unsigned integer store 
    uint256 public myUint256 = 10; // this is the defaul value if we don't specify its size 

    // then you have an enum which is an enumerated list whic will allow us to keep track of things within our contract
    // the following example shows an enum that will allow us to keep track of the states within our contract 
    enum State {waiting, ready, active}
    State public state; // now we will be able to access the enum pulbicly using the getter 

    constructor() public {
        state = State.waiting; // this is set to be the defaul state 
    }

    function active() public {
        state = State.active;  // this function is used to set the state to active
    }

    fucntion isActive() public view returns(bool) {
        return state == State.active; // this function will check the state of the contract
    }


    uint256 public peopleCount = 0;
    mapping(uint => Person) public people; 

    struct Person {
        uint _id; // this is like the index that we implement 
        string _name;
        string _surname;
    }
    

    function addPerson(string memory _name, string memory _surname) public {
        incrementCount() 
        people[peopleCount] = Person(peopleCount, _name, _surname); // this is the first person that we are going to add people[peopleCount]
    }

    function incrementCount() internal {
        peopleCount += 1;
    }

}