from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)
orders = {}

USER_SERVICE_URL = 'http://user-service:5001'
PRODUCT_SERVICE_URL = 'http://product-service:5002'

@app.route('/')
def health():
    return 'Order Service is up and running!'

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data['user_id']
    product_id = data['product_id']

    # Перевірка користувача
    user_res = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    if user_res.status_code != 200:
        return jsonify({'error': 'User not found'}), 404

    # Перевірка продукту
    product_res = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if product_res.status_code != 200:
        return jsonify({'error': 'Product not found'}), 404

    # Створення замовлення
    order_id = str(uuid.uuid4())
    orders[order_id] = {'id': order_id, 'user_id': user_id, 'product_id': product_id}
    return jsonify(orders[order_id]), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
