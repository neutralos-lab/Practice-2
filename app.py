from flask import Flask, request, jsonify
from models import User, Method, Session
from encryption_methods import vigenere_encrypt, vigenere_decrypt, caesar_cipher

app = Flask(__name__)

users = {}
methods = {
    1: Method(1, "Vigenere", '{"key": "str"}', "Vigenere encryption method"),
    2: Method(2, "Caesar", '{"shift": "int"}', "Caesar cipher encryption method")
}
sessions = {}

alphabet = "..:()-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    login = data.get('login')
    secret = data.get('secret')
    if not login or not secret or len(login) < 3 or len(login) > 30 or len(secret) < 3 or len(secret) > 30:
        return jsonify({"error": "Invalid login or secret length"}), 400
    if login in users:
        return jsonify({"error": "User already exists"}), 400
    users[login] = User(login, secret)
    return jsonify({"message": "User added successfully"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify([{"login": user.login} for user in users.values()])

@app.route('/methods', methods=['GET'])
def get_methods():
    return jsonify([{"id": method.id, "caption": method.caption, "description": method.description} for method in methods.values()])

@app.route('/sessions', methods=['POST'])
def create_session():
    data = request.json
    login = data.get('login')
    secret = data.get('secret')
    method_id = data.get('method_id')
    data_in = data.get('data_in')
    if login not in users or users[login].secret != secret:
        return jsonify({"error": "Invalid user or secret"}), 403
    if method_id not in methods:
        return jsonify({"error": "Invalid method"}), 400
    method = methods[method_id]
    if method.caption == "Vigenere":
        key = data.get('key')
        data_out = vigenere_encrypt(data_in, key, alphabet)
    elif method.caption == "Caesar":
        shift = data.get('shift')
        data_out = caesar_cipher(data_in, shift, alphabet)
    else:
        return jsonify({"error": "Unknown method"}), 400
    session = Session(login, method_id, data_in, data_out, "completed")
    sessions[session.id] = session
    return jsonify({"session_id": session.id, "data_out": data_out})

@app.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    return jsonify({
        "user_id": session.user_id,
        "method_id": session.method_id,
        "data_in": session.data_in,
        "data_out": session.data_out,
        "status": session.status,
        "created_at": session.created_at.isoformat(),
        "time_op": session.time_op
    })

@app.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    data = request.json
    login = data.get('login')
    secret = data.get('secret')
    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    if session.user_id != login or users[login].secret != secret:
        return jsonify({"error": "Invalid user or secret"}), 403
    del sessions[session_id]
    return jsonify({"message": "Session deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
