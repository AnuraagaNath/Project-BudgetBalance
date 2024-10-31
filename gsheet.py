import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# for offline credential loading
# from dotenv import dotenv_values
# credentials = dotenv_values(".cred")
# sheet_id = dotenv_values(".sheet_id")

# Google Sheet Scope
scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]


#  Google Cloud Console Credentials for accessing Google Sheet
credentials =   {"type": st.secrets['type'], 
"project_id": st.secrets['project_id'],
"private_key_id": st.secrets['private_key_id'],
  "private_key": st.secrets['private_key'],
  "client_email": st.secrets['client_email'],
  "client_id": st.secrets['client_id'],
  "auth_uri": st.secrets['auth_uri'],
  "token_uri":st.secrets['token_uri'],
  "auth_provider_x509_cert_url": st.secrets['auth_provider_x509_cert_url'],
  "client_x509_cert_url": st.secrets['client_x509_cert_url'],
  "universe_domain": st.secrets['universe_domain']}


# Getting Connection
creds = Credentials.from_service_account_info(credentials, scopes=scopes)
client = gspread.authorize(creds)


workbook = client.open_by_key('1fvZS6RD0Nqg-kEHaVyIqAKIqaYeuI-bDrGrMAVrkPho')

class Data:
    def getDebitData(self):
        df = pd.DataFrame(workbook.worksheet('Debit').get_all_records())
        return df

    def getCreditData(self):
        df = pd.DataFrame(workbook.worksheet('Credit').get_all_records())
        return df


class DebitSheet:
    def __init__(self):
            self.sheet = self.initialize_sheet('Debit')

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

        return sheet

    def next_available_row(self):
        str_list = list(filter(None, self.sheet.col_values(1)))
        return str(len(str_list)+1)

class CreditSheet:
    def __init__(self):
        self.sheet = self.initialize_sheet('Credit')

    def initialize_sheet(self, SheetId):   
        sheet = workbook.worksheet(SheetId)

        def update_if_empty(cell, placeholder):
            if sheet.acell(cell).value is None:
                sheet.update_acell(cell, placeholder)

        update_if_empty('A1', 'Date')
        update_if_empty('B1', 'Balance Cash')
        update_if_empty('C1', 'Balance UPI')
        update_if_empty('D1', 'Total Added Balance')
        update_if_empty('E1', 'Total Balance')

        return sheet
    
    def next_available_row(self):
        str_list = list(filter(None, self.sheet.col_values(1)))
        return str(len(str_list)+1)

class DebitSheetUpdater(DebitSheet):
    
    def update_expense(self, dateofexpense, expense_type, expense_details, expense_amount):
        next_row = self.next_available_row()
        self.sheet.update_acell(f'A{next_row}', dateofexpense)
        self.sheet.update_acell(f'B{next_row}', expense_type)
        self.sheet.update_acell(f'C{next_row}', expense_details)
        self.sheet.update_acell(f'D{next_row}', expense_amount)

        # sum all values 
        values = self.sheet.batch_get(('D2:D',))[0]
        total_expense = sum([float(val[0]) for val in values])
        self.sheet.update_acell(f'E{next_row}', total_expense)

    def getTotalExpense(self):
        expenses = self.sheet.col_values(5)
        last_total_expense = expenses[-1] if expenses and len(expenses)>1 else 0
        return float(last_total_expense) 
    
        
class CreditSheetUpdater(CreditSheet):

    def getCurrentBalance(self):
        balances = self.sheet.col_values(5)
        prev_balance = balances[-1] if  balances and len(balances)>1 else 0
        return float(prev_balance)  


    def update_AddedBalance(self, date_income, added_balance, type_bal):
        next_row = self.next_available_row()
        self.sheet.update_acell(f'A{next_row}', date_income)
        if type_bal == 'Cash':
            self.sheet.update_acell(f'B{next_row}', added_balance)
            self.sheet.update_acell(f'C{next_row}', 0)
        else:
            self.sheet.update_acell(f'C{next_row}', added_balance)
            self.sheet.update_acell(f'B{next_row}', 0)
        prev_balance = self.getCurrentBalance()
        totalAddedBalance = float(self.sheet.acell(f'B{next_row}').value) + float(self.sheet.acell(f'C{next_row}').value) + prev_balance
        self.sheet.update_acell(f'D{next_row}', totalAddedBalance)


        debitsheet = DebitSheetUpdater()
        balance_left = totalAddedBalance - debitsheet.getTotalExpense()

        self.sheet.update_acell(f'E{next_row}', round(balance_left, 2))

        
