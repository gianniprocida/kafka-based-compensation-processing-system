
import os
import uuid
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka.producer import KafkaProducer
from entities import Employee, Compensation
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Load environment variables from .env file
load_dotenv(verbose=True)

# Initialize FastAPI app
app = FastAPI()


compensation_rates = {
    "bike": {"base_rate": 0.5, "double_rate_distance": 10, "double_rate": 2},
    "bus": {"base_rate": 0.25},
    "train": {"base_rate": 0.25},
    "car": {"base_rate": 0.1}
}

employee_data = [
    {"name": "Paul", "transport": "car", "distance": 60, "office_days": 4},
    {"name": "Martin", "transport": "bus", "distance": 8, "office_days": 2},
    {"name": "Jeroen", "transport": "bike", "distance": 9, "office_days": 5},
    {"name": "Tineke", "transport": "bike", "distance": 4, "office_days": 3},
    {"name": "Arnout", "transport": "train", "distance": 23, "office_days": 2},
    {"name": "Iris", "transport": "bike", "distance": 11, "office_days": 4},
    {"name": "Dymphie", "transport": "car", "distance": 12, "office_days": 3}
]

# Event handler for startup
@app.on_event('startup')
async def startup_event():
    """
    Event handler called when the application starts up.
    This function initializes Kafka topics and admin client.
    """
    logger.info(f"""
      Connecting to {os.environ["BOOTSTRAP_SERVERS"]}.
      Username: '{os.environ["user"]}'
      Password: {os.environ["password"]}
    """)
    
    # Initialize Kafka admin client
    client = KafkaAdminClient(
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        api_version=(0, 10, 2),
        security_protocol="SASL_PLAINTEXT",
        sasl_plain_username=os.environ["user"],
        sasl_plain_password=os.environ["password"],
        sasl_mechanism="SCRAM-SHA-256")
    
    # Create Kafka topics if they don't already exist
    try:
        topic_employee = NewTopic(name=os.environ['TOPIC_EMPLOYEE'],
                                  num_partitions=int(
                                      os.environ['PARTITIONS_EMPLOYEE']),
                                  replication_factor=int(os.environ['REPLICAS_EMPLOYEE']))
        client.create_topics([topic_employee])

        topic_compensation = NewTopic(name=os.environ['TOPIC_COMPENSATION'],
                                      num_partitions=int(
                                          os.environ['PARTITIONS_COMPENSATION']),
                                      replication_factor=int(os.environ['REPLICAS_COMPENSATION']))
        client.create_topics([topic_compensation])
    except TopicAlreadyExistsError as e:
        print(e)
    finally:
        client.close()

# Function to create Kafka producer
def make_producer():
    """
    Create and return a KafkaProducer instance.
    """
    producer = KafkaProducer(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
                             api_version=(0, 10, 2),
                             security_protocol="SASL_PLAINTEXT",
                             sasl_plain_username=os.environ["user"],
                             sasl_plain_password=os.environ["password"],
                             sasl_mechanism="SCRAM-SHA-256")
    return producer

# Endpoint to create employee records
@app.post('/api/employee', status_code=201, response_model=List[Employee])
async def create_employee():
    """
    Endpoint to create employee records and publish them to Kafka topic.
    """
    mydata = []

    producer = make_producer()

    # Create Employee objects and publish to Kafka topic
    for item in employee_data:
        
        try:
            employee = Employee(name=item["name"],
                                transport=item["transport"],
                                distance=item["distance"],
                                office_days=item["office_days"])

        
            producer.send(
                topic=os.environ["TOPIC_EMPLOYEE"],
                value=employee.json().encode("utf-8"),
            )
        except Exception as e:
            logger.error(f"An error occurred while processing employee data {e}")

    producer.flush()

    return

# Endpoint to create compensation records
@app.post('/api/compensation', status_code=201, response_model=List[Compensation])
async def create_compensation():
    """
    Endpoint to create compensation records and publish them to Kafka topic.
    """

    producer = make_producer()
    
    # Create the compensation_rates object and publish to Kafka topic

    compensation = Compensation(bike=compensation_rates["bike"],
                                bus=compensation_rates["bus"],
                                train=compensation_rates["train"],
                                car=compensation_rates["car"])


    try:
        producer.send(
            topic=os.environ["TOPIC_COMPENSATION"],
            value=compensation.json().encode("utf-8"),
        )
        print("Message sent successfully")
    except Exception as e:
        logger.error(f"An error occurred while processing employee data {e}")

    producer.flush()

    return
