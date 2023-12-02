FIx this problem

```
(venv) stephen:order-service$ python -m unittest discover
.F/home/stephen/Projects/order-service/app/services.py:116: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  order = Order.query.get(order_id)
....F..
======================================================================
FAIL: test_create_order (tests.test_endpoints.TestOrderEndpoints)
Test creating a new order
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephen/Projects/order-service/tests/test_endpoints.py", line 46, in test_create_order
    self.assertEqual(response.status_code, 201)
AssertionError: 500 != 201

======================================================================
FAIL: test_get_orders_by_user (tests.test_endpoints.TestOrderEndpoints)
Test retrieving orders associated with a specific user
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephen/Projects/order-service/tests/test_endpoints.py", line 130, in test_get_orders_by_user
    self.assertEqual(response.status_code, 200)
AssertionError: 500 != 200

----------------------------------------------------------------------
Ran 9 tests in 6.526s

FAILED (failures=2)
```

```
import unittest
from app import app, db
from app.models import Order, OrderItem, StatusEnum
import json

class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        """ Set up test environment """
        self.app = app.test_client()

        with app.app_context():
            app.config['TESTING'] = True
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            db.create_all()

    def tearDown(self):
        """ Remove test environment """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_check(self):
        """ Test the health check endpoint """
        with app.app_context():
            response = self.app.get('/health')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'healthy')

    def test_create_order(self):
        """ Test creating a new order """
        with app.app_context():
            order_data = {
                'user_id': 1,
                'status': 'pending',
                'items': [
                    {'product_id': 1, 'quantity': 2, 'price': 10.0},
                    {'product_id': 2, 'quantity': 1, 'price': 20.0}
                ]
            }

            response = self.app.post('/orders', json=order_data)
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['order_id'])

            # Retrieve the created order from the database and check if it exists
            created_order = db.session.get(Order, data['order_id'])
            self.assertIsNotNone(created_order)
            self.assertEqual(created_order.user_id, order_data['user_id'])
            self.assertEqual(created_order.status, StatusEnum.PENDING)

            # Check the associated order items
            self.assertEqual(created_order.items.count(), 2)

    def test_get_orders(self):
        """ Test retrieving all orders """
        with app.app_context():
            # Assuming some orders exist in the database
            # Create sample orders for testing
            order1 = Order(user_id=1, total_price=50.0, status=StatusEnum.SHIPPED)
            order2 = Order(user_id=2, total_price=30.0, status=StatusEnum.PENDING)
            db.session.add(order1)
            db.session.add(order2)
            db.session.commit()

            response = self.app.get('/orders')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)  # Assuming there are orders in the database

    def test_get_order_details(self):
        """ Test retrieving details of a specific order by order ID """
        with app.app_context():
            # Assuming an order exists in the database
            # Create a sample order for testing
            order = Order(user_id=1, total_price=50.0, status=StatusEnum.SHIPPED)
            db.session.add(order)
            db.session.commit()

            order_id = order.id

            response = self.app.get(f'/orders/{order_id}')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['id'], order_id)

    def test_update_order_status(self):
        """ Test updating the status of an order by order ID """
        with app.app_context():
            # Assuming an order exists in the database
            # Create a sample order for testing
            order = Order(user_id=1, total_price=50.0, status=StatusEnum.PENDING)
            db.session.add(order)
            db.session.commit()

            order_id = order.id
            new_status_data = {'status': 'shipped'}

            response = self.app.patch(f'/orders/{order_id}', json=new_status_data)
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Order status updated')

            # Retrieve the updated order from the database and check if status is updated
            updated_order = db.session.get(Order, order_id)
            self.assertEqual(updated_order.status, StatusEnum.SHIPPED)

    def test_get_orders_by_user(self):
        """ Test retrieving orders associated with a specific user """
        with app.app_context():
            # Assuming orders associated with a specific user exist in the database
            # Create sample orders associated with a user for testing
            user_id = 1
            order1 = Order(user_id=user_id, total_price=50.0, status=StatusEnum.SHIPPED)
            order2 = Order(user_id=user_id, total_price=30.0, status=StatusEnum.PENDING)
            db.session.add(order1)
            db.session.add(order2)
            db.session.commit()

            response = self.app.get(f'/orders/user/{user_id}')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)

    def test_cancel_order(self):
        """ Test canceling an order by order ID """
        with app.app_context():
            # Assuming an order exists in the database
            # Create a sample order for testing
            order = Order(user_id=1, total_price=50.0, status=StatusEnum.PENDING)
            db.session.add(order)
            db.session.commit()

            order_id = order.id

            response = self.app.delete(f'/orders/{order_id}')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Order canceled')

            # Check if the order is deleted from the database
            deleted_order = db.session.get(Order, order_id)
            self.assertIsNone(deleted_order)

    def test_get_orders_by_status(self):
        """ Test retrieving orders by their status """
        with app.app_context():
            # Assuming orders with a specific status exist in the database
            # Create sample orders with a specific status for testing
            status = StatusEnum.PENDING.value
            order1 = Order(user_id=1, total_price=50.0, status=status)
            order2 = Order(user_id=2, total_price=30.0, status=status)
            db.session.add(order1)
            db.session.add(order2)
            db.session.commit()

            response = self.app.get(f'/orders/status/{status}')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)

    def test_get_order_items(self):
        """ Test retrieving all order items for a specific order """
        with app.app_context():
            # Assuming order items for a specific order exist in the database
            # Create sample order items for a specific order for testing
            order_id = 1
            item1 = OrderItem(order_id=order_id, product_id=1, quantity=2, price=10.0)
            item2 = OrderItem(order_id=order_id, product_id=2, quantity=1, price=20.0)
            db.session.add(item1)
            db.session.add(item2)
            db.session.commit()

            response = self.app.get(f'/orders/{order_id}/items')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()


```

