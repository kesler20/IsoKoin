from hashlib import sha256
import time

def SHA256(text):
    return sha256(text.encode('ascii')).hexdigest()

def mine(block_number, transactions, previous_hash, prefix_zeros):
    prefix_str = '0'*prefix_zeros
    nonce = 0
    commas = True
    transaction = ''
    for exchanges in transactions:
        transaction += exchanges.transactions 
    while commas == True:
        nonce += 1
        text = str(block_number) + transaction + previous_hash + str(nonce)
        new_hash = SHA256(text)
        if new_hash.startswith(prefix_str):
            commas = False
        else:
            print(f'Nonse: {nonce}')
            print(f'New Attempt: {new_hash}')
            print(f'we want: {prefix_str}')
    return new_hash, nonce

def mine_pending_transactions(difficulty, transactions, previous_hash):
    print('----------------------start mining----------------------')
    time.sleep(3)
    start_time = time.time()
    new_hash, nonse = mine(5, transactions, previous_hash, difficulty)
    total_time = time.time() - start_time
    print('''
        Block Mined!!
        Nonse: {}
        New Hash: {}
        time taken: {}
    '''.format(nonse, new_hash, total_time))
    time.sleep(3)
    return new_hash, nonse