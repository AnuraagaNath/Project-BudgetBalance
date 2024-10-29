import streamlit as st
import pandas as pd
from gsheet import Data
import plotly.express as px

data = Data()

credit = data.getCreditData()

debit = data.getDebitData()

st.title('Budget Analysis')

st.text("Credits")
st.table(credit)

st.text("Debits")
st.table(debit)

# preprocessing
debit['Date'] = pd.to_datetime(debit['Date'], format='mixed')

# Expense over date
st.markdown('## Expense over Time')
datewise = debit.groupby('Date')['Expense Amount'].sum().reset_index()

expenses = px.line(data_frame=datewise, x='Date', y='Expense Amount', markers='o', title='Expense over time').update_layout(xaxis_title='Date', yaxis_title='Amount')

st.plotly_chart(expenses)