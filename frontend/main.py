import requests
import streamlit as st
import pandas as pd
import numpy as np

st.title('KPIs Dashboard')

# Sidebar filters
st.sidebar.write("FILTERS")

active_lst = st.sidebar.multiselect(
    label="Active",
    options=[],
    default=[],
    key=None
)

fashion_lst = st.sidebar.multiselect(
    label="Fashion News",
    options=[],
    default=[],
    key=None
)

age_filtered_lst = st.sidebar.slider(
    'Select a range of ages',
    0, 100, (20, 80)
)

# Get KPIs
num_customers = 0
avg_age = 0
num_active = 0
num_fashion = 0
kpi_url = 'https://api-dot-virtual-ego-376415.oa.r.appspot.com/api/v1/kpi'
response = requests.get(kpi_url)
if response.status_code == 200:
    kpis = response.json()
    num_customers = kpis["num_customers"]
    avg_age = kpis["avg_age"]
    num_active = kpis["num_active"]
    num_fashion = kpis["num_fashion"]
else:
    st.write("Failed to retrieve KPIs.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Customers", f"{num_customers}")
kpi2.metric("Average Age", f"{avg_age}")
kpi3.metric("Active Customers", f"{num_active}")
kpi4.metric("Fashion News Subscribers", f"{num_fashion}")

customer_url = 'https://api-dot-virtual-ego-376415.oa.r.appspot.com/api/v1/customer'
params = {
    "active": ",".join(active_lst),
    "fashion": ",".join(fashion_lst),
    "age_min": age_filtered_lst[0],
    "age_max": age_filtered_lst[1]
}
response = requests.get(customer_url, params=params)
if response.status_code == 200:
    customers = response.json()
    df = pd.DataFrame(customers)
    st.write("Customer Data:")
    st.write(df)
else:
    st.write("Failed to retrieve customer data.")
