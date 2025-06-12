from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
products = {}

@app.route('/')
def health():
    return 'Product Service is up and running!'

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product_id = str(uuid.uuid4())
    products[product_id] = {'id': product_id, 'name': data['name']}
    return jsonify(products[product_id]), 201

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
