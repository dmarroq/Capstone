import pymongo
import pandas as pd
import numpy as np
from flask import Flask, jsonify
from flask_restx import Api, Namespace, Resource

app = Flask(__name__)
api = Api(app, version='1.0',
          title='Customers API',
          description="""
        API endpoints used to communicate Customers
        between Mongo database and streamlit
        """,
          contact="Diego",
          endpoint="/api/v1")

user = "dmar"
passw = "jJ0i1oGohezcEsGb"
host = "pikachu.eoylcqy.mongodb.net"
database = "kpis"

client = pymongo.MongoClient(
    "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority".format(user, passw, host, database))
db = client[database]

# Get data from MongoDB
def load_data(query):
    try:
        cursor = db.customers.find(query)
        data = pd.DataFrame(list(cursor))
        data = data.drop('_id', axis=1) # drop the MongoDB ObjectId field
    except Exception as e:
        print(e)
        data = pd.DataFrame()
    return data

kpi_ns = Namespace('kpi', description='KPI operations')
customer_ns = Namespace('customer', description='Customer operations')

@kpi_ns.route('/')
class KPI(Resource):
    def get(self):
        customer_df = load_data({})
        num_customers = customer_df["customer_id"].nunique()
        avg_age = np.mean(customer_df["age"])
        num_active = customer_df["club_member_status"].nunique()
        num_fashion = customer_df["fashion_news_frequency"].nunique()

        return {
            "num_customers": num_customers,
            "avg_age": avg_age,
            "num_active": num_active,
            "num_fashion": num_fashion
        }

@customer_ns.route('/')
class Customer(Resource):
    def get(self):
        customer_df = load_data({})
        return customer_df.to_dict('records')
        
api.add_namespace(kpi_ns)
api.add_namespace(customer_ns)

if __name__ == '__main__':
    app.run(debug=True)
