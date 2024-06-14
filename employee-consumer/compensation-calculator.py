import os
import uuid
from typing import List
from dotenv import load_dotenv
from kafka.consumer import KafkaConsumer
import json
import logging
import csv

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__file__)


load_dotenv(verbose=True)


def calculate_compensation(employee_record):
    transport = employee_record.value["transport"]
    distance = float(employee_record.value["distance"])
    office_days = int(employee_record.value["office_days"])
    
    file_path = os.path.join('..', 'shared', 'data.json')
   
    try:
        with open(file_path, 'r') as f:
            compensation_rates = json.load(f)
    except FileNotFoundError:
        print(f"Error: File data.json not found.")

    if transport == "bike":
        base_rate = float(compensation_rates["bike"]["base_rate"])
        double_rate_distance = float(
            compensation_rates["bike"]["double_rate_distance"])
        double_rate = float(compensation_rates["bike"]["double_rate"])

        compensation = base_rate * distance * office_days
        if distance >= 5 and distance <= double_rate_distance:
            compensation *= double_rate
    else:

        base_rate = compensation_rates[transport]["base_rate"]
        compensation = distance * base_rate * office_days
    return round(compensation, 2)


def data_key_deserializer(key):
    return key.decode('utf-8')


def data_value_deserializer(value):
    return json.loads(value.decode('utf-8'))


def main():
    logger.info(f"""Started Python consumer for
                    topic {os.environ["TOPIC_EMPLOYEE"]}""")

    consumer_employee = KafkaConsumer(bootstrap_servers=os.environ["BOOTSTRAP_SERVERS"],
                                      group_id=os.environ['CONSUMER_GROUP_EMPLOYEE'],
                                      value_deserializer=data_value_deserializer,
                                      api_version=(0, 10, 2),
                                      security_protocol="SASL_PLAINTEXT",
                                      sasl_plain_username=os.environ["user"],
                                      sasl_plain_password=os.environ["password"],
                                      sasl_mechanism="SCRAM-SHA-256")

    consumer_employee.subscribe([os.environ['TOPIC_EMPLOYEE']])

    file_path = os.path.join('data', 'monthly_overview.csv')

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["employee", "transport", "traveled distance", "compensation"])

        for employee_record in consumer_employee:

            compensation = calculate_compensation(employee_record)

            logger.info(f"""
                        Consumed person: {employee_record.value["name"]}
                        transport: {employee_record.value["transport"]}
                        distance: {employee_record.value["distance"]}
                        office days {employee_record.value["office_days"]}
                        your compensation {compensation}
                        """)

            writer.writerow([employee_record.value["name"], employee_record.value["transport"],
                            employee_record.value["distance"], compensation])


if __name__ == '__main__':
    main()
