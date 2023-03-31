import pymongo
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, Namespace
from flask_httpauth import HTTPBasicAuth

# Load data from MongoDB

user = "dmar"
passw = "jJ0i1oGohezcEsGb"
host = "pikachu.eoylcqy.mongodb.net"
database = "kpis"

client = pymongo.MongoClient(
    "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority"
    .format(user, passw, host, database))
db = client[database]

app = Flask(__name__)
api = Api(app, version='1.0',
          title='H&M API',
          description="""
        API endpoints used to communicate H&M
        between Mongo database and streamlit
        """,
          contact="Diego",
          endpoint="/api/v1")

# Define valid API keys
api_keys = {
    "api_key_1": "api_key_1",
    "api_key_2": "user2"
}

users_passwords = {
    "user1": "password1",
    "user2": "password2"
}


# Create HTTPBasicAuth object
auth = HTTPBasicAuth()

# Verify the API key entered by the user matches the one in the dictionary
@auth.verify_password
def verify_api_key(api_key, password):
    if api_key in api_keys and api_keys[api_key] == password:
        return api_key

# Require authentication for certain routes
# @auth.login_required
def get_customer_data(query):
    try:
        cursor = db.customers.find(query).limit(1000)
        data = pd.DataFrame(list(cursor))
        data = data.drop('_id', axis=1) # drop the MongoDB ObjectId field
    except Exception as e:
        print(e)
        data = pd.DataFrame()
    return data

# @auth.login_required
def load_transaction_data(query):
    try:
        cursor = db.transactions.find(query).limit(1000)
        data = pd.DataFrame(list(cursor))
        data = data.drop('_id', axis=1) # drop the MongoDB ObjectId field
    except Exception as e:
        print(e)
        data = pd.DataFrame()
    return data

# @auth.login_required
def load_articles_data(query):
    try:
        cursor = db.articles.find(query).limit(1000)
        data = pd.DataFrame(list(cursor))
        data = data.drop('_id', axis=1) # drop the MongoDB ObjectId field
    except Exception as e:
        print(e)
        data = pd.DataFrame()
    return data

# ------------------------

# Namespaces

# Get customer stuff

customer_ns = Namespace('customer', description='Customer data', path='/api/v1')
api.add_namespace(customer_ns)

@customer_ns.route('/customers')
class Customers(Resource):
    # @auth.login_required
    @api.expect(api.parser().add_argument('api_key', location='headers', required=True))
    def get(self):
        api_key = request.headers.get('api_key')
        if not verify_api_key(api_key, api_keys.get(api_key)):
            return {'message': 'Invalid API key'}, 401
        query = request.args.get('query')
        customer_df = get_customer_data(query)
        return jsonify(customer_df.to_dict(orient='records'))
    
# Get transactions stuff

transactions_ns = Namespace('transactions', description='Transactions', path='/api/v1')
api.add_namespace(transactions_ns)

@transactions_ns.route('/transactions')
class Transactions(Resource):
    # @auth.login_required
    @api.expect(api.parser().add_argument('api_key', location='headers', required=True))
    def get(self):
        api_key = request.headers.get('api_key')
        if not verify_api_key(api_key, api_keys.get(api_key)):
            return {'message': 'Invalid API key'}, 401
        query = request.args.get('query')
        transactions_df = load_transaction_data(query)
        return jsonify(transactions_df.to_dict(orient='records'))
    
articles_ns = Namespace('articles', description='Articles', path='/api/v1')
api.add_namespace(articles_ns)

@articles_ns.route('/articles')
class Articles(Resource):
    # @auth.login_required
    @api.expect(api.parser().add_argument('api_key', location='headers', required=True))
    def get(self):
        api_key = request.headers.get('api_key')
        if not verify_api_key(api_key, api_keys.get(api_key)):
            return {'message': 'Invalid API key'}, 401
        query = request.args.get('query')
        articles_df = load_articles_data(query)
        return jsonify(articles_df.to_dict(orient='records'))
    
if __name__ == '__main__':
    app.run(debug=True)

