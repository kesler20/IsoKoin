from blockchain import *
from time import time
import pprint
import _database_model as dd

encrypted_password, private_key, public_key = dd.generate_key('hello world')

pp = pprint.PrettyPrinter(indent=4)

transactions_block0 = []
for _ in range(4):
    transaction = Transaction('kesler','utomi','13',private_key,0)
    transaction.transactionValidation(private_key)
    transactions_block0.append(transaction)

_blockchain = Blockchain()
block = Block(transactions_block0, time(), 0)
block.mineBlock(_blockchain)
_blockchain.addBlock(block)

file_manager = dd.FileUpdateSystem()

file_manager.generate_table(_blockchain)
