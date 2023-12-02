"""
This module contains routes for managing orders.

Endpoints:
- GET /health: Health check endpoint returning a success status.
- POST /orders: Create a new order.
- GET /orders: Retrieve all orders.
- GET /orders/<int:order_id>: Get details of a specific order by order ID.
- PATCH /orders/<int:order_id>: Update the status of an order by order ID.
- GET /orders/user/<int:user_id>: Get orders associated with a specific user.
- DELETE /orders/<int:order_id>: Cancel an order by order ID.
- GET /orders/status/<string:status>: Get orders by their status.
- GET /orders/<int:order_id>/items: Get all order items for a specific order.
"""
import logging
from flask import jsonify, request
from app.services import OrderService, OrderItemService
from app import app
from app.models import StatusEnum

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

        required_fields = ['user_id', 'status', 'items']
        for field in required_fields:
            if field not in order_data:
                return jsonify({"error": f"Missing '{field}' field"}), 400

        status = order_data['status'].lower()

        valid_statuses = [
            StatusEnum.PENDING.value,
            StatusEnum.PROCESSING.value,
            StatusEnum.SHIPPED.value
        ]

        if status not in valid_statuses:
            return jsonify({"error": "Invalid status provided"}), 400

        order_id = order_service.create_new_order(order_data)
        return jsonify({"message": "New order created", "order_id": order_id}), 201

    except KeyError as exception:
        return jsonify({"error": f"Missing key: {str(exception)}"}), 400

    except Exception as exception:
        logging.error(f"Error processing order creation: {str(exception)}")
        return jsonify({"error": "An error occurred while processing the request"}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    """Route to retrieve all orders."""
    try:
        orders = order_service.get_all_orders()
        return jsonify(orders), 200
    except Exception as exception:
        error_message = str(exception)
        return jsonify({"error": error_message}), 500

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    """Get details of a specific order by order ID."""
    try:
        order = order_service.get_order_by_id(order_id)
        if order:
            return jsonify(order), 200
        return jsonify({"message": "Order not found"}), 404

    except Exception as exception:
        return jsonify({"error": str(exception)}), 500

@app.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id):
    """Update the status of an order by order ID."""
    try:
        status_data = request.json
        if not status_data:
            return jsonify({"error": "No data provided"}), 400

        new_status = status_data.get('status').lower()

        if not new_status:
            return jsonify({"error": "Incomplete data provided"}), 400

        valid_statuses = [
            StatusEnum.PENDING.value,
            StatusEnum.PROCESSING.value,
            StatusEnum.SHIPPED.value
        ]

        if new_status not in valid_statuses:
            return jsonify({"error": "Invalid status provided"}), 400

        success = order_service.update_order_status(order_id, status_data)
        if success:
            return jsonify({"message": "Order status updated"}), 200
        return jsonify({"message": "Order not found"}), 404

    except ValueError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as exception:
        return jsonify({"error": str(exception)}), 500

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    """Get orders associated with a specific user."""
    try:
        orders = order_service.get_orders_by_user(user_id)
        return jsonify(orders), 200

    except Exception as exception:
        logging.exception("Error: %s", str(exception))
        return jsonify({"error": "An error occurred while processing the request"}), 500

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    """Cancel an order by order ID."""
    try:
        success = order_service.cancel_order(order_id)
        if success:
            return jsonify({"message": "Order canceled"}), 200
        return jsonify({"message": "Order not found"}), 404

    except Exception as exception:
        return jsonify({"error": str(exception)}), 500

@app.route('/orders/status/<string:status>', methods=['GET'])
def get_orders_by_status(status):
    """Get orders by their status."""
    try:
        orders = order_service.get_orders_by_status(status)
        return jsonify(orders), 200

    except Exception as exception:
        return jsonify({"error": str(exception)}), 500

@app.route('/orders/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    """Get all order items for a specific order."""
    try:
        items = order_item_service.get_order_items(order_id)
        return jsonify(items), 200

    except Exception as exception:
        return jsonify({"error": str(exception)}), 500
