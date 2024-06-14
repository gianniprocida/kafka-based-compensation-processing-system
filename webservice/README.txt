# Run 

docker-compose up -d 

the following command to deploy what's defined in the docker-compose.yaml file


# Run 

docker-compose ps 

#to make sure that every container/service is up and running:



### Important when you run docker-ps command

"0.0.0.0:9092->9092/tcp": This means that port 9092 on the host machine is mapped to port 9092 inside the Docker
 container. Any traffic sent to port 9092 on the host will be directed to the corresponding port 9092 within 
 the container.
"0.0.0.0:29092->29092/tcp": Similarly, this indicates that port 29092 on the host machine is mapped to port 29092 inside the Docker container.
The "0.0.0.0" in the mapping means that the container is bound to all network interfaces on the host, making it accessible from external sources. The first part before the arrow (->) is the host machine's port, and the second part after the arrow is the corresponding port inside the container.


# Create a virtual environment in python

python3 -m venv venv

# Activate the virtual environment

source venv/bin/activate  

# Install python packages

pip install -r requirements.txt

# run the application 

uvicorn main:app --reload

# run an http client. Send a post request on port 8000/ ( where our application lives)


http POST 10.1.3.75:8088/api/employee

http POST 10.1.3.75:8088/api/compensation



List topics

docker exec -it cli-tools kafka-topics --list --bootstrap-server broker0:29092,broker1:29093,broker2:29094


Create Topics 

docker exec -it cli-tools kafka-topics --create --bootstrap-server broker0:29092 --topic people --partitions 3 --replication-factor 3


Describe Topics

docker exec -it cli-tools kafka-topics --describe --bootstrap-server broker0:29092 --topic people --partitions 3 --replicatin-factor 3


docker exec -it cli-tools kafka-console-co
nsumer --bootstrap-server broker0:29092 --topic people.basic.python

#Exctract the password 

password="$(kubectl get secret cluster-kafka-user-passwords --namespace default -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";


echo -n $password | base64




helm install kafka-release bitnami/kafka --set persistence.size=8Gi,logPersistence.size=8Gi,replicaCount=3,volumePermissions.enabled=true,persistence.enabled=true,logPersistence.enabled=false