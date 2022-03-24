from datetime import datetime
import pandas as pd
import streamlit as st
from dashboard import dashboard_ui
from hypothesis_testing import hypothesis_testing_ui
from utility import *

st.set_page_config(layout='wide')

df = pd.read_csv("dataset/supermarket_sales - Sheet1.csv")
df = df.drop(['Branch', "Tax 5%", "gross margin percentage"], axis=1)
df.columns = [
    'invoice_id',
    'city',
    'customer_type',
    'gender',
    'product_line',
    'unit_price',
    'quantity',
    'total',
    'date',
    'time',
    'payment',
    'cogs',
    'gross_income',
    'Rating',
]

df['time'] = pd.to_datetime(df['time'] + ' ' + df['date'])
df = df.drop(['date'], axis=1)

selected_ui = st.sidebar.selectbox(
    'Select a UI',
    ["Dashboard", "Hypothesis Testing"],
    index=1)

if selected_ui == "Dashboard":

    selected_store = st.sidebar.selectbox(
        'Select a City',
        ["All Store", *df.city.unique()])

    df = df[df['city'] == selected_store] if selected_store != "All Store" else df

    selected_month = st.sidebar.selectbox(
        'Select a Month',
        ["Lifetime", *df.time.sort_values().dt.strftime('%B %Y').unique()])

    if selected_month != "Lifetime":
        previous_month = datetime.strptime(selected_month, '%B %Y')
        previous_month = offset_month(previous_month, -1)
        previous_month = previous_month.strftime('%B %Y')

        current_df = df[df['time'].dt.strftime('%B %Y') == selected_month]
        previous_df = df[df['time'].dt.strftime('%B %Y') == previous_month]
    else:
        current_df = df
        previous_df = df.iloc[0:0]

    dashboard_ui(current_df, previous_df)

if selected_ui == "Hypothesis Testing":
    hypothesis_testing_ui(df)
