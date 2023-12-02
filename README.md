# Order Service

The Order Service is a microservice within an eCommerce platform that facilitates order management via RESTful APIs. This service is developed using Python, Docker, Flask, and offers endpoints to perform various operations related to orders.

## Features

- **Order Management**: Create, retrieve, update, and delete orders.
- **Order Details**: Manage order specifics like products, quantities, statuses, and customer information.
- **Integration Support**: Seamlessly integrates with other microservices for a holistic eCommerce experience.

## Technologies Used

- **Python**: Utilized as the primary programming language for development.
- **Flask**: A micro web framework used for building the RESTful APIs.
- **Docker**: Containerization for easy deployment and scalability.
- **RESTful API**: Adherence to REST principles for endpoint design and interaction.

## Installation

### Prerequisites

- **Python 3.x**: Ensure Python is installed.
- **Docker**: Install Docker for containerization.

### Setup Steps

1. Clone this repository:

    ```bash
    https://github.com/munuhee/order-service.git
    ```

2. Navigate to the order service directory:

    ```bash
    cd order-service
    ```

3. Build the Docker container:

    ```bash
    docker build -t order-service .
    ```

4. Run the Docker container:

    ```bash
    docker run -p 5000:5000 order-service
    ```

5. Access the service at `http://localhost:5000`

## API Endpoints

The service exposes the following endpoints:

- GET /health: Health check endpoint returning a success status.
- POST /orders: Create a new order.
- GET /orders: Retrieve all orders.
- GET /orders/<int:order_id>: Get details of a specific order by order ID.
- PATCH /orders/<int:order_id>: Update the status of an order by order ID.
- GET /orders/user/<int:user_id>: Get orders associated with a specific user.
- DELETE /orders/<int:order_id>: Cancel an order by order ID.
- GET /orders/status/<string:status>: Get orders by their status.
- GET /orders/<int:order_id>/items: Get all order items for a specific order.

## Usage

- Utilize any HTTP client (e.g., cURL, Postman) to interact with the endpoints provided by the Order Service.
- Ensure proper authentication and authorization mechanisms are in place for secure access.

## Configuration

- Adjust environment variables or settings in the `config.py` or `.env` file for database connections, authentication details, or any service-specific configurations.

## Contributing

- Contributions, suggestions, or bug reports are highly appreciated! Feel free to open issues or pull requests for improvements.
