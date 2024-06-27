from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import string
import time
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database configuration
DATABASE = "dbname=eod_service user=eod_user password=your_password"
conn = psycopg2.connect(DATABASE)
cur = conn.cursor()

ALPHABET = " ,.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
users = {
    "John": {"secret": "John"}
}
methods = {}
sessions = {}
session_id_counter = 1

def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    return ''.join(ALPHABET[(ALPHABET.index(c) + shift) % len(ALPHABET)] if c in ALPHABET else c for c in text)

def vigenere_cipher(text, key, decrypt=False):
    key = key.upper()
    key_indices = [ALPHABET.index(k) for k in key if k in ALPHABET]
    key_length = len(key_indices)
    result = []
    for i, char in enumerate(text):
        if char in ALPHABET:
            text_index = ALPHABET.index(char)
            key_index = key_indices[i % key_length]
            if decrypt:
                new_index = (text_index - key_index) % len(ALPHABET)
            else:
                new_index = (text_index + key_index) % len(ALPHABET)
            result.append(ALPHABET[new_index])
        else:
            result.append(char)
    return ''.join(result)

def crack_caesar(cipher_text):
    possible_texts = []
    for shift in range(len(ALPHABET)):
        possible_texts.append(caesar_cipher(cipher_text, shift, decrypt=True))
    return possible_texts

def crack_vigenere(cipher_text):
    # Placeholder function for cracking Vigenere
    return ["Not implemented yet"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users', methods=['POST'])
def add_user():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify([{"login": login} for login in users]), 200

@app.route('/users/list', methods=['GET'])
def list_users():
    return render_template('users.html', users=list(users.keys()))

@app.route('/methods', methods=['GET'])
def get_methods():
    return render_template('methods.html', methods=list(methods.values()))

@app.route('/encrypt', methods=['GET'])
def encrypt_form():
    method_id = request.args.get('method_id')
    method = methods.get(method_id)
    if method:
        return render_template('encrypt.html', method=method, users=list(users.keys()))
    else:
        return redirect(url_for('get_methods'))

@app.route('/encrypt', methods=['POST'])
def encrypt():
    global session_id_counter
    data = request.form
    user_id = data['user_id']
    method_id = data['method_id']
    action = data['action']
    data_in = data['data_in']
    params = {}
    if user_id in users and method_id in methods and len(data_in) <= 1000:
        data_in_filtered = ''.join([c for c in data_in.upper() if c in ALPHABET])
        start_time = time.time()
        if methods[method_id]['caption'] == 'Caesar':
            shift = int(data['shift'])
            params['shift'] = shift
            data_out = caesar_cipher(data_in_filtered, shift, decrypt=(action == 'decrypt'))
        elif methods[method_id]['caption'] == 'Vigenere':
            key = data['key']
            params['key'] = key
            data_out = vigenere_cipher(data_in_filtered, key, decrypt=(action == 'decrypt'))
        else:
            return jsonify({"message": "Invalid method"}), 400
        end_time = time.time()
        session = {
            'id': session_id_counter,
            'user_id': user_id,
            'method_id': method_id,
            'data_in': data_in,
            'params': params,
            'data_out': data_out,
            'status': 'completed',
            'created_at': datetime.now().isoformat(),
            'time_op': end_time - start_time
        }
        sessions[session_id_counter] = session
        session_id_counter += 1
        return redirect(url_for('get_sessions'))
    else:
        return jsonify({"message": "Invalid input"}), 400

@app.route('/sessions', methods=['GET'])
def get_sessions():
    return render_template('sessions.html', sessions=sessions.values())

@app.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    session = sessions.get(session_id)
    if session:
        return render_template('session.html', session=session)
    else:
        return jsonify({"message": "Session not found"}), 404

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    data = request.form
    secret = data['secret']
    session = sessions.get(session_id)
    if session and users[session['user_id']]['secret'] == secret:
        del sessions[session_id]
        return jsonify({"message": "Success"}), 200
    else:
        return jsonify({"message": "Error"}), 400

@app.route('/sessions/<int:session_id>/delete', methods=['POST'])
def delete_session_form(session_id):
    session = sessions.get(session_id)
    if session:
        secret = request.form['secret']
        user_id = session['user_id']
        if users[user_id]['secret'] == secret:
            del sessions[session_id]
            return redirect(url_for('get_sessions'))
        else:
            return render_template('session.html', session=session, error="Invalid Pass")
    else:
        return jsonify({"message": "Session not found"}), 404

# Database initialization
def init_db():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()

@app.route('/users/add', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
    except psycopg2.Error as e:
        return jsonify({"message": "User already exists"}), 400
    return jsonify({"message": "User added successfully"}), 200

@app.route('/users/delete', methods=['POST'])
def delete_user():
    username = request.form['username']
    password = request.form['password']
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user and check_password_hash(user[0], password):
        cur.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 400

@app.route('/users/update_password', methods=['POST'])
def update_password():
    username = request.form['username']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user and check_password_hash(user[0], old_password):
        hashed_password = generate_password_hash(new_password)
        cur.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, username))
        conn.commit()
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 400

@app.route('/crack', methods=['POST'])
def crack_cipher():
    data = request.form
    method_id = data['method_id']
    cipher_text = data['cipher_text']
    if method_id == '1':  # Caesar
        possible_texts = crack_caesar(cipher_text)
    elif method_id == '2':  # Vigenere
        possible_texts = crack_vigenere(cipher_text)
    else:
        return jsonify({"message": "Invalid method"}), 400
    return render_template('crack_results.html', results=possible_texts)

init_db()

if __name__ == '__main__':
    methods['1'] = {'id': '1', 'caption': 'Caesar', 'json_params': '{"shift": "int"}',
                    'description': ''}
    methods['2'] = {'id': '2', 'caption': 'Vigenere', 'json_params': '{"key": "str"}',
                    'description': ''}
    app.run(debug=True)
