from blockchain import *
from time import time
import pprint
import _database_model as dd

encrypted_password, private_key, public_key = dd.generate_key('hello world')

pp = pprint.PrettyPrinter(indent=4)

session_data = dd.create_user_data('kesler','hello world',public_key)
print(session_data)

transactions_block0 = []
for _ in range(4):
    transaction = Transaction('kesler','utomi','130',private_key,0)
    transaction.transactionValidation(private_key)
    transactions_block0.append(transaction)

transactions_block1 = []
for _ in range(4):
    transaction = Transaction('kesler','utomi','3',private_key,1)
    transaction.transactionValidation(private_key)
    transactions_block1.append(transaction)

transactions_block2 = []
for _ in range(4):
    transaction = Transaction('kesler','utomi','300',private_key,2)
    transaction.transactionValidation(private_key)
    transactions_block2.append(transaction)

_blockchain = Blockchain()
block = Block(transactions_block0, time(), 0)
block.mineBlock(_blockchain)
_blockchain.addBlock(block)

block = Block(transactions_block1, time(), 1)
block.mineBlock(_blockchain)
_blockchain.addBlock(block)

block = Block(transactions_block2, time(), 2)
block.mineBlock(_blockchain)
_blockchain.addBlock(block)

#_blockchain.mine_verify_blocks()
pp.pprint(_blockchain)
for block in _blockchain.chainJSONencode():
    pp.pprint(block)
    print(' ')
print('Lengh: ', len(_blockchain.chain))
