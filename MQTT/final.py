import docker
import subprocess
client = docker.from_env()

client.swarm.init() # Swarm Initilization 

node = client.nodes.list()
attr = node[0].attrs
Created_Date = attr['CreatedAt']
Name = attr['Description']['Hostname']
ID = attr['ID']



# Network Creation 
ipam_pool = docker.types.IPAMPool(subnet='10.10.10.2/24', gateway='10.10.10.1',iprange='10.10.10.2/24')
ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
client.networks.create("se443_test_net", driver = "overlay", scope = "global", attachable = True,ipam=ipam_config )



subprocess.run(["docker","service","create","--name","broker","--replicas","3","--restart-condition","any","--network=se443_test_net","--mount","type=bind,source=/Users/amal/Downloads/MQTT/mosquitto.conf,destination=/mosquitto/config/mosquitto.conf","eclipse-mosquitto:latest"]) 

# # ------------------>SERVICES<---------------------------------
#  SUB Service =  docker service create --network test_network_1  --replicas 3 efrecon/mqtt-client sub  -h 10.0.3.24  -p 1883  -t "Helloworld networks=['test_network_1']"


Sub = client.services.create("efrecon/mqtt-client",["sub","-h","10.10.10.4","-p","1883","-t","alfaisal_uni", "-v"],networks=['se443_test_net'],name = "subscriber")
Sub.scale(replicas = 3)


# PUB Service =  docker service create --network test_network_1 --replicas 3 efrecon/mqtt-client pub  -h 10.0.3.24  -p 1883  -t "Helloworld"  -m 'Test' -i "Nouman"


Pub = client.services.create("efrecon/mqtt-client",["pub","-h","10.10.10.4","-p","1883","-t","alfaisal_uni","-m","Amal Alshuwaier 191283"],networks=['se443_test_net'], name= "publisher")
Pub.scale(replicas = 3)

print("\n")
print("Swarm Details: \n")
print("Swarm Host Name: "+Name+", ID: "+ ID+", Created At: "+ Created_Date )


print("\n")
print("Publisher's ID, Name, Date of Creation")
pub = subprocess.call('./pub-info.sh')
print("\n")


print("Subscriber's ID, Name, Date of Creation")
sub = subprocess.call('./sub-info.sh')
print("\n")

subprocess.call('./test.sh')

