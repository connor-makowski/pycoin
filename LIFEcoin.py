import hashlib
import time
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA512

proof_of_work='000'
digits=len(proof_of_work)

def Read_Private_Key_File(key_location, account_name=""):
    private_key_file = open(key_location+r"\Private_Key_"+account_name+".txt", "r")
    PEM_private_key = private_key_file.read()
    private_key_file.close()
    obj_key=RSA.importKey(PEM_private_key.encode('utf-8'))
    return obj_key

def Determine_My_Public_Key(key_location, account_name=""):
    obj_key=Read_Private_Key_File(key_location, account_name)
    PEM_Public_Key=((obj_key.publickey()).exportKey()).decode('utf-8')
    print ('Public key stored')
    return PEM_Public_Key

class Blockchain:
    def __init__(self):
        self.Chain={}
        self.Balance_Sheet=self.Balances()
        self.Running_Balance=self.Balances()
        self.Recent_Transaction_Blocks=10
        self.Recent_Transactions=self.Recent_Transaction()
        self.Recent_Pre_Block_Transactions=self.Recent_Transaction()
        print ('Blockchain Sucessfully Created!')
        
    def Initialize(self, Public_Key, Funding_Amount):
        self.Block_ID=1
        Current_Block=self.Block(self.Block_ID)
        Current_Block.Add_To_Donor_Act(self.Initialization_Block(), Public_Key, Funding_Amount)
        Current_Block.Calculate_Nonce()
        Current_Block.Finalize()
        self.Chain[self.Block_ID]=Current_Block
        Next_Block=self.Block(self.Block_ID+1)
        self.Chain[self.Block_ID+1]=Next_Block
        self.Gen_Next_Block()
        Temp_Balance_Sheet=self.Balances()
        Temp_Balance_Sheet.Account_Status=dict(self.Balance_Sheet.Account_Status)
        self.Recent_Transactions.Compute(self.Chain, self.Recent_Transaction_Blocks, self.Block_ID)
        self.Chain[self.Block_ID]=Current_Block
        for Transaction in Current_Block.data:
            self.Balance_Sheet.Adjust(Transaction)
        self.Running_Balance.Account_Status=dict(self.Balance_Sheet.Account_Status)
        self.Block_ID=2
        print ('First Block Initialized')
    
    def Gen_Next_Block(self):
        Next_Block=self.Block(self.Block_ID+2)
        self.Chain[self.Block_ID+2]=Next_Block
        
    def Add_Block(self, Public_Key):
        Current_Block=self.Chain[self.Block_ID]
        Previous_Block=self.Chain[self.Block_ID-1]
        Current_Block.Begin_Block(Previous_Block, Public_Key)
        Current_Block.Calculate_Nonce()
        Current_Block.Finalize()
        self.Submit_Block(Current_Block)
        #Send Block to System
    
    #Receive Block From System
    def Submit_Block(self, Block_To_Submit):
        if self.Validate_Block_Sequence(Block_To_Submit.block_id, Block_To_Submit):
            print ('Validation of block sequence passed')
            Temp_Balance_Sheet=self.Balances()
            Temp_Balance_Sheet.Account_Status=dict(self.Balance_Sheet.Account_Status)
            self.Recent_Pre_Block_Transactions.Compute(self.Chain, self.Recent_Transaction_Blocks, self.Block_ID)
            if Block_To_Submit.Validate_Block(Temp_Balance_Sheet, self.Recent_Pre_Block_Transactions):
                print ('Validation of all transactions in block passed')
                self.Gen_Next_Block()
                self.Block_ID=Block_To_Submit.block_id+1
                self.Chain[self.Block_ID-1]=Block_To_Submit
                for Transaction in Block_To_Submit.data:
                    self.Balance_Sheet.Adjust(Transaction)
                self.Running_Balance.Account_Status=dict(self.Balance_Sheet.Account_Status)
                for Transaction in (self.Chain[self.Block_ID]).data:
                    self.Running_Balance.Adjust(Transaction)
                self.Recent_Transactions.Compute(self.Chain, self.Recent_Transaction_Blocks, self.Block_ID+1)
                print ('Block Submitted')
            else:
                print ('Invalid Transactions in Block')
        else:
            print ('Invalid Block Sequence')
    
    #TODO Code in exception for missed blocks
    #TODO Code in way to accept different Chain
    
    def Generate_Transaction(self, To, Amount, key_location, account_name=""):
        New_Transaction=self.Transaction(To, Amount, key_location, account_name)
        #Save Trial1 to try to submit the same transaction twice 
        #Remove this Code for actual use
        self.Trial1=New_Transaction
        self.Check_And_Record(New_Transaction)
        #Send Transaction to System
    
    #Receive Transaction
    def Check_And_Record(self, Transaction):
        #TODO Check if connected to more than half of nodes
        if Transaction.Verify():
            print ('Transaction is valid')
            if self.Recent_Transactions.Check_Transaction(Transaction):
                print ('Not a duplicate')
                print ('Submitted in acceptable time frame')
                if (self.Running_Balance).Check_Balance(Transaction):
                    print ('User balance is sufficient')
                    (self.Chain[self.Block_ID+1]).Insert_Transaction(Transaction)
                    (self.Running_Balance).Adjust(Transaction)
                    print ('Transaction Submitted')
                else:
                    print ('Insufficient Balance')
            else:
                print('Duplicate or Timed Out Transaction')
        else:
            print ('Invalid Transaction')

    def Validate_Chain(self):
        for Block_ID in range(len(self.Chain))[2:-2]:
            if self.Validate_Block_Sequence(Block_ID):
                pass
            else:
                return False
        return True
    
    def Validate_Block_Sequence(self, Block_ID, Block_To_Submit='Chain'):
        if Block_To_Submit=='Chain':
            Block_To_Validate=self.Chain[Block_ID]
        else:
            Block_To_Validate=Block_To_Submit
        Test_Block=Block_To_Validate
        Previous_Block=self.Chain[Block_ID-1]
        if Block_To_Validate.current_timestamp<=Block_To_Validate.last_timestamp:
            return False
        if Block_To_Validate.last_timestamp!=Previous_Block.current_timestamp:
            return False
        if Block_To_Validate.block_id!=Block_ID:
            return False
        if Block_To_Validate.Hash_Data(Block_To_Validate.data)!=Block_To_Validate.hashed_data:
            return False
        if Test_Block.Apply_Hash(Test_Block.nonce)!=Block_To_Validate.hash:
            return False
        if Block_To_Validate.hash[:digits]!=proof_of_work:
            return False
        if Previous_Block.hash!=Block_To_Validate.last_hash:
            return False
        else:
            return True
    
    class Initialization_Block:
        def __init__(self):
            self.block_id=-1
            self.hash='0000000000000000000000000000000000000000000000000000000000000000'
            self.current_timestamp=0
            
    class Block:
        def __init__(self, Block_ID):
            self.block_id=Block_ID
            self.data=[]
            self.current_timestamp=time.time()
        
        def Insert_Transaction(self, Transaction):
            (self.data).append(Transaction)
        
        def Begin_Block(self, previous_block, Public_Key):
            self.public_key=Public_Key
            self.last_hash=previous_block.hash
            self.last_timestamp=previous_block.current_timestamp
            self.hashed_data=self.Hash_Data(self.data)
        
        def Add_To_Donor_Act(self, previous_block, Public_Key, Funding_Amount):
            self.public_key=Public_Key
            Extra_Funds=self.Additional_Funding(Public_Key, Funding_Amount)
            (self.data).append(Extra_Funds)
            self.last_hash=previous_block.hash
            self.last_timestamp=previous_block.current_timestamp
            self.hashed_data=self.Hash_Data(self.data)

        def Apply_Hash(self, nonce):
            hash_output = self.Hash_Data(
                                str(self.block_id).encode('utf-8')+
                                str(self.last_hash).encode('utf-8')+
                                str(self.last_timestamp).encode('utf-8')+
                                str(self.public_key).encode('utf-8')+
                                str(self.hashed_data).encode('utf-8')+
                                str(nonce).encode('utf-8')
                             )
            return hash_output

        def Calculate_Nonce(self):
            nonce=0
            while self.Apply_Hash(nonce)[:digits]!=proof_of_work:
                nonce +=1
            self.nonce=nonce

        def Finalize(self):
            self.hash=self.Apply_Hash(self.nonce)
            self.current_timestamp=time.time()
            #Announce Block to system
        
        def Validate_Block(self, Temp_Balance_Sheet, Recent_Transactions):
            for Transaction in self.data:
                if Transaction.Verify() and Temp_Balance_Sheet.Check_Balance(Transaction):
                    if Recent_Transactions.Check_Transaction(Transaction):
                        Temp_Balance_Sheet.Adjust(Transaction)
                    else:
                        return False
                else:
                    return False
            return True
        
        def Hash_Data(self, data):
            hash_value = hashlib.sha256()
            hash_value.update(str(data).encode('utf-8'))
            return hash_value.hexdigest()
        
        class Additional_Funding():
            def __init__(self, Public_Key, Funding_Amount):
                self.To=Public_Key
                self.From='System'
                self.Amount=Funding_Amount
            
            def Verify(self):
                return True
    
    class Recent_Transaction:
        def __init__(self):
            pass
        
        #TODO Code in exception for missed transactions
            
        def Compute(self, Chain, Blocks_To_Consider, Block_ID):
            self.Recent_Transaction_Signatures=[]
            Num_Blocks=Block_ID
            self.Starting_Timestamp=Chain[max(1,Num_Blocks-Blocks_To_Consider-3)].last_timestamp
            for Block_Num in range(Num_Blocks)[max(1,Num_Blocks-Blocks_To_Consider-2):]:
                for Transaction in Chain[Block_Num].data:
                    if Transaction.From!='System':
                        self.Recent_Transaction_Signatures.append(Transaction.Signature)
        
        def Check_Transaction(self, Transaction):
            if Transaction.From=='System':
                return True
            if Transaction.Time>self.Starting_Timestamp:
                if Transaction.Signature not in self.Recent_Transaction_Signatures:
                    self.Recent_Transaction_Signatures.append(Transaction.Signature)
                    return True
            return False
                
    class Balances:
        def __init__(self):
            self.Account_Status={}
        
        def Add_Account(self, key_location, account_name=''):
            random_generator = Random.new().read
            obj_key = RSA.generate(1024, random_generator)
            PEM_private_key=(obj_key.exportKey()).decode('utf-8')
            private_key_file = open(key_location+r"\Private_Key_"+account_name+".txt", "w")
            private_key_file.write(PEM_private_key)
            private_key_file.close()
            Public_Key=((obj_key.publickey()).exportKey()).decode('utf-8')
            self.Account_Status[Public_Key]=0
            print ('Account added to for {}'.format(account_name))
        
        def Recompute(self, Chain):
            for Public_Key in self.Account_Status:
                self.Account_Status[Public_Key]=0
            for Block_ID in range(len(Chain))[1:-1]:
                Block_Data=Chain[Block_ID].data
                for Transaction in Block_Data:
                    self.Adjust(Transaction)
        
        def Adjust(self, Transaction):
            if Transaction.From!='System':
                self.Account_Status[Transaction.From]-=Transaction.Amount
            if Transaction.To not in self.Account_Status:
                self.Account_Status[Transaction.To]=0
            self.Account_Status[Transaction.To]+=Transaction.Amount
        
        def Check_Balance(self, Transaction):
            if Transaction.From=='System':
                return True
            if self.Account_Status[Transaction.From]>=Transaction.Amount:
                return True
            return False
    
    class Transaction:
        def __init__(self, To, Amount, key_location, account_name):
            self.Time=time.time()
            obj_key=Read_Private_Key_File(key_location, account_name)
            From=((obj_key.publickey()).exportKey()).decode('utf-8')
            Transaction_String="{to_var}{amount_var}{from_var}{time_var}".format(to_var=To, amount_var=Amount, from_var=From, time_var=self.Time)
            hashed_transaction=self.Hash_Transaction(Transaction_String)
            Signature=obj_key.sign(hashed_transaction, '')
            self.To=To
            self.From=From
            self.Amount=Amount
            self.Signature=Signature
            print ('Transaction Generated')
        
        def Verify(self):
            public_key=RSA.importKey((self.From).encode('utf-8'))
            Transaction_String="{to_var}{amount_var}{from_var}{time_var}".format(to_var=self.To, amount_var=self.Amount, from_var=self.From, time_var=self.Time)
            hashed_transaction=self.Hash_Transaction(Transaction_String)
            verify=public_key.verify(hashed_transaction, self.Signature)
            return verify
        
        def Hash_Transaction(self, Transaction_String):
            return SHA512.new(str(Transaction_String).encode('utf-8')).digest()
