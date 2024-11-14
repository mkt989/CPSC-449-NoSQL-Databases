from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client.myDatabase  # Replace with your database name
users_collection = db.exampleOneCollection # Replace with your collection name

# Insert a new user into MongoDB
@app.route('/user', methods=['POST'])
def add_user():
    # Get data from the request
    user_data = request.json
    
    # Insert into MongoDB
    users_collection.insert_one({
        "name": user_data['name'],
        "email": user_data['email'],
        "age": user_data['age']
    })
    
    return jsonify({"message": "User added successfully!"}), 201

# Get all users from MongoDB
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in users_collection.find():
        user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
        users.append(user)
    
    return jsonify(users), 200

# Get a single user by name
@app.route('/users/<name>', methods=['GET'])
def get_user_by_name(name):
    user = users_collection.find_one({"name": name})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
