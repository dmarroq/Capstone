import pymongo
from flask import Flask, request, jsonify
from flask_restx import Api, Namespace, Resource
from bson import ObjectId


user = "dmar"
passw = "jJ0i1oGohezcEsGb"
host = "pikachu.eoylcqy.mongodb.net"
database = "kpis"

app = Flask(__name__)

# Create api v1
api = Api(app, version='1.0',
          title='Customers API',
          description="""
        API endpoints used to communicate Customers
        between Mongo database and streamlit
        """,
          contact="Diego",
          endpoint="/api/v1")

# Define the connect and disconnect
def connect():
    client = pymongo.MongoClient(
    "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority"
    .format(user, passw, host, database))
    conn = client[database]
    return conn, client

def disconnect(conn, client):
    client.close()


# --------------------------

# Get API and Flask stuff
customers = Namespace('customers', path='/api/v1')
api.add_namespace(customers)

@customers.route("/customers")
class get_all_customers(Resource):
    def get(self):
        conn, client = connect()
        result = list(conn.customers.find())
        # Convert ObjectId to string
        for customer in result:
            customer['_id'] = str(customer['_id'])
        disconnect(conn, client)
        return jsonify({'result': result})

@customers.route("/customers/<string:_id>")
@customers.doc(params={'_id': 'The ID of the customer'})
class get_select_customer(Resource):
    def get(self, _id):
        conn, client = connect()
        result = conn.customers.find_one({"_id": ObjectId(_id)})
        # Convert ObjectId to string
        result['_id'] = str(result['_id'])
        disconnect(conn, client)
        return jsonify({'result': result})

# 127.0.0.1/hello
@api.route("/hello")
class hello(Resource):
    def get(self):
        return {"content": "Hello from Flask"}

# --------------------------

if __name__ == '__main__':
    app.run(debug=True)
