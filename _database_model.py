from datetime import timedelta
from flask import Flask, request, session
import os
from os import path as ps
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.engine.base import Transaction
from sqlalchemy.orm import relationship
from flask_sqlalchemy import BaseQuery, SQLAlchemy
import datetime
import rsa

create_engine("mysql+pymysql://isokoin:pw@host/db", pool_pre_ping=True)
ROOT_DIR = os.path.dirname(os.getcwd())
app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='static'
)static

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///isokoin.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'top secret!'
app.secret_key = 'password'
app.permanent_session_lifetime = timedelta(minutes=50)
db = SQLAlchemy(app)

#------------------------------ BACKEND FUNCTIONALITY-----------------------------------------------

# this is for index and block 
def textfile_i_o(filename, text, write, _seek=True):
    try:
        file = open(filename, 'r+')
    except FileNotFoundError:
        file = open(filename, 'w')
        file.close()
    file = open(filename, 'r+')
    content = file.read()
    if write:
        if _seek:
            file.seek(0)
        else:
            pass
        file.write(text)
    else:
        pass
    file.close()
    return content

class File(object):
    	
    def __init__(self, filename, mode):
        self.filename = filename 
        self.mode = mode 
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    def __exit__(self, exec_type, exec_val, traceback):
        self.file.close()

class FileUpdateSystem(File):

    def __init__(self, *a ,**kw):
        self.a = a 
        self.kw = kw

    def convert_data_to_html_table(self):
        pass
    
    # make sure to copy the line as its represented
    def deleteLine(self, filename, lines_to_delete):
        # filtering 
        for line_to_delete in lines_to_delete:
            with File(filename, 'r+') as f:
                output = []
                content = f.readlines()
                for line in content:
                    if line.startswith(line_to_delete):
                        print('deleted line: ',line)
                        pass
                    else:
                        output.append(line)
        # rewriting 
        with File(filename, 'w') as f:
            for line in output:
                f.write(line)
    
    def series_to_list(self, series):
        list_ = [i for i in series]
        return list_

    def generate_table(self, _blockchain):

        for block in _blockchain.chain:
            transactions = block.transactions
            for transaction in transactions:
                i: Transaction = transaction
                print(i)

                table_of_contents = f'''
<tr>
<th>{i.index}</th>
<td>{i.sender}</td>
<td>{i.ammount}</td>
<td>{i.receiver}</td>
<td>{i.time}</td>
<td>{i.hash}</td>
</tr>
                '''
        with File('info.html', 'w') as f:
            f.write(table_of_contents)
        
    
    def append_from_pending(self, blockchain):

        for transaction in blockchain.transactions:
            i: Transaction = transaction
            print(i)

            table_of_contents = f'''
<tr>
<th>{i.index}</th>
<td>{i.sender}</td>
<td>{i.ammount}</td>
<td>{i.receiver}</td>
<td>{i.time}</td>
<td>{i.hash}</td>
</tr>
            '''
            with File('info.html', 'w') as f:
                try:
                    f.write(table_of_contents)
                except UnboundLocalError:
                    pass
        
    # find a way to append the tables int the destianation files
    def append_table(self, blockchain, section_to_target):
        filename = r'templates\account.html'
        try:
            self.generate_table(blockchain)
        except UnboundLocalError:
            self.append_from_pending(blockchain)

        

        with File(filename, 'r') as fin, File('output.html', 'w') as fout, File('info.html', 'r') as content:
            table = content.read()
            fin_list = fin.readlines()
            print(fin_list)
            for line in fin_list:
                
                fout.write(line)
                if line == section_to_target + '\n':
                    print(line)
                    fout.write(table)
                    fout.write('\n')
                else:
                    pass

        with File(filename, 'w') as fout, File('output.html', 'r') as fin:
            content = fin.read()
            fout.write(content)
        


    def update_block_list(self, _blockchain, section_to_target):
        output_updated = False
        filename = r'templates\blockchain.html'
        for block in _blockchain.chain:
            new_block = f'''
            <div class="card flex">
                <p>Block: {block.index}</p>
                <p>Hash: {block.hash}</p>
                <p>Nonse: {block.nonse}</p>
                <p>Previous Hash: {block.previous}</p>
                <p>Time: {block.time}</p>
                <a href="../view_transactions" class="btn btn-outline">View Transactions</a>
                <i class="fas fa-database fa-3x"></i>
            </div>
            ''' 
            


            with File(filename, 'r') as fin, File('output.html', 'w') as fout:
                content = fin.readlines()
                for line in content:
                    print(line)
                    fout.write(line)
                    if line == section_to_target + '\n':
                        fout.write(new_block)
                        output_updated = True
                        fout.write('\n')
                    else:
                        pass
        if output_updated:            
            with File(filename, 'w') as fout, File('output.html', 'r') as fin:
                content = fin.read()
                fout.write(content)                

