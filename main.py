from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)

# Permite CORS pentru toate originile
CORS(app)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="admin",
        password="admin_password",
        database="myapp"
    )

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
