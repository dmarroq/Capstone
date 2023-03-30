import requests
import pandas as pd
import streamlit as st
from requests.auth import HTTPBasicAuth

# API endpoint
customers_url = "https://api-dot-virtual-ego-376415.oa.r.appspot.com/api/v1/customers"
transactions_url = "http://api-dot-virtual-ego-376415.oa.r.appspot.com/api/v1/transactions"
articles_url = "http://api-dot-virtual-ego-376415.oa.r.appspot.com/api/v1/articles"

users = {
    "api_key_1": "user1",
    "api_key_2": "user2"
}
# Verify the password entered by the user matches the one in the dictionary
def verify_user(username, password):
    if username in users and password == users[username]:
        return True
    return False

# st.image("/home/d_marroquin/Capstone/frontend/H&MLogo.jpg", width=200)

def run_app():
    st.title("H&M Dashboard")
    st.markdown("Welcome to the H&M dashboard.")
    # Get data from API
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.button("Login")
    if login:
        if verify_user(username, password):
            response_customers = requests.get(customers_url, auth=HTTPBasicAuth(username, password))
            response_transactions = requests.get(transactions_url, auth=HTTPBasicAuth(username, password))
            response_articles = requests.get(articles_url, auth=HTTPBasicAuth(username, password))
            data_customers = response_customers.json()
            customer_df = pd.DataFrame(data_customers)
            data_transactions = response_transactions.json()
            transactions_df = pd.DataFrame(data_transactions)
            data_articles = response_articles.json()
            articles_df = pd.DataFrame(data_articles)
            logged_in = True
        else:
            st.warning("Invalid username or password")
            logged_in = False
    else:
        logged_in = False

    # Display the login form if the user is not logged in
    if not logged_in:
        return

    # ---------------------------------------------------

    # Create the Streamlit app
    st.title("H&M KPIs")


    # Display the data_customers
    st.title("H&M Customers")
    st.dataframe(customer_df)
    # # Display the data_transactions
    st.title("H&M Transactions")
    st.dataframe(transactions_df)
    # # Display the data_articles
    st.title("H&M Articles")
    st.dataframe(articles_df)

    # ---------------------------------------------------
    #######################################################
    #################### FILTERS ##########################
    #######################################################


    # Get unique values for filters
    # Customer filters
    active_lst = customer_df["club_member_status"].unique()
    age_lst = customer_df["age"].to_list()

    # Transactions filters
    sales_channel_lst = transactions_df["sales_channel_id"].unique()
    price_lst = transactions_df["price"].to_list()

    # Articles filters
    product_type_lst = articles_df["product_type_no"].unique()

    # Create sidebar for filters
    st.sidebar.write("FILTERS")

    # Customers
    active_filtered_lst = st.sidebar.multiselect(
        label="Customers Active",
        options=active_lst,
        default=active_lst,
        key=None
    )
    st.sidebar.write('Active selected:', active_filtered_lst)

    age_filtered_lst = st.sidebar.slider(
        'Select a range of ages',
        0, 100, (20, 80)
    )

    st.sidebar.write('Ages range selected:', age_filtered_lst)

    # Transactions

    filtered_sales_channel_lst = st.sidebar.multiselect(
        label="Transactions Sales Channels",
        options=sales_channel_lst,
        default=sales_channel_lst,
        key=None
    )
    st.sidebar.write('Sales channels selected:', filtered_sales_channel_lst)

    filtered_price_lst = st.sidebar.slider(
        'Select a range of prices',
        0.0, 1.0, (0.0, 0.4)
    )

    st.sidebar.write('Price range selected:', filtered_price_lst)

    # Articles

    filtered_product_type_lst = st.sidebar.multiselect(
        label="Product Types",
        options=product_type_lst,
        default=product_type_lst,
        key=None
    )
    st.sidebar.write('Product types selected:', filtered_product_type_lst)

    # Make filters work
    active_filtered_lst = [f"^{active}$" for active in active_filtered_lst]

    if len(active_filtered_lst) == 0:
        active_filtered_lst = ".*"
    else:
        active_filtered_lst = "|".join(active_filtered_lst)

    customer_df = customer_df[
        (customer_df["club_member_status"].str.contains(active_filtered_lst, case=False)) &
        (customer_df["age"].between(age_filtered_lst[0], age_filtered_lst[1]))
    ]

    filtered_transactions_df = transactions_df[
        (transactions_df["sales_channel_id"].isin(filtered_sales_channel_lst)) &
        (transactions_df["price"].between(filtered_price_lst[0], filtered_price_lst[1]))
    ]

    filtered_articles_df = articles_df[
        articles_df["product_type_no"].isin(filtered_product_type_lst)
    ]

    # ---------------------------------------------------
    #######################################################
    ################## CUSTOMERS ##########################
    #######################################################

    # Get KPIs
    num_customers = customer_df["customer_id"].nunique()
    avg_age = customer_df["age"].mean()
    num_active = customer_df["club_member_status"].nunique()

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        label="Number of different customers",
        value=num_customers,
        delta=num_customers,
    )

    kpi2.metric(
        label="Number of different statuses",
        value=num_active,
        delta=num_active,
    )

    kpi3.metric(
        label="Average age",
        value=round(avg_age, 2),
        delta=-10 + avg_age,
    )

    # Get visuals
    st.write(customer_df.groupby(["age"])["customer_id"].count())

    st.bar_chart(customer_df.groupby(["age"])["customer_id"].count())

    st.bar_chart(customer_df.groupby(["club_member_status"])["customer_id"].count())


    # ---------------------------------------------------
    ##########################################################
    ################## TRANSACTIONS ##########################
    ##########################################################

    st.title("H&M Transactions")
    st.dataframe(filtered_transactions_df)

    # Get KPIs
    num_transactions = filtered_transactions_df["article_id"].nunique()
    total_sales = filtered_transactions_df["price"].sum()

    kpi1, kpi2 = st.columns(2)

    kpi1.metric(
        label="Number of transactions",
        value=num_transactions,
        delta=num_transactions,
    )

    kpi2.metric(
        label="Total income",
        value=total_sales,
        delta=total_sales,
    )

    # Get visuals
    st.bar_chart(filtered_transactions_df.groupby(["sales_channel_id"])["article_id"].count())

    st.line_chart(filtered_transactions_df.groupby(["article_id"])["price"].sum())


    # ---------------------------------------------------
    ##########################################################
    ##################### ARTICLES ##########################
    ##########################################################

    st.title("H&M Articles")
    st.dataframe(filtered_articles_df)

    # Get KPIs
    num_product_types = filtered_articles_df["product_type_no"].nunique()

    kpi1 = st.columns(1)

    kpi1[0].metric(
        label="Number of Product Types",
        value=num_product_types,
        delta=num_product_types,
    )

    # Get visuals
    st.bar_chart(filtered_articles_df.groupby(["product_type_no"])["article_id"].count())
    
if __name__ == '__main__':
    run_app()
