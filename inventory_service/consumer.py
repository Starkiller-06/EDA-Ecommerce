from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    "order-events",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

inventory = {
    "item1": 10,
    "item2": 0
}

for message in consumer:
    event = message.value
    data = event["data"]

    item_id = data["itemId"]
    quantity = data["quantity"]

    print(f"Received OrderPlaced for {item_id}")

    if inventory.get(item_id, 0) >= quantity:
        inventory[item_id] -= quantity

        producer.send("inventory-events", {
            "event": "InventoryReserved",
            "data": data
        })

        print("Inventory reserved")

    else:
        producer.send("inventory-events", {
            "event": "OutOfStock",
            "data": data
        })

        print("Out of stock")