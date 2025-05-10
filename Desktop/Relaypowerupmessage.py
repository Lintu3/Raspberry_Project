import socket

# This script is a simple TCP client that connects to a server and sends commands to it.

server_ip = "00.00.00.00"
server_port = 8080

while True:
    command = input("Relay start write 'on' to stop write 'off': ")  # just to show an example of command.
    if command == "on" or command == "off":
        # Create a TCP/IP socket
        # The socket is created using the IPv4 address family (AF_INET) and the TCP protocol (SOCK_STREAM).
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        # Send the command to the server
        client_socket.send(command.encode('utf-8'))
        client_socket.close()

        print("Command sent to Raspberry Pi.")
    else: 
        print(f"Invalid command: '{command}' !! Try again.")