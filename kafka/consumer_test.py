from kafka import KafkaConsumer
import json

topic = "armor-insert"

def main():
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                            auto_offset_reset='earliest',
                            consumer_timeout_ms=1000)
    consumer.subscribe(['armor-insert'])
    while(True):
        msg = consumer.poll()
        if not msg:
            continue
        if msg.error():
            print("Error occurred" + msg.error())
        else:
            print(msg)

if __name__ == "__main__":
    main()