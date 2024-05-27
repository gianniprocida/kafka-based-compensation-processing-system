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

We will install Kafka using a Helm chart. First, add the Bitnami repository to your local Helm configuration:

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Next, deploy a Bitnami Kafka cluster with three brokers in the `default` namespace (the default configuration for the Bitnami/Kafka chart) by running the following command:

```
helm install cluster-kafka bitnami/kafka
```

After installation, detailed instructions and essential information regarding the deployment and configuration of the Kafka cluster will be displayed. Be sure to save this information, as it will be necessary for accessing Kafka. You can also experiment with a pod consumer or producer to verify that the cluster is up and running. </br>
Here's an example of what the detailed instructions and essential information may look like:




The highlighted parts will be stored in a `configMap` and a `secret`. Through the `configMap` resource, applications (including the two consumers and the Python web server) will be guided on connecting to the Kafka cluster. Meanwhile, the `secret` resource ensures secure authentication between applications (clients) and brokers using the SCRAM-SHA-256 mechanism with the specified username and password