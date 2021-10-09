pragma solidity ^0.8.9;

contract IsoKoin {
    string public name = 'IsoKoin';
    string public symbol = 'ISK';
    string public standard = 'ISK Token v1.0.0';
    uint public decimals = 20;
    uint public maxSupply = 10000000000000000000000;

    constructor(
        string memory _name, 
        string memory _symbol, 
        uint _decimals, 
        uint _maxSupply
    ) 
    {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        maxSupply = _maxSupply;
    }

    // database to keep track of the balances
    mapping(address => uint) public balanceOf;
    mapping(address => mapping(address => uint)) public allowance;

    event Transfer(
        address indexed _from,
        address indexed _to,
        uint _value
    );

    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint _value
    );

    function IsKToken (uint _initialSupply) public {
        balanceOf[msg.sender] = _initialSupply;
        maxSupply = _initialSupply;
    }

    function transfer1(address _from, address _to, uint _value) external returns (bool success) {
        require(_to != address(0));
        // take tokens out of my account
        balanceOf[_from] = balanceOf[_from] - (_value);
        // add them to the person that we are passing it too
        balanceOf[_to] = balanceOf[_to] + (_value);
        emit Transfer(_from, _to, _value);
        return true;
    }

    function transfer2(address _to, uint _value) external returns (bool success) {
        require(balanceOf[msg.sender] >= _value);
        transfer1(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint _value) external returns (bool succes) {
        require(_spender != address(0));
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint _value) external returns (bool success) {
        require(_value <= balanceOf[_from]);
        require(_value <= allowance[_from][msg.sender] - (_value));
        transfer1(_from, _to, _value);
        return true;
    }

}