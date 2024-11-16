from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Set up the MongoDB client
client = MongoClient('mongodb://localhost:27017/')  # Adjust your MongoDB URI accordingly
db = client['myDatabase']  # Replace with your database name
collection = db['exampleTwoCollection']  # Replace with your collection name

@app.route('/students', methods=['POST'])
def add_students():
    # Retrieve JSON data from the request
    data = request.json
    if not data or not isinstance(data, list):
        return jsonify({'error': 'Invalid input. Please provide a list of students.'}), 400

    try:
        # Insert multiple documents into the collection
        result = collection.insert_many(data)
        
        # Return the inserted IDs as a response
        return jsonify({'inserted_ids': str(result.inserted_ids)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/students', methods=['GET'])
def get_students():
    try:
        # Retrieve all student documents from the collection
        students = list(collection.find({}, {'_id': 0}))  # Exclude the _id field for cleaner output
        
        # Return the list of students as a JSON response
        return jsonify(students), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
