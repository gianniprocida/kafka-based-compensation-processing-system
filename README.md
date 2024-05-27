# kafka-based-compensation-processing-system
## Overview 
The project presents a Kafka-based data processing architecture tailored for managing compensation rates and employee records. Leveraging Kafka for streamlined data processing, it centralizes storage and enhances data ingestion efficiency. The setup includes: 

1. Deploying a Bitnami Kafka cluster with three brokers.

2. Configuring a Python-based web server to expose endpoints for JSON data submission via HTTP POST requests, enabling seamless integration with Kafka topics.

3. Implementing Two consumers operating in separate groups to analyze the data, generate JSON outputs, and compute employee compensation.

4. Deploying a client pod specifically for sending POST requests to the Python-based web server. 


## Prerequisites 
* Docker Desktop
* macOS
* Helm 

# Deploying a Bitnami Kafka cluster with three brokers.