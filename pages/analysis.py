import streamlit as st
import pandas as pd
from gsheet import Data
import plotly.express as px

data = Data()

df = data.getData()

st.title('Budget Analysis')

# preprocessing
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df['Total Added Balance'] = df['Total Added Balance'].apply(lambda x: int(x) if x else 0)
df = df.sort_values('Date')
st.table(df)


# Expense over date
st.markdown('## Expense over Time')
datewise = df.groupby('Date')['Expense Amount'].sum().reset_index()

expenses = px.line(data_frame=datewise, x='Date', y='Expense Amount', markers='o', title='Expense over time').update_layout(xaxis_title='Date', yaxis_title='Amount')

st.plotly_chart(expenses)


# monthwise budget and expense
st.markdown('## Budget and Expense')

month = st.selectbox('Choose the month', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Semtember', 'October', 'November', 'December'])

year = st.selectbox('Choose the Year', [2024])

temp = df.copy()
temp['Month'] = temp['Date'].dt.month_name()
temp['Year'] = temp['Date'].dt.year
categorywise = temp.groupby(['Expense Type', 'Budget', 'Date', 'Month', 'Year'])['Expense Amount'].sum().reset_index()
categorywise = categorywise.query(f'Month==\'{month}\' and Year=={year}')

if st.button('Get Budget Analysis'):

    df_melted = categorywise.melt(id_vars=["Expense Type", "Date"], value_vars=["Budget", "Expense Amount"], var_name="Category", value_name="Amount")

    budgetandexpense = px.bar(df_melted, x="Expense Type", y="Amount", color="Category", barmode="group", title=f'Budget and Expense based on {month}').update_layout(yaxis_title='Budget/Expense Amount')

    st.plotly_chart(budgetandexpense)