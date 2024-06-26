import os
import gspread
import pandas as pd
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]

creds = Credentials.from_service_account_file('cred.json', scopes=scopes)
client = gspread.authorize(creds)

sheet_id = os.getenv('SHEET_ID')
workbook = client.open_by_key(sheet_id)

class Data:
    def getData(self):
        df = pd.DataFrame(workbook.worksheet('Sheet1').get_all_records())
        return df


class CreateTable:
    def initialize_sheet(self, SheetId):   
        sheet = workbook.worksheet(SheetId)

        def update_if_empty(cell, placeholder):
            if sheet.acell(cell).value is None:
                sheet.update_acell(cell, placeholder)

        update_if_empty('A1', 'Date')
        update_if_empty('B1', 'Expense Type')
        update_if_empty('C1', 'Budget')
        update_if_empty('D1', 'Expense Amount')
        update_if_empty('E1', 'Total Expense')
        update_if_empty('F1', 'Total Added Balance')
        update_if_empty('G1', 'Total Balance')

        return sheet

class Updater:
    def __init__(self):
        table = CreateTable()
        self.sheet = table.initialize_sheet('Sheet1')
        
    def getCurrentBalance(self):
        balances = self.sheet.col_values(7)
        prev_balance = balances[-1] if  balances and len(balances)>1 else 0
        return float(prev_balance)

    def getTotalExpense(self):
        return float(self.sheet.acell('E2').value)

    def next_available_row(self):
        str_list = list(filter(None, self.sheet.col_values(1)))
        return str(len(str_list)+1)

    def daily_budget_selector(self, expense_type):
        match expense_type:
            case 'Other Expenses':
                return 1500
            case 'Travel':
                return 1000
            case 'Food':
                return 2000
            case 'Medicine':
                return 500
            case 'Clothes':
                return 1000
            

    
    
    def update_expense(self, dateofexpense, expense_type, expense_amount):
        next_row = self.next_available_row()
        self.sheet.update_acell(f'A{next_row}', dateofexpense)
        self.sheet.update_acell(f'B{next_row}', expense_type)
        self.sheet.update_acell(f'C{next_row}', self.daily_budget_selector(expense_type))
        self.sheet.update_acell(f'D{next_row}', expense_amount)

        # sum all values 
        values = self.sheet.batch_get(('D2:D',))[0]
        total_expense = sum([float(val[0]) for val in values])
        self.sheet.update_acell(f'E{next_row}', total_expense)

        # subtract expense from balance
        current_balance = self.getCurrentBalance()
        expenses = self.sheet.col_values(4)
        last_expense = expenses[-1] if expenses and len(expenses) > 1 else 0
        current_balance = current_balance - float(last_expense)
        self.sheet.update_acell(f'G{next_row}', current_balance)
        
    


    def update_AddedBalance(self, added_balance):
        next_row = self.next_available_row()
        self.sheet.update_acell(f'F{next_row}', added_balance)
        self.update_balance(added_balance)

    def update_balance(self, added_balance):
        next_row = self.next_available_row()
        prev_balance = self.getCurrentBalance()
        total_balance = prev_balance + added_balance
        self.sheet.update_acell(f'G{next_row}', total_balance)
