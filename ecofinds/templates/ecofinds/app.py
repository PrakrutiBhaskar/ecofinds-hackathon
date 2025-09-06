from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # This enables Cross-Origin Resource Sharing

# --- Database Configuration ---
# IMPORTANT: Replace with your own MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # <-- PUT YOUR MYSQL PASSWORD HERE
    'database': 'ecofinds'
}

# Function to get a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_-CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# --- API Routes ---

@app.route('/signup', methods=['POST'])
def signup():
    """Handles new user registration."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Hash the password for security
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()

    try:
        # Insert the new user into the 'login' table
        cursor.execute(
            "INSERT INTO login (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409
    except mysql.connector.Error as err:
        return jsonify({'error': f'An error occurred: {err}'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    """Handles user login authentication."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    # dictionary=True lets us access columns by name (e.g., user['password_hash'])
    cursor = conn.cursor(dictionary=True)

    try:
        # Step A: Fetch the user from the database based on the username
        cursor.execute(
            "SELECT id, username, password_hash FROM login WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone() # Get the first result

        # Step B: Check if a user was found AND if the submitted password matches the stored hash
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Password is correct!
            # In a real app, you would create a session here
            return jsonify({'message': 'Login successful'}), 200
        else:
            # Invalid username or password
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return jsonify({'error': 'An error occurred during login'}), 500
    finally:
        cursor.close()
        conn.close()

# --- Run the application ---
if __name__ == '__main__':
    # The server will run on http://127.0.0.1:5000
    app.run(debug=True)
