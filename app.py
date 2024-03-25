from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'travel'
}

# Function to establish database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None

# Function to create a new user in the database
def create_user(email, password):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print("Error inserting user into database:", err)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        return False

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if not email or not password or not confirm_password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    if create_user(email, password):
        return jsonify({'message': 'Signup successful'}), 201
    else:
        return jsonify({'error': 'Failed to create user'}), 500

if __name__ == '__main__':
    app.run(debug=True)
