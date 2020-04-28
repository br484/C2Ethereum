pragma solidity >=0.4.22 <0.6.0;

contract botchain{
    
    string  asd;
    address mywallet;
    
    constructor() public hello(){
        
        asd="Arquitetura de Sistemas Distribuidos";
    }
    
    function  print_asd() public view returns(string memory){
        
        return asd;
    }
    
    function set_asd(string memory newasdvalue) public{
        
        asd=newasdvalue;
    }
}
