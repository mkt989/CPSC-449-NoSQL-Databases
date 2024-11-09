from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient("mongodb://127.0.0.1:27017/")

# Function to check MongoDB connection
def check_mongo_connection():
    try:
        # The ping command is used to check if the MongoDB server is available
        client.admin.command('ping')
        return True
    except ConnectionFailure:
        return False

# Route to test MongoDB connection
@app.route('/check_mongo_connection', methods=['GET'])
def check_connection():
    if check_mongo_connection():
        return jsonify({"message": "MongoDB connection successful"}), 200
    else:
        return jsonify({"message": "MongoDB connection failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
