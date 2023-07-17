import tkinter as tk
from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

win = tk.Tk()
# Set window size here to '440x640' pixels
win.geometry('440x640')
# Set window title here to 'FedUni Banking'
win.title('FedUni Banking')

# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()

# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var, show='*')

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry = tk.Entry(win)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(win, height=10, width=48)

# The bank account object we will work with
account = BankAccount()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    pin_number_var.set('')

def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''    

    # Limit to 4 chars in length
    if pin_number_var.get().__len__() < 4:
        # Set the new pin number on the pin_number_var
        pin_number_var.set(pin_number_var.get() + event.widget['text'])

def log_in(event):
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global account_number_entry

    # Create the filename from the entered account number with '.txt' on the end
    filename = account_number_entry.get() + '.txt'

    # Try to open the account file for reading
    try:
        # Open the account file for reading
        global account_file
        account_file = open(filename, 'r')
        lines = account_file.readlines()

        # First line is account number
        account.set_account_number(lines[0])
        # Second line is PIN number, raise exception if the PIN entered doesn't match account PIN read
        account.set_pin_number(lines[1])

        if int(pin_number_var.get()) != int(account.get_pin_number()):
            raise Exception

        # Read third and fourth lines (balance and interest rate) 
        account.set_balance(lines[2])
        account.set_interest_rate(lines[3])
        account.set_transaction_list(lines[4:])

        # Section to read account transactions from file - start an infinite 'do-while' loop here

            # Attempt to read a line from the account file, break if we've hit the end of the file. If we
            # read a line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list

        # Close the file now we're finished with it
        account_file.close()
        remove_all_widgets()
        create_account_screen()


    # Catch exception if we couldn't open the file or PIN entered did not match account PIN
    except Exception:
        # Show error messagebox and & reset BankAccount object to default...
        tk.messagebox.showerror('Failed', 'Bad Username or Password!')
        account = BankAccount()
        #  ...also clear PIN entry and change focus to account number entry
        pin_number_var.set('')
        account_number_entry.focus_set()

    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen


# ---------- Button Handlers for Account Screen ----------

def save_and_log_out(event):
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account

    # Save the account with any new transactions
    file = open(str(account.get_account_number()) + '.txt', 'r+')
    file.write(account.save_to_file())
    file.close()
    # Reset the bank account object
    account = BankAccount()
    # Reset the account number and pin to blank
    account_number_var.set('')
    pin_number_var.set('')
    account_number_entry.focus_set()
    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()

