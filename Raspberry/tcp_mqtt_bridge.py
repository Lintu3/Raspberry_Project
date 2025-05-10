import paho.mqtt.client as mqtt
import socket
# Defining the MQTT broker address (localhost in this case) and MQTT topic
broker_address = "127.0.0.1"
topic = "relaylamp"

# Creating an MQTT client instance with a specific client ID and protocol versio
client = mqtt.Client(client_id="RaspCl", protocol=mqtt.MQTTv311)

# Connecting the MQTT client to the broker
client.connect(broker_address)

# Creating a TCP/IP socket for server-side communication
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the socket to all available network interfaces on port 8080
server_socket.bind(('0.0.0.0', 8080))

# Configuring the socket to listen for incoming connections, with a backlog of 1. Could be changed to some other number.
server_socket.listen(1)

print("Listening TCP/IP....")

# Infinite loop to handle incoming TCP/IP connections
while True:
    (client_socket, address) = server_socket.accept()
    print(f"Connection to {address}")

# Receiving a command from the client (up to 1024 bytes) and decoding it as UTF-8
    command = client_socket.recv(1024).decode('utf-8')
    if command:
        print(f"Command: {command} received")
        # Publishing the received command to the specified MQTT topic
        client.publish(topic, command)
        print(f"Command: {command} sent to MQTT broker on topic: {topic}")
    # Closing the client socket after processing the command
    client_socket.close()