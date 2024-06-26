import pandas as pd
import streamlit as st
from gsheet import CreateTable, Updater



# functionality
st.title('Project-BalanceBudget')

if st.button('Reload'):
    st.rerun()
    
if st.button('Check Balance'):
    updater = Updater()
    st.markdown(f' #### Current balance: {updater.getCurrentBalance()}')





st.markdown('### Expense')
expense_type = st.selectbox('Expense Type:', ['Other Expenses', 'Travel', 'Food', 'Medicine', 'Clothes', 'Electronics Appliances'])
dateofexpense = st.date_input('Enter Date')
expense_amount = st.number_input('Amount of the expense', value=None)

if expense_type and expense_amount and st.button('Enter', key='Done1'):
    updater = Updater()
    updater.update_expense(dateofexpense = str(dateofexpense),
                                           expense_type = expense_type, 
                                           expense_amount = expense_amount)
    total_expense = updater.getTotalExpense()
    st.success('Sucessfully added to the balance sheet')
    st.text(f'Total amount of expense of all time (Todo: By month): {total_expense} \n Current balance remaining is {updater.getCurrentBalance()}')
    st.session_state.number_input = None
elif (not expense_type or not expense_amount) and st.button('Enter', key='Empty1'):
    st.warning('Please enter all the details')




st.markdown('### Added Balance')
added_balance = st.number_input('Amount of money added', value=None)
if added_balance and st.button('Enter', key='Done2'):
    updater = Updater()
    updater.update_AddedBalance(added_balance)
    st.success(f'Sucessfully added ₹{added_balance} to the balance sheet')
    st.session_state.number_input = None
elif not added_balance and st.button('Enter', key='Empty2'):
    st.warning('Please enter all the details')


