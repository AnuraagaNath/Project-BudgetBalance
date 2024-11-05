import streamlit as st
from gsheet import CreditSheetUpdater, DebitSheetUpdater, BalanceSheet
# from database import Database


# Title
st.title('Project-BalanceBudget')

## database initialization
# db = Database()

# Check Balance
if st.button('Check Balance'):
    updater = BalanceSheet()
    st.markdown(f' #### Current balance: {updater.currBalance()}')
    # currBalance = db.currBalance()
    # st.markdown(f' #### Current balance: {currBalance}')



# Debit Section
st.markdown('### Debit')
with st.form("Debit", clear_on_submit=True):
    expense_type = st.selectbox('Expense Type:', ['Others', 'Cab', 'Rail', 'Metro', 'Subscription', 'Dine Out', 'Health', 'Shopping', 'Mom\'s Expense', 'Dad\'s Expense'])
    expense_details = st.text_input('Enter Details')
    dateofexpense = st.date_input('Enter Date')
    expense_amount = st.number_input('Amount of the expense', value=None)
    submit_button1 = st.form_submit_button("Enter")

    if expense_type and expense_amount and submit_button1:
        updater = DebitSheetUpdater()
        updater.update_expense(
                dateofexpense = str(dateofexpense), 
                expense_type = expense_type, 
                expense_details=expense_details, 
                expense_amount = expense_amount)
        
        balance = BalanceSheet()
        balance.updateBalance("Debit", expense_amount=expense_amount)
        # db.addDebit(date=dateofexpense, expense_type=expense_type, details=expense_details, expense_amount=expense_amount)
        
        st.success(f'Sucessfully added ₹{expense_amount} for {expense_type} to the debit sheet')
        st.session_state.number_input = None

    elif (not expense_type or not expense_amount) and submit_button1:
        st.warning('Please enter all the details')



# Credit Section
st.markdown('### Credit')
with st.form("Credit", clear_on_submit=True):
    date_income = st.date_input('Date')
    type_bal = st.selectbox('Type', ['UPI', 'Cash'])
    added_balance = st.number_input('Amount of money added', value=None)
    submit_button2 = st.form_submit_button("Enter")
    if added_balance and submit_button2:
        updater = CreditSheetUpdater()
        updater.update_AddedBalance(str(date_income), float(added_balance), type_bal)
        balance = BalanceSheet()
        balance.updateBalance("Credit", added_balance=added_balance)
        # if type_bal == "Cash":
        #     db.addCredit(date_income, added_cash=added_balance, added_upi=0)
        # elif type_bal == "UPI":
        #     db.addCredit(date_income, added_cash=0, added_upi=added_balance)

        st.success(f'Sucessfully added ₹{added_balance} via {type_bal} to the Credit sheet')
        st.session_state.number_input = None
    elif not added_balance and submit_button2:
        st.warning('Please enter all the details')


