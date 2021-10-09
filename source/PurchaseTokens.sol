pragma solidity ^0.8.9;

import './isk_platform.sol';

contract ERC20Token {
    
    struct Users {
        address _id;
        int balance;
        string name;
    }

    Users[] public user;

    mapping(address => uint) public balances;

    function mint() public virtual {
        balances[msg.sender] ++;
    }
}

contract IsoKoin is ERC20Token {
    string public symbol = 'ISK';

    string public name = "IsoKoin";

    address[] public owners; // initialise an array of addresses
    uint public ownerCount;

    function mint() public override {
        super.mint();
        ownerCount ++;
        owners.push(msg.sender);
    }
}

contract TransferingWallet {
    address payable wallet;
    address public token;

    constructor(address payable _wallet, address _token) {
        wallet = _wallet;
        token = _token;
    }

    function buyToken() public payable {
        ERC20Token _token  = ERC20Token(address(token));

        _token.mint();

        wallet.transfer(msg.value);
    }
}