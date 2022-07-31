# published a topic temperature_reading to kafka broker at locahost:9092
from kafka import KafkaProducer
import time
import pickle


if __name__ == "__main__":

    producer = KafkaProducer(bootstrap_servers="kafka:9092")

    with open("streaming_data.pickle", "rb") as handle:
        stream_data = pickle.load(handle)

    for data in stream_data:
        producer.send("temperature_readings", bytes(data, 'utf-8'))
        time.sleep(0.5)
 
 