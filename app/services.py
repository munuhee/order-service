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
                status=status.upper(),
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
        except Exception as exception:
            db.session.rollback()
            raise exception

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
            order = db.session.get(Order, order_id)
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
        except Exception as exception:
            raise exception

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

        except Exception as exception:
            db.session.rollback()
            raise exception

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
                    'status': order.status.value
                    }
                formated_orders.append(formated_order)

            return formated_orders
        except Exception as exception:
            raise exception

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
        except Exception as exception:
            db.session.rollback()
            raise exception

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
        except Exception as exception:
            raise exception

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
        except Exception as exception:
            raise exception
