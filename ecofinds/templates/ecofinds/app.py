from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow the frontend to communicate with this backend
CORS(app)

# --- MySQL Configuration ---
# Replace these with your actual MySQL database credentials
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' # or your username
app.config['MYSQL_PASSWORD'] = 'root' # your password
app.config['MYSQL_DB'] = 'ecofinds'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # Returns results as dictionaries

# Initialize MySQL
mysql = MySQL(app)

# --- API Routes ---

@app.route('/signup', methods=['POST'])
def signup():
    """Handles new user registration."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    cursor = mysql.connection.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT * FROM login WHERE username = %s", [username])
    user = cursor.fetchone()
    if user:
        return jsonify({'error': 'Username already exists'}), 409 # 409 Conflict

    # Hash the password for security before storing it
    hashed_password = generate_password_hash(password)

    # Insert the new user into the database
    cursor.execute("INSERT INTO login (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    """Handles user login authentication."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    cursor = mysql.connection.cursor()
    
    # Retrieve user from database
    cursor.execute("SELECT * FROM login WHERE username = %s", [username])
    user = cursor.fetchone()
    cursor.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid username or password'}), 401 # 401 Unauthorized

    # In a real app, you would generate a token (like a JWT) here.
    # For this example, we'll just confirm success.
    return jsonify({'message': 'Login successful'}), 200

# This allows the script to be run directly
if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible from your network
    app.run(host='0.0.0.0', port=5000, debug=True)

