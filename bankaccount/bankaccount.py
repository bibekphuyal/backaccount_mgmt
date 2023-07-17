class BankAccount:

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number = 0
        self.pin_number = ''
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []

    def get_account_number(self):
        return self.account_number

    def set_account_number(self, number):
        self.account_number = int(number)

    def get_pin_number(self):
        return self.pin_number

    def set_pin_number(self, pin):
        self.pin_number = int(pin)

    def get_balance(self):
        return self.balance

    def set_balance(self, bal):
        self.balance = float(bal)

    def get_interest_rate(self):
        return self.interest_rate

    def set_interest_rate(self, rate):
        self.interest_rate = float(rate)

    def get_transaction_list(self):
        return self.transaction_list

    def set_transaction_list(self, trans):
        self.transaction_list = trans

    def deposit_funds(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        try:
            self.balance += amount
            self.transaction_list.append('\nDeposit\n{}'.format(float(amount)))
            return True, 'Success', 'Deposit successful!'
        except TypeError:
            return False, 'Failed', 'Please enter a positive number!'

    def withdraw_funds(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        try:
            if amount <= self.balance:
                self.balance -= float(amount)
                self.transaction_list.append('\nWithdrawal\n{}'.format(float(amount)))
                return True, 'Success' 'Withdraw Succeeded!'
            else:
                return False, 'Failed', 'Insufficient balance!'
        except TypeError:
            return False, 'Please enter a number!'
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''
        s1 = ''
        for e in self.transaction_list:
            s1 += str(e)
        return s1

    def save_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        s1 = ''
        for e in self.transaction_list:
            s1 += str(e)

        return '{}\n{}\n{}\n{}\n'.format(self.account_number, self.pin_number, self.balance, self.interest_rate) + s1