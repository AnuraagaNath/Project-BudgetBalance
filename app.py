import streamlit as st
from gsheet import CreditSheetUpdater, DebitSheetUpdater



# Title
st.title('Project-BalanceBudget')
    
# Check Balance
if st.button('Check Balance'):
    updater = CreditSheetUpdater()
    st.markdown(f' #### Current balance: {updater.getCurrentBalance()}')


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
        updater.update_expense(dateofexpense = str(dateofexpense), 
                            expense_type = expense_type, 
                            expense_details=expense_details, 
                            expense_amount = expense_amount)
        
        st.success(f'Sucessfully added ₹{expense_amount} for {expense_type} to the Credit sheet')
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
        st.success(f'Sucessfully added ₹{added_balance} via {type_bal} to the Debit sheet')
        st.session_state.number_input = None
    elif not added_balance and submit_button2:
        st.warning('Please enter all the details')


