import mysql.connector as connector
import pandas as pd

class Database:
    # create and initialize the tables
    def __init__(self):
        self.conn = connector.connect(host = "localhost", 
                    port = "3306",
                    user = "root",
                    password = "9223", 
                    database = "budgetbalance")
        

        # create credit table
        query1 = '''
        create table if not exists credit(
            Id mediumint not null auto_increment primary key,
            Date date, 
            Added_Cash float,
            Added_UPI float,
            Total_Added_Balance float
        );'''


        # create debit table
        query2 = '''
        create table if not exists debit(
            Id mediumint not null auto_increment primary key,
            Date date, 
            Expense_Type varchar(20),
            Details varchar(100),
            Expense_Amount float
        );
        '''

        # create Current Balance record
        query3 = '''   
        create table if not exists balance(
            Id mediumint not null auto_increment primary key,
            Current_Balance float
        );
        '''

        self.curr = self.conn.cursor()
        self.curr.execute(query1)
        self.curr.execute(query2)
        self.curr.execute(query3)
        self.conn.commit()
    

    # fetch credit table
    def fetchCredit(self):
        self.curr.execute("select * from credit;")
        return pd.DataFrame(self.curr.fetchall(), columns=["Id", "Date", "Added_Cash", "Added_UPI", "Total_Added_Balance"])
    
    # fetch debit table
    def fetchDebit(self):
        self.curr.execute("select * from debit;")
        return pd.DataFrame(self.curr.fetchall(), columns=["Id", "Date", "Expense_Type", "Details", "Expense_Amount"])

    # add to the balance table
    def currBalance(self):

        # checks if the table is empty - then insert a 0 value initially
        query = "insert into balance(Current_Balance) select 0 where not exists (select 1 from balance);"
        self.curr.execute(query)

        # if the table is not empty - fetch the last updated balance 
        currBalanceQuery = "select Current_Balance from balance where Id = (select max(Id) from balance);"

        self.curr.execute(currBalanceQuery)
        currBalance = self.curr.fetchone()[0]
        self.conn.commit()

        return currBalance


    def updateBalance(self, currBalance):
        query = "insert into balance(Current_Balance) values({})".format(currBalance)
        self.curr.execute(query)
        self.conn.commit()

    # add to the credit table
    def addCredit(self, date, added_cash, added_upi):
        totalAddedBalance = added_cash + added_upi
        currBalance = self.currBalance()
        currBalance += totalAddedBalance
        self.updateBalance(currBalance)

        query = "insert into credit(Date, Added_Cash, Added_UPI, Total_Added_Balance) values('{}', {}, {}, {});".format(date, added_cash, added_upi, totalAddedBalance)
        self.curr.execute(query)
        self.conn.commit()

    # add to the debit table
    def addDebit(self, date, expense_type, details, expense_amount):
        currBalance = self.currBalance()
        currBalance -= expense_amount
        self.updateBalance(currBalance)

        query = "insert into debit(Date, Expense_Type, Details, Expense_Amount) values('{}', '{}', '{}', {})".format(date, expense_type, details, expense_amount)

        self.curr.execute(query)
        self.conn.commit()
    


    




