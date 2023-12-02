"""
Module Docstring: TestOrderEndpoints

This module contains unit tests for the endpoints related to orders in the application.
"""

import unittest
import json
from app import app, db
from app.models import Order, OrderItem, StatusEnum

class TestOrderEndpoints(unittest.TestCase):
    """
    TestOrderEndpoints Class

    This class contains unit tests for various endpoints related to orders in the application.
    """
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

            created_order = db.session.get(Order, data['order_id'])
            self.assertIsNotNone(created_order)
            self.assertEqual(created_order.user_id, order_data['user_id'])
            self.assertEqual(created_order.status, StatusEnum.PENDING)

            self.assertEqual(created_order.items.count(), 2)

    def test_get_orders(self):
        """ Test retrieving all orders """
        with app.app_context():
            order1 = Order(user_id=1, total_price=50.0, status=StatusEnum.SHIPPED)
            order2 = Order(user_id=2, total_price=30.0, status=StatusEnum.PENDING)
            db.session.add(order1)
            db.session.add(order2)
            db.session.commit()

            response = self.app.get('/orders')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)

    def test_get_order_details(self):
        """ Test retrieving details of a specific order by order ID """
        with app.app_context():
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
            order = Order(user_id=1, total_price=50.0, status=StatusEnum.PENDING)
            db.session.add(order)
            db.session.commit()

            order_id = order.id
            new_status_data = {'status': 'shipped'}

            response = self.app.patch(f'/orders/{order_id}', json=new_status_data)
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Order status updated')

            updated_order = db.session.get(Order, order_id)
            self.assertEqual(updated_order.status, StatusEnum.SHIPPED)

    def test_get_orders_by_user(self):
        """ Test retrieving orders associated with a specific user """
        with app.app_context():
            user_id = 1
            order1 = Order(user_id=user_id, total_price=50.0, status='SHIPPED')
            order2 = Order(user_id=user_id, total_price=30.0, status='PENDING')
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