def generate_key(password):
    public_key, private_key = rsa.newkeys(2048)
    encrypted_password = password.encode('utf8')
    encrypted_password = str(rsa.encrypt(encrypted_password, public_key))

    return encrypted_password, str(private_key), str(public_key)
    
def retrive_password(encrypted_password, public_key):
    password = rsa.decrypt(encrypted_password, public_key)
    decrypted_password = password.decode('utf8')
    return decrypted_password

def create_transaction_data(transactions, sender):

    found_user = check_if_registered(sender)

    try:
        if found_user == False:
            return None
        else:
            db.create_all()
            session_data = Transactions(
                session_id=increment_id(Transactions), 
                user_id= found_user.participant_id,
                content = transactions.hash
            )
            db.session.add(session_data)
            db.session.commit()
            return session_data
    except AttributeError:
        return None

def update_user_balance(sender, ammount):
    db.create_all()
    user = db.session.query(UserAccount).filter_by(username=sender).first()
    try:
        user.balance -= ammount
    except AttributeError:
        pass
    print('updating balance of: ',user)
    db.session.commit()
    return user

def generate_block_number():
    _index = textfile_i_o('block_index.txt','', False)
    print('block number: ',_index) 
    _index = int(_index) + 1
    _index = textfile_i_o('block_index.txt',f'{_index}', True)
    return int(_index)

def update_receiver_balance(receiver_username, ammount):
    db.create_all()
    receiver = db.session.query(UserAccount).filter_by(username=receiver_username).first()
    receiver.balance += ammount
    db.session.commit()
    return receiver

def create_user_data(username, password, public_key):
    public_key = str(public_key)
    encrypted_password, private_key, _ = generate_key(password)
    
    db.create_all()
    session_data = UserAccount(
        participant_id=increment_id(UserAccount),
        username=username, 
        password=encrypted_password,
        public_key=public_key,
        private_key = private_key
    )
    db.session.add(session_data)
    db.session.commit()
    return session_data

def reset(reset_all_users=False, reset_all_posts=False):
    if 'username' in session:
        print('          loading reset .....')
        db.create_all()
        all_users = db.session.query(UserAccount).all()
        all_posts = db.session.query(Transactions).all()
        if reset_all_users:
            for user in all_users:
                users_to_delete = UserAccount.query.filter_by(username=user.participant_id).first()
                db.session.delete(users_to_delete)
                db.session.commit()
        else:
            pass
        if reset_all_posts:
            for post in all_posts:
                posts_to_delete = users_to_delete = Transactions.query.filter_by(session_id=post.session_id).first()
                db.session.delete(posts_to_delete)
                db.session.commit()
        else:
            pass
        print(all_users)
        session.pop('username', None) 
        session.pop('password', None) 
        session.pop('date', None) 
    else:
        pass  
    
def increment_id(column_objct):
    db.create_all()
    users = db.session.query(column_objct).all()
    return len(users) + 1
        
def init_session_(*args):
    for attribute_values in args:
        session[attribute_values] = request.form[attribute_values]     

def check_database_column(column_objct):
    db.create_all()
    datasess = db.session.query(column_objct).all() 
    print(datasess)

def check_if_registered(sender):
    db.create_all()
    found_user = db.session.query(UserAccount).filter_by(username=sender).first()
    print(f' checking if {sender} is registered.....')
    if type(found_user) == BaseQuery:
        return None
    elif found_user == None:
        return None
    else:
        return found_user

# -------------------------------- DATABASE MODEL OBJECTS----------------------------------------------
class UserAccount(db.Model):
    default_password, default_key, public_key = generate_key('password')
    __tablename__ = 'user_account'
    participant_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(80), nullable=False, default=f'username{participant_id}', unique=True)
    password = Column(String(80), nullable=False, default=f'{default_password}', unique=True)
    balance = Column(Integer, nullable=False, default=10000)
    public_key = Column(String(80), nullable=False, default=f'{public_key}', unique=True)
    private_key = Column(String(80), nullable=False, default=f'{default_key}', unique=True)
    transactions = relationship('Transactions', backref='author', lazy=True)
    address =  Column(String(80), nullable=False, default='127.0.0.1:5500')
    
    def __repr__(self):
        return f'''
        UserAccount(
                username : {self.username},
                participant id : {self.participant_id},
                transactions completed: {self.transactions},
                balance : {self.balance} ISK,
                address : {self.address},
                public key: {self.public_key}
            )
        '''
    
class Transactions(db.Model):

    session_id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String(80), nullable=False, default='start session')
    user_id = Column(Integer, ForeignKey('user_account.participant_id'), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'''
            Transactions(
                date : {self.date},
                session id : {self.session_id},
                content: {self.content},
                author : {self.user_id}
            )
        '''
