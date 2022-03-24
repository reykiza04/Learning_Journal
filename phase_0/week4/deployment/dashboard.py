import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
from utility import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


def dashboard_ui(current_df, previous_df):
    st.title("My Store Dashboard")
    st.subheader("Sales Performance")

    current_transactions = current_df['invoice_id'].count()
    previous_transactions = previous_df['invoice_id'].count()

    sales_history = current_df.groupby(current_df.time.dt.strftime('%Y-%m-%d')).agg({'invoice_id': 'count'})
    sales_history.columns = ['transactions']
    sales_history.index = pd.to_datetime(sales_history.index)
    sales_history.index.name = 'date'
    sales_history = sales_history.reset_index()

    st.plotly_chart(px.bar(sales_history, x='date', y='transactions'), use_container_width=True)

    st.subheader("Store Performance")

    col1, col2, col3, col4 = st.columns(4)

    current_revenue = current_df['gross_income'].sum()
    previous_revenue = previous_df['gross_income'].sum()
    delta_revenue = current_revenue - previous_revenue

    current_item_sold = current_df['quantity'].sum()
    previous_item_sold = previous_df['quantity'].sum()
    delta_item_sold = current_item_sold - previous_item_sold

    current_rating = current_df['Rating'].mean()
    previous_rating = previous_df['Rating'].mean()
    delta_rating = current_rating - previous_rating

    col1.metric(label="Transactions", value=current_transactions, delta=str(current_transactions - previous_transactions))
    col2.metric(label="Items Sold", value=current_item_sold, delta=str(current_item_sold - previous_item_sold))
    col3.metric(label="Revenue", value='$ {:20,.2f}'.format(current_revenue), delta='{:20,.2f}'.format(delta_revenue))
    col4.metric(label="Rating", value='%.1f' % current_rating, delta='%.1f' % delta_rating)

    col1, col2 = st.columns(2)

    product_df = current_df.groupby('product_line').agg({'invoice_id': 'count'})
    product_df.columns = ['Count']
    product_df.index.name = 'Category'
    product_df = product_df.reset_index()
    col1.plotly_chart(px.pie(product_df, names='Category', values='Count'), use_container_width=True)

    store_df = current_df.groupby('city').agg({'invoice_id': 'count'})
    store_df.columns = ['Count']
    store_df.index.name = 'Category'
    store_df = store_df.reset_index()
    col2.plotly_chart(px.pie(store_df, names='Category', values='Count'), use_container_width=True)

    week_df = current_df.groupby(current_df.time.dt.day_name()).agg({'invoice_id': 'count'})
    dayofweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    week_df = week_df.reindex(dayofweek)
    week_df.columns = ['Transactions']

    col1, col2 = st.columns(2)
    col1.subheader("Average Daily Sales Performance")
    col2.subheader("Average Hourly Sales Performance")

    _, col2 = st.columns(2)
    selected_day = col2.selectbox("Select a Day", ["All Day", *dayofweek])

    col1, col2 = st.columns(2)

    day_df = current_df[current_df['time'].dt.day_name() == selected_day] if selected_day != "All Day" else current_df
    day_df = day_df.groupby(day_df.time.dt.strftime("%H")).agg({'invoice_id': 'count'})
    day_df.columns = ['Transactions']

    col1.plotly_chart(px.bar(week_df, text_auto=True), use_container_width=True)
    col2.plotly_chart(px.bar(day_df, text_auto=True), use_container_width=True)

    st.subheader("Product Line Performance")
    sales = current_df.groupby([current_df.time.dt.strftime('%Y-%m-%d'), 'product_line']).agg({'invoice_id': 'count'})

    sales = sales.reset_index()
    sales = sales.pivot(index='time', columns='product_line', values='invoice_id')
    sales = sales.fillna(0).astype(int)
    sales.index = pd.to_datetime(sales.index)

    options = st.multiselect(
        'Select Product Line',
        sales.columns.values,
        sales.columns.values[:2]
    )

    chart_data = pd.DataFrame(
        sales[options].values,
        sales.index,
        columns=options
    )

    # st.line_chart(chart_data)
    st.plotly_chart(px.bar(chart_data, x=chart_data.index, y=options, barmode='group', text_auto=True), use_container_width=True)

    st.subheader("Customer Demographics")


    col1, col2, col3 = st.columns(3)

    membership_df = current_df.groupby('customer_type').agg({'invoice_id': 'count'})
    membership_df.columns = ['Count']
    membership_df.index.name = 'Membership'
    membership_df = membership_df.reset_index()

    col1.plotly_chart(px.pie(membership_df, names='Membership', values='Count'), use_container_width=True)

    gender_df = current_df.groupby('gender').agg({'invoice_id': 'count'})
    gender_df.columns = ['Count']
    gender_df.index.name = 'Gender'
    gender_df = gender_df.reset_index()

    col2.plotly_chart(px.pie(gender_df, names='Gender', values='Count'), use_container_width=True)

    payment_df = current_df.groupby('payment').agg({'invoice_id': 'count'})
    payment_df.columns = ['Count']
    payment_df.index.name = 'Payment'
    payment_df = payment_df.reset_index()

    col3.plotly_chart(px.pie(payment_df, names='Payment', values='Count'), use_container_width=True)
