from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
users = {}

@app.route('/')
def health():
    return 'User Service is up and running!'

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = str(uuid.uuid4())
    users[user_id] = {'id': user_id, 'name': data['name']}
    return jsonify(users[user_id]), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
