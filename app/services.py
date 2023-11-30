"""
The 'OrderService' module manages operations related to orders within the application.
It includes functionalities for creating, retrieving, updating, and canceling orders,
as well as calculating order totals and fetching orders based on specific criteria.
"""

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
            order = Order(**order_data)
            db.session.add(order)
            db.session.commit()
            return order.id
        except Exception as e:
            db.session.rollback()
            raise e

    def get_all_orders(self):
        orders = Order.query.all()
        formated_orders = []
        for order in orders:
            formated_order = {
                'id': order.id,
                'user_id': order.user_id,
                'total_price': order.total_price,
                'status': order.status,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'items': order.items
            }
            formated_orders.append(formated_order)
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
            order = db.session.get(Order, order_id)
            order_serialized = {
                'id': order.id,
                'user_id': order.user_id,
                'total_price': order.total_price,
                'status': order.status,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'items': order.items
            }
            return order_serialized if order else None
        except Exception as e:
            raise e

    def update_order_status(self, order_id, status_data):
        """
        Updates the status of an order.

        Args:
        - order_id (int): ID of the order to update.
        - status_data (dict): Updated status information.

        Returns:
        - bool: True if order status updated successfully, otherwise False.

        Raises:
        - Exception: If an error occurs during order status update.
        """
        try:
            order = db.session.get(Order, order_id)
            if order:
                order.status = status_data['status']
                order.updated_at = status_data['updated_at']
                db.session.commit()
                return True
            return False
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
            orders = Order.query.filter_by(status=status).all()
            formated_orders = []
            for order in orders:
                formated_order = {
                    'id': order.id,
                    'user_id': order.user_id,
                    'total_price': order.total_price,
                    'created_at':order.created_at,
                    'updated_at':order.updated_at,
                    'status': order.status
                    }
                formated_orders.append(formated_order)
            return formated_orders
        except Exception as e:
            raise e

    def calculate_order_total(self, order_items):
        """
        Calculates the total price of an order.

        Args:
        - order_items (list): List of items comprising the order.

        Returns:
        - float: Total price of the order.

        Raises:
        - Exception: If an error occurs during order total calculation.
        """
        try:
            total_price = sum(item['price'] for item in order_items)
            return total_price
        except Exception as e:
            raise e

class OrderItemService:
    """
    A class handling various operations related to order items.
    """

    def __init__(self):
        """
        Initializes the OrderItemService.
        """
        pass

    def create_order_item(self, order_id, item_data):
        """
        Creates a new order item for a given order.

        Args:
        - order_id (int): ID of the order to add the item to.
        - item_data (dict): Data for the new order item.

        Returns:
        - int: The ID of the created order item.

        Raises:
        - Exception: If an error occurs during order item creation.
        """
        try:
            item_data['order_id'] = order_id
            order_item = OrderItem(**item_data)
            db.session.add(order_item)
            db.session.commit()
            return order_item.id
        except Exception as e:
            db.session.rollback()
            raise e

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
                    'updated_at': item.updated_at
                }
                formatted_items.append(formatted_item)
            return formatted_items
        except Exception as e:
            raise e

    def update_order_item(self, item_id, updated_data):
        """
        Updates an order item.

        Args:
        - item_id (int): ID of the order item to update.
        - updated_data (dict): Updated data for the order item.

        Returns:
        - bool: True if order item updated successfully, otherwise False.

        Raises:
        - Exception: If an error occurs during order item update.
        """
        try:
            order_item = db.session.get(OrderItem, item_id)
            if order_item:
                order_item.quantity = updated_data['quantity']
                order_item.updated_at = updated_data['updated_at']
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_order_item(self, item_id):
        """
        Deletes an order item.

        Args:
        - item_id (int): ID of the order item to delete.

        Returns:
        - bool: True if order item deleted successfully, otherwise False.

        Raises:
        - Exception: If an error occurs during order item deletion.
        """
        try:
            order_item = db.session.get(OrderItem, item_id)
            if order_item:
                db.session.delete(order_item)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e
