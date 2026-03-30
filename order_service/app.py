from fastapi import FastAPI
from kafka import KafkaProducer
import json
import uuid

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

orders_db = [] 

@app.post("/orders")
def create_order(order: dict):
    order_id = str(uuid.uuid4())

    new_order = {
        "orderId": order_id,
        "userId": order["userId"],
        "itemId": order["itemId"],
        "quantity": order["quantity"],
        "status": "PENDING"
    }

    orders_db.append(new_order)

    # Publish event
    producer.send("order-events", {
        "event": "OrderPlaced",
        "data": new_order
    })

    return {"message": "Order received", "status": "ACCEPTED"}