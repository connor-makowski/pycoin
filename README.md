pycoin
===============

A Python based blockchain tool for quickly creating Blockchains.

Features
--------

- Allow users to create a Blockchain and add blocks of transactional data to it
- Allow users to verify an anonymous identity and the amount of resources owned by that anonymous identity
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

1. Clone this repo in your preferred directory and enter the repo:
    ```sh
    $ git clone https://github.com/connor-makowski/pycoin.git
    $ cd pycoin
    ```
2. Initialize Python.
    ```sh
    $ python
    ```
3. Import the Blockchain code and some associated functions.
    ```sh
    >>> import pycoin
	  >>> from pycoin import Determine_My_Public_Key
	  >>> from pycoin import Read_Private_Key_File
    ```
4. Set your the location to store your private blockchain keys.
    ```sh
    >>> key_location=r"C:\users\conmak\desktop"
    ```

5. Create your Blockchain object (Named 'X').
    ```sh
    >>> X=pycoin.Blockchain()
    ```

6. Create an account for yourself and for a friend.
    ```sh
	  >>> X.Balance_Sheet.Add_Account(key_location, "MyAccount")
    >>> X.Balance_Sheet.Add_Account(key_location, "OtherAccount")
    ```

7. Create variables that represent each account's public keys.
    ```sh
	  >>> My_Public_Key=Determine_My_Public_Key(key_location, "MyAccount")
	  >>> Other_Public_Key=Determine_My_Public_Key(key_location, "OtherAccount")
    ```

8. Initialize your Blockchain.
    ```sh
	  >>>X.Initialize(My_Public_Key)
    ```

9. Generate a transaction to send your first mined coin to your friend's account.
    ```sh
	  >>> X.Generate_Transaction(To=Other_Public_Key, Amount=1, key_location, "MyAccount")
    ```

10. Try to double spend allocated resources.
    ```sh
	  >>> X.Generate_Transaction(To=Other_Public_Key, Amount=1, key_location, "MyAccount")
    ```

11. Add a block to the Blockchain. (any node in the network can do this)
    ```sh
	  >>> X.Add_Block(My_Public_Key)
    ```

12. Check running balances of all accounts in the Blockchain.
    ```sh
	  >>> X.Show_Balances()
    ```

13. Attempt to check and record a transaction that has already been submitted. (In Line 98 of pycoin.py, there is a special variable called "trial_1" which represents the last transaction that has been submitted. This should be removed before deploying pycoin in a live setting.)
    ```sh
	  >>> X.Check_And_Record(X.Trial1)
    ```
14. Validate all transactions in the chain. This should happen after you receive a new chain.
    ```sh
	  >>> X.Validate_Chain()
    ```

License
-------

Copyright 2018 Connor Makowski

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job.)

[Crypto]: <https://pypi.org/project/crypto/>
