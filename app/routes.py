"""
Module: order routes

This module contains routes to manage orders using Flask.
Routes include:
- Creating a new order
- Getting order details by ID
- Updating order status by ID
- Retrieving orders by user ID
- Cancelling an order by ID
- Retrieving orders by status
- Calculating the total price of an order
"""

from flask import jsonify, request
from app.services import OrderService, OrderItemService
from app import app

order_service = OrderService()
order_item_service = OrderItemService()

@app.route('/health', methods=['GET'])
def health_check():
    """health check returning a success status"""
    application_status = {
        'status': 'healthy'
    }
    return jsonify(application_status), 200

@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order."""
    try:
        order_data = request.json
        if not order_data:
            return jsonify({"error": "No data provided"}), 400
        
        order_id = order_service.create_new_order(order_data)
        return jsonify({"message": "New order created", "order_id": order_id}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    """Route to retrieve all orders."""
    try:
        orders = order_service.get_all_orders()
        return jsonify(orders), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    """Get details of a specific order by order ID."""
    try:
        order = order_service.get_order_by_id(order_id)
        if order:
            return jsonify(order), 200
        return jsonify({"message": "Order not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id):
    """Update the status of an order by order ID."""
    try:
        status_data = request.json
        if not status_data:
            return jsonify({"error": "No data provided"}), 400
        
        success = order_service.update_order_status(order_id, status_data)
        if success:
            return jsonify({"message": "Order status updated"}), 200
        return jsonify({"message": "Order not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    """Get orders associated with a specific user."""
    try:
        orders = order_service.get_orders_by_user(user_id)
        return jsonify(orders), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    """Cancel an order by order ID."""
    try:
        success = order_service.cancel_order(order_id)
        if success:
            return jsonify({"message": "Order canceled"}), 200
        return jsonify({"message": "Order not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/status/<string:status>', methods=['GET'])
def get_orders_by_status(status):
    """Get orders by their status."""
    try:
        orders = order_service.get_orders_by_status(status)
        return jsonify(orders), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/calculate-total', methods=['POST'])
def calculate_order_total():
    """Calculate the total price of an order."""
    try:
        order_items = request.json.get('order_items')
        if not order_items:
            return jsonify({"error": "No order items provided"}), 400
        
        total_price = order_service.calculate_order_total(order_items)
        return jsonify({"total_price": total_price}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/<int:order_id>/items', methods=['POST'])
def create_order_item(order_id):
    """Create a new order item for a specific order."""
    try:
        item_data = request.json
        if not item_data:
            return jsonify({"error": "No data provided"}), 400
        
        item_id = order_item_service.create_order_item(order_id, item_data)
        return jsonify({"message": "New order item created", "item_id": item_id}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    """Get all order items for a specific order."""
    try:
        items = order_item_service.get_order_items(order_id)
        return jsonify(items), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/items/<int:item_id>', methods=['PATCH'])
def update_order_item(item_id):
    """Update an order item by item ID."""
    try:
        updated_data = request.json
        if not updated_data:
            return jsonify({"error": "No data provided"}), 400
        
        success = order_item_service.update_order_item(item_id, updated_data)
        if success:
            return jsonify({"message": "Order item updated"}), 200
        return jsonify({"message": "Order item not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/items/<int:item_id>', methods=['DELETE'])
def delete_order_item(item_id):
    """Delete an order item by item ID."""
    try:
        success = order_item_service.delete_order_item(item_id)
        if success:
            return jsonify({"message": "Order item deleted"}), 200
        return jsonify({"message": "Order item not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
