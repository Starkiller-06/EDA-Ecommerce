# EDA-Ecommerce

## Architecture and Decoupling
This project demonstrates an Event-Driven Architecture (EDA) by breaking down a traditional e-commerce checkout process into a decoupled, event-driven microservices architecture. In a standard monolithic approach, when a user attempts to make a purchase, the system synchronously updates the inventory, processes payments, and sends confirmation emails all at once, which can cause the system to freeze under load. 

By contrast, this application decouples these responsibilities using a message broker. The Order Service simply exposes an API endpoint to receive the order, saves it locally with a PENDING status, publishes an `OrderPlaced` event to the broker, and immediately returns an HTTP accepted response to the user. The Inventory Service and Notification Service operate completely independently, listening to the message broker for specific events (like `OrderPlaced`, `InventoryReserved`, or `OutOfStock`) and reacting to them. This decoupling means that if the notification system crashes or experiences delays, it will not block the user from placing an order or prevent the inventory from updating.

## Technologies Used
* Python 
* FastAPI (Order Service API framework)
* Apache Kafka & Zookeeper (Message Broker) 
* Docker & Docker Compose (for containerized broker setup) 

## How to Run the Project

To run this project, ensure you have Python and Docker installed on your machine.

**1. Start the Message Broker**
Navigate to the root directory containing the `docker-compose.yml` file and start the Kafka and Zookeeper services using Docker.
```bash
docker-compose up -d
```

**2. Start the Order Service (Producer)**
Navigate to the `order_service` directory. Install the required dependencies (e.g., `fastapi`, `uvicorn`, `kafka-python`) and start the application to build the API and publisher logic.
```bash
uvicorn app:app --reload --port 8000
```

**3. Start the Inventory Service (Consumer 1)**
Open a new terminal, navigate to the `inventory_service` directory, and start the inventory consumer script.
```bash
python consumer.py
```

**4. Start the Notification Service (Consumer 2)**
Open another terminal, navigate to the `notif_service` directory, and start the notification consumer script so it can subscribe to the correct topics and log its actions to the console.
```bash
python consumer.py
```

**5. Test the Application**
You can now test the decoupled system by sending a POST request to `http://localhost:8000/orders` with a JSON body containing `userId`, `itemId`, and `quantity`. Check the console logs of your consumer terminals to see the events being processed asynchronously.