routes:
```
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

        if status not in [StatusEnum.PENDING.value, StatusEnum.PROCESSING.value, StatusEnum.SHIPPED.value]:
            return jsonify({"error": "Invalid status provided"}), 400


        order_id = order_service.create_new_order(order_data)
        return jsonify({"message": "New order created", "order_id": order_id}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    """Route to retrieve all orders."""
    try:
        orders = order_service.get_all_orders()
        print(orders)
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

        new_status = status_data.get('status').lower()

        if not new_status:
            return jsonify({"error": "Incomplete data provided"}), 400

        if new_status not in [StatusEnum.PENDING.value, StatusEnum.PROCESSING.value, StatusEnum.SHIPPED.value]:
            return jsonify({"error": "Invalid status provided"}), 400

        success = order_service.update_order_status(order_id, status_data)
        if success:
            return jsonify({"message": "Order status updated"}), 200
        return jsonify({"message": "Order not found"}), 404

    except ValueError:
        return jsonify({"error": "Invalid JSON format"}), 400
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

@app.route('/orders/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    """Get all order items for a specific order."""
    try:
        items = order_item_service.get_order_items(order_id)
        return jsonify(items), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


```


```
"""
Module containing database models for orders and order items.
"""

from datetime import datetime
from enum import Enum as PyEnum
from app import db

class StatusEnum(PyEnum):
    """Enumerates the status options for orders."""
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'

class Order(db.Model):
    """
    Represents an order in the database.
    """

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float)
    items = db.relationship(
                'OrderItem',
                backref='order',
                cascade='all,delete-orphan',
                lazy='dynamic'
            )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.PENDING)

    def __repr__(self):
        return f"<Order id={self.id}, user_id={self.user_id}, " \
               f"total_price={self.total_price}, status='{self.status}'>"


class OrderItem(db.Model):
    """
    Represents an item within an order in the database.
    """

    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<OrderItem id={self.id}, order_id={self.order_id}, " \
               f"product_id={self.product_id}, quantity={self.quantity}, " \
               f"price={self.price}>"

```
services:
```
"""
The 'OrderService' module manages operations related to orders within the application.
It includes functionalities for creating, retrieving, updating, and canceling orders,
as well as calculating order totals and fetching orders based on specific criteria.
"""
from datetime import datetime
from app import db
from app.models import Order, OrderItem

class OrderService:
    """
    A class handling various operations related to orders.
    """

    def __init__(self):
        """
        Initializes the OrderService.
        """
        pass

    def create_new_order(self, order_data):
        """
        Creates a new order.

        Args:
        - order_data (dict): Data for the new order.

        Returns:
        - int: The ID of the created order.

        Raises:
        - Exception: If an error occurs during order creation.
        """
        try:
            user_id = order_data.get('user_id')
            status = order_data.get('status')

            items_data = order_data.get('items', [])

            # Create the Order object
            new_order = Order(
                user_id=user_id,
                status=status,
            )

            total_price = 0

            # Add OrderItems to the new order and calculate total price
            for item_data in items_data:
                price = item_data.get('price')
                quantity = item_data.get('quantity')
                total_price += price * quantity

                new_order.items.append(OrderItem(
                    product_id=item_data.get('product_id'),
                    quantity=quantity,
                    price=price
                ))

            new_order.total_price = total_price

            db.session.add(new_order)
            db.session.commit()
            return new_order.id
        except Exception as e:
            db.session.rollback()
            raise e

    def get_all_orders(self):
        """
        Fetches all orders from the database and formats them into a list of dictionaries.

        Returns:
        list: A list containing dictionaries, each representing an order with the following keys:
        """
        orders = Order.query.all()
        formated_orders = []
        for order in orders:
            items = []
            for item in order.items:
                item_info = {
                    'id': item.id,
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'price': item.price,
                    'created_at': item.created_at
                }
                items.append(item_info)

            formatted_order = {
                'id': order.id,
                'user_id': order.user_id,
                'total_price': order.total_price,
                'status': order.status.value,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'items': items
            }
            formated_orders.append(formatted_order)
        return formated_orders

    def get_order_by_id(self, order_id):
        """
        Retrieves an order by its ID.

        Args:
        - order_id (int): ID of the order to retrieve.

        Returns:
        - dict or None: Serialized order data if found, else None.

        Raises:
        - Exception: If an error occurs during order retrieval.
        """
        try:
            order = Order.query.get(order_id)
            if order:
                items = []
                for item in order.items:
                    item_info = {
                        'id': item.id,
                        'product_id': item.product_id,
                        'quantity': item.quantity,
                        'price': item.price,
                        'created_at': item.created_at
                    }
                    items.append(item_info)

                order_serialized = {
                    'id': order.id,
                    'user_id': order.user_id,
                    'total_price': order.total_price,
                    'status': order.status.value,
                    'created_at': order.created_at,
                    'updated_at': order.updated_at,
                    'items': items
                }
                return order_serialized
            return None
        except Exception as e:
            raise e

    def update_order_status(self, order_id, status_data):
        """
        Update the status of an order by order ID.

        Args:
        - order_id (int): ID of the order to update.
        - status_data (dict): Dictionary containing the new status data.

        Returns:
        - bool: True if the order status is updated successfully, else False.
        """
        try:
            order = db.session.get(Order, order_id)

            if not order:
                return False

            new_status = status_data.get('status')
            updated_at = datetime.utcnow()

            # Update the order status and updated_at timestamp
            order.status = new_status.upper()
            order.updated_at = updated_at
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    def get_orders_by_user(self, user_id):
        """
        Retrieves orders associated with a user.

        Args:
        - user_id (int): ID of the user.

        Returns:
        - list: Serialized data of orders associated with the user.

        Raises:
        - Exception: If an error occurs during retrieval of user's orders.
        """
        try:
            orders = Order.query.filter_by(user_id=user_id).all()
            formated_orders = []
            for order in orders:
                formated_order = {
                    'id': order.id,
                    'user_id': order.user_id,
                    'total_price': order.total_price,
                    'status': order.status
                    }
                formated_orders.append(formated_order)

            return formated_orders
        except Exception as e:
            raise e

    def cancel_order(self, order_id):
        """
        Cancels an order.

        Args:
        - order_id (int): ID of the order to cancel.

        Returns:
        - bool: True if order canceled successfully, otherwise False.

        Raises:
        - Exception: If an error occurs during order cancellation.
        """
        try:
            order = db.session.get(Order, order_id)
            if order:
                db.session.delete(order)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    def get_orders_by_status(self, status):
        """
        Retrieves orders by their status.

        Args:
        - status (str): Status of the orders to retrieve.

        Returns:
        - list: Serialized data of orders with the specified status.

        Raises:
        - Exception: If an error occurs during retrieval of orders by status.
        """
        try:
            orders = Order.query.filter_by(status=status.upper()).all()
            formated_orders = []
            for order in orders:
                items = []
                for item in order.items:
                    item_info = {
                        'id': item.id,
                        'product_id': item.product_id,
                        'quantity': item.quantity,
                        'price': item.price,
                        'created_at': item.created_at
                    }
                    items.append(item_info)
                formated_order = {
                    'id': order.id,
                    'user_id': order.user_id,
                    'total_price': order.total_price,
                    'items': items,
                    'created_at':order.created_at,
                    'updated_at':order.updated_at,
                    'status': order.status.value
                    }
                formated_orders.append(formated_order)
            return formated_orders
        except Exception as e:
            raise e

class OrderItemService:
    """
    A class handling various operations related to order items.
    """
    
    def get_order_items(self, order_id):
        """
        Retrieves all order items for a given order.

        Args:
        - order_id (int): ID of the order to retrieve items for.

        Returns:
        - list: Serialized data of order items for the specified order.

        Raises:
        - Exception: If an error occurs during retrieval of order items.
        """
        try:
            items = OrderItem.query.filter_by(order_id=order_id).all()
            formatted_items = []
            for item in items:
                formatted_item = {
                    'id': item.id,
                    'order_id': item.order_id,
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'price': item.price,
                    'created_at': item.created_at,
                }
                formatted_items.append(formatted_item)
            return formatted_items
        except Exception as e:
            raise e


```

__init__:
```
"""Initialize Flask app with SQLAlchemy and Flask-Migrate.

Creates a Flask app instance, configures it using 'config.py',
sets up SQLAlchemy for database operations, and configures Flask-Migrate.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes


```