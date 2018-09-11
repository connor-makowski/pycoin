LIFEcoin
===============

A Python based blockchain tool for managing cash flows in humanitarian efforts

Features
--------

- Allow users to create a Blockchain and add blocks of transactional data to it
- Allow users to verify identity and amount of funds available to specific participants
- Allow users to cryptographically secure transactions, validate them and record them in blocks
- Allow users to validate other Blockchains and reach a consensus among a system of users

Prerequisites
-------------

This project uses a number of open source projects to work properly:

* [Crypto] - A simple interface to GPG encryption and decryption

How to Use
----------

Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Command Line Interface

1. Clone this repo in your preferred directory:
    ```sh
    $ git clone https://github.mit.edu/conmak/LIFEcoin.git
    ```
	
2. Initialize Python.
    ```sh
    $ python
    ```
3. Import the Blockchain code and some associated functions.
    ```sh
    >>> import LIFEcoin
	>>> from LIFEcoin import Determine_My_Public_Key
	>>> from LIFEcoin import Read_Private_Key_File
    ```

4. Create your Blockchain object (Named 'X').
    ```sh
    >>> X=LIFEcoin.Blockchain()
    ```
	
5. Create an Admin and Funds Account.
    ```sh
	>>> X.Balance_Sheet.Add_Account(r"C:\users\conmak\desktop\HLBC_Keys", "Admin_Account")
	>>> X.Balance_Sheet.Add_Account(r"C:\users\conmak\desktop\HLBC_Keys", "Funds_Account")
    ```

6. Create variables that represent each account's public keys.
    ```sh
	>>> Admin_Public_Key=Determine_My_Public_Key(r"C:\users\conmak\desktop\HLBC_Keys", "Admin_Account")
	>>> Funds_Public_Key=Determine_My_Public_Key(r"C:\users\conmak\desktop\HLBC_Keys", "Funds_Account")
    ```

7. Initialize your Blockchain (Create your first Block) and give the Admin account some arbitrarily large amount of LifeCoin. The Admin will control the total amount of funds available in the system.
    ```sh
	>>>X.Initialize(Admin_Public_Key, 100000000000000000)
    ```
	
8. Generate a transaction for the total amount of funding that is currently available to the system.
    ```sh
	>>> X.Generate_Transaction(Funds_Public_Key, 5000, r"C:\users\conmak\desktop\HLBC_Keys", "Admin_Account")
    ```

9. Add organizations and users for this Blockchain and determine their public keys.
    ```sh
	>>> X.Balance_Sheet.Add_Account(r"C:\users\conmak\desktop\HLBC_Keys", "Org1_Account")
	>>> X.Balance_Sheet.Add_Account(r"C:\users\conmak\desktop\HLBC_Keys", "Org2_Account")
	>>> X.Balance_Sheet.Add_Account(r"C:\users\conmak\desktop\HLBC_Keys", "User1_Account")
	>>> X.Balance_Sheet.Add_Account(r"C:\users\conmak\desktop\HLBC_Keys", "User2_Account")
	>>> Org1_Public_Key=Determine_My_Public_Key(r"C:\users\conmak\desktop\HLBC_Keys", "Org1_Account")
	>>> Org2_Public_Key=Determine_My_Public_Key(r"C:\users\conmak\desktop\HLBC_Keys", "Org2_Account")
	>>> User1_Public_Key=Determine_My_Public_Key(r"C:\users\conmak\desktop\HLBC_Keys", "User1_Account")
	>>> User2_Public_Key=Determine_My_Public_Key(r"C:\users\conmak\desktop\HLBC_Keys", "User2_Account")
    ```

10. Allocate LifeCoin to users.
    ```sh
	>>> X.Generate_Transaction(User1_Public_Key, 10, r"C:\users\conmak\desktop\HLBC_Keys", "Funds_Account")
	>>> X.Generate_Transaction(User2_Public_Key, 10, r"C:\users\conmak\desktop\HLBC_Keys", "Funds_Account")
    ```

11. Allow users to claim their LifeCoins as cash by trading it to Organizations for any desired from of local currency.
    ```sh
	>>> X.Generate_Transaction(Org1_Public_Key, 10, r"C:\users\conmak\desktop\HLBC_Keys", "User1_Account")
    ```

12. Try to double dip on allocated cash. (Let a user try to withdrawl more than is allowed.)
    ```sh
	>>> X.Generate_Transaction(Org1_Public_Key, 10, r"C:\users\conmak\desktop\HLBC_Keys", "User1_Account")
    ```

13. Add a block to the Blockchain. (any node in the network can do this)
    ```sh
	>>> X.Add_Block(Org1_Public_Key)
    ```

14. Check running balances of all accounts in the Blockchain.
    ```sh
	>>> print (vars(X.Running_Balance))
    ```

15. Attempt to check and record a transaction that has already been submitted. (In Line 92 of LIFEcoin.py, there is a special variable called "trial_1" which represents the last transaction that has been submitted. This should be removed before deploying LIFEcoin in a live setting.)
    ```sh
	>>> X.Check_And_Record(X.Trial1)
    ```

License
-------

Copyright 2018 Connor Makowski

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job.)

[Crypto]: <https://pypi.org/project/crypto/>

