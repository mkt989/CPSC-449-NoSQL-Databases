from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Set up the MongoDB client
client = MongoClient('mongodb://localhost:27017/')  # Adjust your MongoDB URI accordingly
db = client['myDatabase']  # Replace with your database name
collection = db['exampleThreeCollection1']  # Replace with your collection name

# Endpoint to get students with filters
@app.route('/students', methods=['GET'])
def get_students():
    # Extract query parameters for grade filtering
    min_grade = request.args.get('min_grade', type=float)  # Minimum grade for filter
    max_grade = request.args.get('max_grade', type=float)  # Maximum grade for filter
    sort_order = request.args.get('sort', default='asc', type=str)  # Sort order

    print(min_grade,"min grade")
    query = {'grade':{}}
    if min_grade is not None:
        query['grade']['$gte'] = min_grade  # Greater than min_grade
    if max_grade is not None:
        query['grade']['$lte']= max_grade  # Less than max_grade

    # Determine sort direction
    sort_direction = 1 if sort_order == 'asc' else -1

    try:
        # Find matching documents
        students = list(collection.find(query).sort('grade', sort_direction))
        count = len(students)  # Count of documents that match the query

        # Exclude the _id field from the result for cleaner output
        students = [{**student, '_id': str(student['_id'])} for student in students]

        return jsonify({
            'count': count,
            'students': students
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to add a new student
@app.route('/students', methods=['POST'])
def add_student():
    try:
        # Get the student details from the request body
        student_data = request.get_json()

        # Validate the student data (basic example)
        if not student_data or 'name' not in student_data or 'grade' not in student_data:
            return jsonify({'error': 'Invalid data'}), 400

        # Insert the new student document into the collection
        result = collection.insert_one(student_data)

        # Return success message with the inserted student ID
        return jsonify({
            'message': 'Student added successfully',
            'student_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
