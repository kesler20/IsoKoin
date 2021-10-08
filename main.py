from flask import redirect, url_for, render_template, request, session, flash
from _database_model import *
from blockchain import *
from datetime import datetime

_blockchain = Blockchain()
file_manager = FileUpdateSystem()
_INDEX = 0

def make_transaction(sender, receiver, ammount, private_key, index):
    transaction = Transaction(sender, receiver, ammount, private_key, index)
    transaction.transactionValidation(private_key)  
    if transaction.transaction_granted:
        _blockchain.transactions.append(transaction) # this is the transactions_block(n) collection
    else:
        pass
    summary = transaction.transactions
    return transaction.transaction_granted, summary

@app.route('/login/', methods=['POST', 'GET'])
def logins():
    if request.method == 'POST':
        init_session_('username','password')
        username = session['username']
        password = session['password']
        transactions = 'No transactions recorded'
        balance = 10000
        corresponding_users_in_database = check_if_registered(username)
        
        if corresponding_users_in_database == None:
            #REEGISTRATION PROCESS
            encrypted_password, private_key, public_key = generate_key(password)
            registered_user = create_user_data(username,password, public_key)
            print(f' the following user data has been registered: {registered_user}')
        else:
            # LOAD OTHER INFO FROM DATABASE
            print(corresponding_users_in_database)
            balance = corresponding_users_in_database.balance
            public_key = corresponding_users_in_database.public_key
            transactions = corresponding_users_in_database.transactions
            private_key = corresponding_users_in_database.private_key

        session['transactions'] = transactions
        session['balance'] = int(balance)
        session['public_key'] = public_key
        session['private_key'] = private_key
    else:
        pass
    return render_template('index.html')
    
@app.route('/account/', methods=['POST','GET'])
def accounts():
    global _INDEX
    global file_manager 
    global _blockchain

    # WHETHER REQUEST METHOD IS POST OR GET IT DOES THE SAME THING
    if request.method == 'POST':
        if 'username' in session:
            balance = int(session['balance'])
            sender = session['username']
            receiver = request.form['receiver']
            ammount = int(request.form['amt'])
            private_key = session['private_key']
            if balance > ammount:
                # transaction index refers to the transaction list containing transactions objects
                usr = update_user_balance(sender, ammount)
                try:
                    print('user blance:', usr.balance)
                except AttributeError:
                    flash('Please request an account in the login section!!')
                    return render_template('error.html')

                transaction_granted, summary = make_transaction(sender, receiver, ammount, private_key, _INDEX)
                if transaction_granted:
                    session['balance'] -= ammount
                    session['transactions'] = summary
                    data = create_transaction_data(summary, sender)
                    print('the following transaction data was created: ',data)
                    try:
                        receiver = update_receiver_balance(receiver, ammount)
                    except AttributeError:
                        flash('you cannot send ISOKOINs to people who are not registered!!')
                        sender = receiver
                        receiver = session['username']
                        transaction_granted, summary = make_transaction(sender, receiver, ammount, private_key, _INDEX)
                        session['balance'] += ammount
                        session['transactions'] = summary
                        data = create_transaction_data(summary, sender)
                        print('the following transaction data was created: ',data)
                        receiver = update_receiver_balance(receiver, ammount)
                        return render_template('error.html')
                    
                    print('receiver :', receiver)

                    balance = session['balance']  
                    public_key = session['public_key']
                    username = session['username']
                    transactions = session['transactions']
                    summary = _blockchain.transactions
                    file_manager.append_table(_blockchain, '                        </tr><!----->')

                    return render_template('account.html', balance=balance, public_key=public_key, username=username, transactions=transactions, summary=summary) 
                else:
                    summary = 'No transactions recorded'
                    flash('you cannot send ISOKOINs from another persons account!!')
                    return render_template('error.html')
            else:
                summary = 'No transactions recorded'
                flash("You don't have sufficient ISOKOINs ")
                return render_template('error.html')
                
        else:
            flash('Please request an account in the login section!!!')
            return render_template('error.html')
    else:
        if 'username' in session:
            balance = session['balance']
            public_key = session['public_key']
            username = session['username']
            transactions = session['transactions']
            summary = _blockchain.transactions
            file_manager.append_table(_blockchain, '                        </tr><!----->')

            return render_template('account.html', balance=balance, public_key=public_key, username=username, transactions=transactions, summary=summary)
        else:
            flash('Please request an account in the login section!!!')
            return render_template('error.html')

@app.route('/poll/<vote>', methods=['POST', 'GET'])
def polls(vote):
    if 'username' in session:
        if request.method == 'GET':
            use_case_voted = vote
            try:
                comment_made = request.form['comment']
            except KeyError:
                comment_made = 'no comment'
            print(session['username'], comment_made)
            print(session['username'], use_case_voted)
            with File('feedback.txt', 'a') as f, File('voting-poll.txt', 'a') as fpoll: # also save the name of the username that did that
                f.write('' + comment_made + ' by ' + session['username'] + '\n')
                fpoll.write('' + use_case_voted + ' by ' + session['username'] + '\n')
            return redirect(url_for('polls')) # maybe render a thank you message that shows the progress in the voting
        else:
            return render_template('poll.html')  
    else:
        flash('Please request an account in the login section!!!')
        return render_template('error.html')          

@app.route('/blockchain/', methods=['POST','GET'])
def blockchains():
    global file_manager
    global _INDEX
    global _blockchain

    target_section = '            </div><!--THIS-->'

    if request.method == 'GET':
        _block = _blockchain.getLastBlock()
        session['new_block_hash'] = _block.hash
        session['new_block_nonse'] = _block.nonse


        file_manager.update_block_list(_blockchain, target_section)
            
        return render_template(
            'blockchain.html', 
            block_number=_INDEX, 
            _hash=session['new_block_hash'], 
            nonse=session['new_block_nonse'],
            previous_hash=_block.previous,
            timestamp=datetime.now(),
            transactions=[transactions for transactions in _block.transactions]
        )

    else:

        _block = Block(_blockchain.transactions, datetime.now(), _INDEX) # get the transactions_block(n) stored in the blockchain
        _block.mineBlock(_blockchain)
        _blockchain.addBlock(_block)
        _block = _blockchain.getLastBlock()
        _INDEX = generate_block_number()
        file_manager.update_block_list(_blockchain, target_section)

    session['new_block_hash'] = _block.hash
    session['new_block_nonse'] = _block.nonse

    return render_template('blockchain.html', pending_transactions=_blockchain.transactions)

@app.route('/view_transactions')
def view_transactions():
    global _blockchain 

    transaction = _blockchain.transactions
    transaction = 'there are no transactions' if len(transaction) == 0 else transaction
    flash(transaction)
    return render_template('error.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<page>/', methods=['POST','GET'])
def show(page):
    if page == 'login':
        redirect(url_for('logins'))

    elif page == 'account':
        redirect(url_for('accounts'))

    elif page == 'transactions':
        redirect(url_for('transactions'))
    
    elif page == 'mine':
        redirect(url_for('miners'))

    elif page == 'blockchain':
        redirect(url_for('blockchains'))
    else:
        pass
    return render_template(f'{page}.html')

if __name__ == '__main__':
    _blockchain.addGenesisBlock()
    app.run(debug=True, port=5500)

# view transaction function to open up all the transactiosns 