from mining_crypto import mine_pending_transactions
import json
import hashlib 
from _database_model import *
import datetime

class Blockchain (object):
     
    def __init__(self):
        self.pendingTransactions: list[Block] = []
        self.chain = self.pendingTransactions
        self.transactions: list[Transactions] = [] # this can be used as pending transactions 
        self.difficulty = 2
        self.mineRewards = 60
    
    def __repr__(self):
        return '''
            BlockChain(
                lenght : {},
                blocks : {}
            )
        '''.format(len(self.pendingTransactions),[block for block in self.pendingTransactions])

    def getLastBlock(self):
        try:
            block = self.chain[-1]
        except IndexError:
            block = self.addGenesisBlock()
        return block 
        
    def addBlock(self, block):
        block: Block = block
        block.previous = self.getLastBlock().hash
        self.pendingTransactions.append(block)

    def mine_verify_blocks(self):
        # clean the pending transactions from the blocks that have already been added 
        for block in self.pendingTransactions:
            if block in self.chain:
                pass
            else:
                self.chain.append(block)
        # check if the transactions within the blocks are verified and the blocks have been mined
        chain = []
        for block in self.pendingTransactions:     
            for transactions in block.transactions:
                if transactions.transaction_granted and block.mined:
                    chain.append(block)
                else:
                    print('some of the transactions within the block have not been granted')
                    print('or there ar some transactions that have not being mined')
                    
        return chain

    def chainJSONencode(self):
        blockArrJSON = []
        for block in self.chain:
            blockJSON = {}
            blockJSON['hash'] = block.hash
            blockJSON['previous'] = block.previous

            transactionJSON = []
            tJSON = {}
            for transaction in block.transactions:
                tJSON['time'] = transaction.time
                tJSON['sender'] = transaction.sender
                tJSON['receiver'] = transaction.receiver
                tJSON['ammount'] = str(transaction.ammount) + ' ISK' 
                tJSON['hash'] = transaction.hash
                transactionJSON.append(tJSON)
            
            blockJSON['transactions'] = transactionJSON
            blockArrJSON.append(blockJSON)
        return blockArrJSON

    def addGenesisBlock(self):
        tArr = []
        tArr.append(Transaction("me", "you", 1, '00000', 0))
        genesis = Block(tArr, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)

        genesis.previous = "None"
        return genesis

class Block (object): # let transactions be a list of transaction objects
    def __init__(self, transactions, time, index):
        self.transactions: list[Transaction] = transactions
        self.time = time
        self.index = index
        self.previous = ''
        self.hash = self.calculateHash()
        self.nonse = 0
        self.mined = False
    # remove the stransactions from the pending transactions when verifying in mineverrfying blocks
    def calculateHash(self):
        hashTransactions = ''
        for transaction in self.transactions: 
            hashTransactions += transaction.hash
        hashString = str(self.time) + hashTransactions + self.previous + str(self.index)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()

    def mineBlock(self, blockchain: Blockchain):
        self.hash, self.nonse = mine_pending_transactions(blockchain.difficulty,self.transactions, blockchain.getLastBlock().hash)
        self.mined = True
        try:
            [blockchain.transactions.remove(transaction) for transaction in blockchain.transactions]
        except ValueError:
            pass
        # add a block once is mined with the pending transactions  

class Transaction (Block):
    def __init__(self, sender, receiver, ammount, private_key, index):
        self.sender = sender
        self.receiver = receiver
        self.ammount = ammount
        self.time = datetime.datetime.now()
        self.transactions = '''
            sender: {},
            receiver: {},
            ammount: {} ISK,
            time: {},
        '''.format(self.sender,self.receiver,self.ammount,self.time)
        self.index = index
        self.hash = self.calculateTransactionHash()
        self.transaction_granted = self.transactionValidation(private_key)

    def __repr__(self):
        return '''
            sender: {},
            receiver: {},
            ammount: {} ISK,
            time: {},
            hash: {}
        '''.format(self.sender,self.receiver,self.ammount,self.time,self.hash)

    def calculateTransactionHash(self):

        transaction_encoded = json.dumps(self.transactions, sort_keys=True).encode()
        transaction_hash = hashlib.sha256(transaction_encoded).hexdigest()
        hashTransactions = transaction_hash

        hashString = str(self.time) + hashTransactions + str(self.index)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()       

    def transactionValidation(self, private_key):
        db.create_all()
        found_user = db.session.query(UserAccount).filter_by(private_key=private_key)
        if found_user:
            self.transaction_granted = True
        else:
            self.transaction_granted = False