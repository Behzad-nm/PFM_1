import pandas as pd
import os
import math


def checkAccount(account):
    global accounts
    if os.path.exists("Accounts.csv"):
        str_cols = {"accountNumber": "str"}
        accounts = pd.read_csv("Accounts.csv", dtype = str_cols)
        if (accounts.loc[accounts["accountNumber"] == account].any(axis = None)):
            return 1    # account exists
        else:
            return 0    # account does not exist
    else:
        return -1       # file is missing


def checkBalance(account):
    global accounts
    theAccount = accounts.loc[accounts["accountNumber"] == account]
    return theAccount["balance"]


def addAccount(bank,accountNumber,balance):
    global accounts
    id = 1 if math.isnan(accounts["ID"].max()) else accounts["ID"].max() + 1
    newAccount = pd.DataFrame([[id, bank, accountNumber, balance]])
    newAccount.to_csv("Accounts.csv", mode = "a", header = False, index = None)


def addTransaction(inOut, amount, account, date, time, description, category):
    global accounts
    if os.path.exists("Transactions.csv"):
        transactions = pd.read_csv("Transactions.csv")
        theAccount = accounts.loc[accounts["accountNumber"] == account]
        accountID = theAccount["ID"]
        balance = checkBalance(account)
        mainRecord = accounts.index[accounts["accountNumber"] == account]
        if not inOut:
            if balance.iloc[0] < amount:
                print("Error! There is not enough fund in this account\n")
            else:
                accounts.loc[mainRecord[0],"balance"] -= amount
        else:
            accounts.loc[mainRecord[0], "balance"] += amount
        accounts.to_csv("Accounts.csv", index = None)
        id = 1 if math.isnan(transactions["ID"].max()) else transactions["ID"].max() + 1
        theTransaction = pd.DataFrame([[id, inOut, amount, accountID.iloc[0], date, time, description, category]])
        theTransaction.to_csv("Transactions.csv", mode = "a", header = False, index = None)
    else:
        print("Ooops! I think some Files are missing!!\n")



def main():
    global accounts
    exit = 0
    checkAccount("-1")
    while not exit:
        operation = int(input("What you want to do?\n0 Add account\n1 Check balance\n2 Add transaction\n3 exit\n"))
        if operation == 0:
            print("Please enter your bank name, your account number and current balance\n")
            bank, accountNumber, balance = input(), input(), input()
            balance = float(balance)
            check = checkAccount(accountNumber)
            if check == 1:
                print("We already have this account\n")
            elif check == 0:
                addAccount(bank, accountNumber, balance)
            else:
                print("Ooops! I think some Files are missing!\n")
        elif operation == 1:
            accountNumber = input("Enter the account account number you want to check\n")
            check = checkAccount(accountNumber)
            if check == 1:
                balance = checkBalance(accountNumber)
                print("The balance of account number: " + accountNumber + " is:\n" + str(balance.iloc[0]))
            elif check == 0:
                print("Sorry, there is no account with this number\n")
            else:
                print("Ooops! I think some Files are missing!\n")
        elif operation == 2:
            print("Please enter the transaction details: type (0 for withdraw, 1 for deposite)" +
                  ", amount, account number, date, time, description and category\n")
            inOut, amount, accountNumber, date, time, description, category = \
                    int(input()), float(input()), input(), input(), input(), input(), input()
            check = checkAccount(accountNumber)
            if check == 1:
                addTransaction(inOut, amount, accountNumber, date, time, description, category)
            elif check == 0:
                print("Sorry, there is no account with this number\n")
            else:
                print("Ooops! I think some Files are missing!\n")
        elif operation == 3:
            break
        else:
            print("Please enter one number from 0 to 3!\n")

if __name__ == "__main__":
    main()
