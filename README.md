# kafka-based-compensation-processing-system
## Overview 
The project presents a Kafka-based data processing architecture tailored for managing compensation rates and employee records. Leveraging Kafka for streamlined data processing, it centralizes storage and enhances data ingestion efficiency. The setup includes: 

1. Deploying a Bitnami Kafka cluster with three brokers.

2. A Python-based web server to expose endpoints for JSON data submission via HTTP POST requests, enabling seamless integration with Kafka topics.

3. Two consumers, operating in separate groups, analyze the data, generating JSON outputs and computing employee compensation.

4. A client pod just meant to send POST requests to the Python-based web server