from kafka import KafkaConsumer
import json

consumer_orders = KafkaConsumer(
    "order-events",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

consumer_inventory = KafkaConsumer(
    "inventory-events",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Notification Service Started...")

while True:
    for msg in consumer_orders.poll(timeout_ms=1000).values():
        for record in msg:
            event = record.value
            if event["event"] == "OrderPlaced":
                print("Email: Order received. Processing...")

    for msg in consumer_inventory.poll(timeout_ms=1000).values():
        for record in msg:
            event = record.value

            if event["event"] == "InventoryReserved":
                print("Email: Order confirmed!")

            elif event["event"] == "OutOfStock":
                print("Email: Item out of stock.")