def perform_deposit(event):
    '''Function to add a deposit for the amount in the amount entry to the
       account's transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        depo = amount_entry.get()
        # Deposit funds
        account.deposit_funds(float(depo))
    
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.

        # Change the balance label to reflect the new balance
        la3 = tk.Label(win, text='Balance: ${}'.format(account.get_balance()))
        # Clear the amount entry
        amount_entry = tk.Entry(win)
        # Update the interest graph with our new balance
        create_account_screen()
    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except Exception:
        tk.messagebox.showerror('Failed', 'Error!')
def perform_withdrawal(event):
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's withdraw_funds method
        withdraw = amount_entry.get()
        # Withdraw funds
        account.withdraw_funds(float(withdraw))

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.

        # Change the balance label to reflect the new balance
        la3 = tk.Label(win, text='Balance: ${}'.format(account.get_balance()))
        # Clear the amount entry
        amount_entry = tk.Entry(win)
        # Update the interest graph with our new balance
        create_account_screen()

    # Catch and display any returned exception as a messagebox 'showerror'
    except Exception:
        tk.messagebox.showerror('Failed', 'Error!') 

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()

def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''
    global account
    # YOUR CODE to generate the x and y lists here which will be plotted
    x = list(range(1, 13))
    y = []
    num = account.get_balance()

    for i in range(12):
        y.append(num)
        num += num * (account.get_interest_rate() / 12)

    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5, 2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()
    
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')


# ---------- UI Screen Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''    
    
    # ----- Row 0 -----

    # 'FedUni Banking' label here. Font size is 32.
    la1 = tk.Label(win, text='FedUni Banking', font=('None', 32))
    la1.grid(row=0, columnspan=3, sticky='news')

    # ----- Row 1 -----

    # Account Number / Pin label here
    la2 = tk.Label(win, text='Account Number / PIN')
    la2.grid(row=1, column=0, sticky='news')
    # Account number entry here
    account_number_entry.grid(row=1, column=1, sticky='news')

    # Account pin entry here
    account_pin_entry.grid(row=1, column=2, sticky='news')

    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    b1 = tk.Button(win, text='1')
    b1.bind('<Button-1>', handle_pin_button)
    b1.grid(row=2, column=0, sticky='news')

    b2 = tk.Button(win, text='2')
    b2.bind('<Button-1>', handle_pin_button)
    b2.grid(row=2, column=1, sticky='news')

    b3 = tk.Button(win, text='3')
    b3.bind('<Button-1>', handle_pin_button)
    b3.grid(row=2, column=2, sticky='news')

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    b4 = tk.Button(win, text='4')
    b4.bind('<Button-1>', handle_pin_button)
    b4.grid(row=3, column=0, sticky='news')

    b5 = tk.Button(win, text='5')
    b5.bind('<Button-1>', handle_pin_button)
    b5.grid(row=3, column=1, sticky='news')

    b6 = tk.Button(win, text='6')
    b6.bind('<Button-1>', handle_pin_button)
    b6.grid(row=3, column=2, sticky='news')

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    b7 = tk.Button(win, text='7')
    b7.bind('<Button-1>', handle_pin_button)
    b7.grid(row=4, column=0, sticky='news')

    b8 = tk.Button(win, text='8')
    b8.bind('<Button-1>', handle_pin_button)
    b8.grid(row=4, column=1, sticky='news')

    b9 = tk.Button(win, text='9')
    b9.bind('<Button-1>', handle_pin_button)
    b9.grid(row=4, column=2, sticky='news')

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    bclear = tk.Button(win, text='Cancel / Clear', bg='red')
    bclear.bind('<Button-1>', clear_pin_entry)
    bclear.grid(row=5, column=0, sticky='news')

    # Button 0 here
    b0 = tk.Button(win, text='0')
    b0.bind('<Button-1>', handle_pin_button)
    b0.grid(row=5, column=1, sticky='news')

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    blogin = tk.Button(win, text='Log In', bg='green')
    blogin.bind('<Button-1>', log_in)
    blogin.grid(row=5, column=2, sticky='news')

    # ----- Set column & row weights -----

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.rowconfigure(0, weight=2)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=2)
    win.rowconfigure(3, weight=2)
    win.rowconfigure(4, weight=2)
    win.rowconfigure(5, weight=2)
    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)


def create_account_screen():
    '''Function to create the account screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var
    
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    la1 = tk.Label(win, text='FedUni Banking', font=('None', 24))
    la1.grid(row=0, columnspan=5, sticky='news')

    # ----- Row 1 -----

    # Account number label here
    la2 = tk.Label(win, text='Account Number: {}'.format(account.get_account_number()))
    la2.grid(row=1, column=0, sticky='news')
    # Balance label here
    la3 = tk.Label(win, text='Balance: ${}'.format(account.get_balance()))
    la3.grid(row=1, column=1, sticky='news')
    # Log out button here
    blogout = tk.Button(win, text='Log Out')
    blogout.bind('<Button-1>', save_and_log_out)
    blogout.grid(row=1, column=2, columnspan=3, sticky='news')
    

    # ----- Row 2 -----

    # Amount label here
    la4 = tk.Label(win, text='Amount($)')
    la4.grid(row=2, column=0, sticky='news')
    # Amount entry here
    amount_entry.grid(row=2, column=1, sticky='news')
    # Deposit button here
    bdeposit = tk.Button(win, text='Deposit')
    bdeposit.bind('<Button-1>', perform_deposit)
    bdeposit.grid(row=2, column=2, sticky='news')
    # Withdraw button here
    bwithdraw = tk.Button(win, text='Withdraw')
    bwithdraw.bind('<Button-1>', perform_withdrawal)
    bwithdraw.grid(row=2, column=3, columnspan=2, sticky='news')

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    text_scrollbar = tk.Scrollbar(win)
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    trans_text = tk.Text(win, height=15)
    trans_text.insert(tk.END, account.get_transaction_string())
    trans_text.configure(state=tk.DISABLED)
    trans_text.grid(row=3, column=0, columnspan=4, sticky='news')

    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited
    # Now add the scrollbar and set it to change with the yview of the text widget
    trans_text.config(yscrollcommand=text_scrollbar.set)
    text_scrollbar.config(command=trans_text.yview)
    text_scrollbar.grid(row=3, column=4, sticky='nsw')

    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    win.rowconfigure(0, weight=2)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    win.rowconfigure(3, weight=1)
    win.rowconfigure(4, weight=1)
    win.columnconfigure(0, weight=2)
    win.columnconfigure(1, weight=2)
    win.columnconfigure(2, weight=1)
    win.columnconfigure(3, weight=0)
    win.columnconfigure(4, weight=0)

# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
win.mainloop()
