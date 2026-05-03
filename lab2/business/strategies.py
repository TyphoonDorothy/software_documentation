# business/strategies.py
from abc import ABC, abstractmethod
import json
import redis
from kafka import KafkaProducer

class IOutputStrategy(ABC):
    @abstractmethod
    def write_data(self, data: list[dict]):
        pass

class ConsoleOutputStrategy(IOutputStrategy):
    def write_data(self, data: list[dict]):
        print(f"--- Writing {len(data)} Air Quality records to CONSOLE ---")
        for item in data[:3]: # Just printing 3 because this dataset has huge rows!
            print(item)
        print("... (console output complete)")

class RedisOutputStrategy(IOutputStrategy):
    def __init__(self, host='localhost', port=6379, key='sensor_dataset'):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.key = key

    def write_data(self, data: list[dict]):
        print(f"--- Writing {len(data)} records to REDIS ---")
        for item in data:
            self.client.rpush(self.key, json.dumps(item))
        print("Successfully saved to Redis.")

class KafkaOutputStrategy(IOutputStrategy):
    def __init__(self, bootstrap_servers=['localhost:9092'], topic='air_quality_metrics'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def write_data(self, data: list[dict]):
        print(f"--- Writing {len(data)} records to KAFKA ---")
        for item in data:
            self.producer.send(self.topic, item)
        self.producer.flush()
        print("Successfully sent to Kafka.")

def get_output_strategy(config_path: str = '../../config.json') -> IOutputStrategy:
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Config file not found, defaulting to Console.")
        return ConsoleOutputStrategy()

    strategy_type = config.get("output_strategy", "console").lower()

    if strategy_type == "redis":
        return RedisOutputStrategy(key=config.get("redis_key", "sensor_dataset"))
    elif strategy_type == "kafka":
        return KafkaOutputStrategy(topic=config.get("kafka_topic", "air_quality_metrics"))
    else:
        return ConsoleOutputStrategy()