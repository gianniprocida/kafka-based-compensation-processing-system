import os
import uuid
from typing import List
from dotenv import load_dotenv
from kafka.consumer import KafkaConsumer
import json
import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__file__)


load_dotenv(verbose=True)


def data_key_deserializer(key):
    """Deserialize the key of a Kafka message."""
    return key.decode('utf-8')


def data_value_deserializer(value):
    """Deserialize the key of a Kafka message."""
    return json.loads(value.decode('utf-8'))


def main():
    """Main function to consume data from Kafka topic and store it in a file."""
    logger.info(f"""Started Python consumer for
                    topic {os.environ["TOPIC_COMPENSATION"]}""")
        
    # Initialize Kafka consumer
    consumer_compensation = KafkaConsumer(bootstrap_servers=os.environ["BOOTSTRAP_SERVERS"],
                             group_id=os.environ['CONSUMER_GROUP_COMPENSATION'],
                             value_deserializer=data_value_deserializer,
                             api_version=(0, 10, 2),
                             security_protocol="SASL_PLAINTEXT",
                             sasl_plain_username=os.environ["user"],
                             sasl_plain_password=os.environ["password"],
                             sasl_mechanism="SCRAM-SHA-256")
    
    
    # Subscribe to Kafka topic 
    consumer_compensation.subscribe([os.environ['TOPIC_COMPENSATION']])
    
    
    logger.info(f"""
      Consuming data from {os.environ["TOPIC_COMPENSATION"]}.
      Username: '{os.environ["user"]}'
      Password: {os.environ["password"]}
    """)
  
    file_path = os.path.join('shared', 'data.json')
    

    with open(file_path, 'w') as f:
        f.write('')
        
    # Iterate over messages from the Kafka topic
    for item in consumer_compensation:
        json_data_str = json.dumps(item.value)
    # Store the JSON string in the data.json file
        with open(file_path, 'w') as f:
          f.write(json_data_str + '\n')

       

if __name__=='__main__':
    main()
   

    
        
