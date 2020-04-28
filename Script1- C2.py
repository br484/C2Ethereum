from web3 import Web3

#importamos o módulo web3 e criamos um objeto de conexão com o servidor ganache-cli
blockchain_server="ws://172.16.91.132:8545"
#especificação do websocket
web3=Web3(Web3.WebsocketProvider(blockchain_server))
abi='[{"constant":false,"inputs":[{"name":"newtestvalue","type":"string"}],"name":"set_test","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"print_test","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"name","type":"string"}],"name":"tellmethename","type":"event"}]'

#EVM utiliza o bytecode gerado após a compilação do solidity (remix.ethereum.org).
bytecode="608060405234801561001057600080fd5b506040805190810160405280601481526020017f53697374656d6173446973747269627569646f730000000000000000000000008152506000908051906020019061005c929190610062565b50610107565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100a357805160ff19168380011785556100d1565b828001600101855582156100d1579182015b828111156100d05782518255916020019190600101906100b5565b5b5090506100de91906100e2565b5090565b61010491905b808211156101005760008160009055506001016100e8565b5090565b90565b6103ea806101166000396000f3fe608060405260043610610046576000357c0100000000000000000000000000000000000000000000000000000000900480635613a7961461004b578063d5221ec814610113575b600080fd5b34801561005757600080fd5b506101116004803603602081101561006e57600080fd5b810190808035906020019064010000000081111561008b57600080fd5b82018360208201111561009d57600080fd5b803590602001918460018302840111640100000000831117156100bf57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192905050506101a3565b005b34801561011f57600080fd5b50610128610277565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561016857808201518184015260208101905061014d565b50505050905090810190601f1680156101955780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b80600090805190602001906101b9929190610319565b507fb04dd642e1aef882e099599e78e3ce85d42be9e7ff7434b5b928eb8f1d94dae1600060405180806020018281038252838181546001816001161561010002031660029004815260200191508054600181600116156101000203166002900480156102665780601f1061023b57610100808354040283529160200191610266565b820191906000526020600020905b81548152906001019060200180831161024957829003601f168201915b50509250505060405180910390a150565b606060008054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561030f5780601f106102e45761010080835404028352916020019161030f565b820191906000526020600020905b8154815290600101906020018083116102f257829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061035a57805160ff1916838001178555610388565b82800160010185558215610388579182015b8281111561038757825182559160200191906001019061036c565b5b5090506103959190610399565b5090565b6103bb91905b808211156103b757600081600090555060010161039f565b5090565b9056fea165627a7a7230582037e9d5bbd0c4950be5527fd9a8918e2c8333ed44a5ad4088eafa8ffbbf89b5220029"

wallet_key="0x97127A61Adcbc2a54023e40886cB9386cf2ec1fe"
private_key="0xf6d5155792a68d93d514358b692da6db4ac676136e15445d3db2651c7197e86b"

#criaremos um smart contractusando o método web3.eth.contract 
#contract_obj.constructor () : - isto significa que quando a transação é implantada, o construtor do contrato deve ser implantado.
#buildTransaction : - esta é a função que criará a transação.
#from : - o endereço da nossa carteira.
#nonce : - isto é basicamente como um contador que deve ser configurado para informar qual número de transação é esse do endereço da carteira
#gas : - especifica o limite máximo que pode ser definido na transação
#gasPrice : quantidade de Éter que você está disposto a pagar por cada unidade de gás e geralmente é medido em Gwei 

def create_contract():
    contract_obj = web3.eth.contract(abi=abi,bytecode=bytecode)
    construct_txn = contract_obj.constructor().buildTransaction({
        'from': wallet_key,
        'nonce': web3.eth.getTransactionCount(wallet_key),
        'gas': web3.eth.getBlock('latest').gasLimit,
        'gasPrice': web3.toWei('30', 'gwei')})

    print("[+] Contrato Criado")
#o método signTransactionseria usado para assiná-lo, que aceita dois argumentos:1) A transação que deve ser assinada 2) A chave privada associada à carteira
    signed = web3.eth.account.signTransaction(construct_txn,private_key)
    print("[+] Contrato Assinado")
#O sendRawTransaction enviará a transação assinada e esse método retornará um valor hexadecimal que é basicamente apenas um hash que representa o contrato na blockchain
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction).hex()
    print("[+] Contrato Implantado")
#O método waitForTransactionReceipt aguardará até que a transação seja minerada e gerará um recibo da transação.
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    if tx_receipt:
        print("[+] Contrato Minado")
        print("Endereço do Contrato",tx_receipt.contractAddress)
        get_testvalue(tx_receipt)

def get_testvalue(tx_receipt):
    print("[+] Chamando a função print_test")
    contract=web3.eth.contract(address=tx_receipt.contractAddress,abi=abi)
#functions () : - este método possui todas as funções que definimos em nosso contrato de solidity - print_test () : - essa foi a função que criamos para imprimir - call () : - este método executará a função e retornará o valor recebido do contrato inteligente
    print("\nEvento :-",contract.functions.print_test().call())    
    set_testvalue(contract,tx_receipt)     

def set_testvalue(contract,tx_receipt):
    name=input("Evento :-")
    print("[+] Construindo a transação")
#contract.functions.set_test () : - Aqui podemos ver que estamos trabalhando com a função set_test do nosso código solidity;
    construct_txn = contract.functions.set_test(name).buildTransaction({
    'from': wallet_key,
    'nonce': web3.eth.getTransactionCount(wallet_key),
    'gas': web3.eth.getBlock('latest').gasLimit,
    'gasPrice': web3.toWei('30', 'gwei')})
    
    print("[+] Transação Criada")
    signed = web3.eth.account.signTransaction(construct_txn,private_key)
    print("[+] Transação Assinada")
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction).hex()
    print("[+] Transação Implantada")
    check = web3.eth.waitForTransactionReceipt(tx_hash)

    if check:
        get_testvalue(tx_receipt)

create_contract() 

