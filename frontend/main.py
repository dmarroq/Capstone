import numpy as np
import pandas as pd
import requests
import streamlit as st

headers = {'Accept': 'application/json'}

api_url = "https://api-dot-virtual-ego-376415.oa.r.appspot.com/api/v1"
customers_url = "/customers"

def make_request(main_url, service_url):
    response = requests.get(f"{main_url}{service_url}", headers=headers)
    response_json = response.json()
    return response_json

def load_json_to_dataframe(response_json):
    target_json = response_json["result"]
    try:
        df = pd.json_normalize(target_json)
    except Exception as e:
        print(e)
    return df

def load_data(main_url, service_url):
    response_json = make_request(main_url, service_url)
    df = load_json_to_dataframe(response_json)
    return response_json, df

response_json, customers_df = load_data(api_url, customers_url)

st.json(response_json)
st.dataframe(customers_df)
