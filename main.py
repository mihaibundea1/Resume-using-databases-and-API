from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import hashlib


app = Flask(__name__)

# Permite CORS pentru toate originile
CORS(app)

def get_db_connection():
    return pymysql.connect(
        host="localhost",  # Try "localhost" if running locally, otherwise use the container name
        user="admin",
        password="admin_password",
        database="myapp",
        port=3308  # Ensure you're using the correct port exposed by the container (3308 on the host)
    )


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(f"Received login attempt for user: {data.get('username')}")  # Pentru debugging

    username = data.get('username')
    password = data.get('password')

    # Criptarea parolei cu SHA256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Login successful for user: {data.get('username')}")
        return jsonify({"message": "Login successful"}), 200
    else:
        print(f"Login failed for user: {data.get('username')}")
        return jsonify({"message": "Invalid credentials"}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Verifică dacă username-ul există deja
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({"message": "Username already exists"}), 409
    
    # Criptează parola
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        # Inserează noul utilizator
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                      (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        conn.close()
        return jsonify({"message": "Registration failed"}), 
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)