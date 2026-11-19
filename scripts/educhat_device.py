#this script will act as user_1 (the code for any user trying to join educhat)
import socket
import threading
import ipaddress
import json
from scripts.supernode import behave_as_supernode
from scripts.ordinary_node import behave_as_ordinary_node

is_supernode = False

def main():
    #creating a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_ip, network_addr = get_broadcast_ip(sock)
    tracker_add = ('10.7.76.31', 5000) #the trackers address

    #reserving port 5001 for this socket (choosing different sockets only because were communicating on the same ip)
    sock.bind(('0.0.0.0', 5001))

    #sending connection request to tracker
    response = connect_to_educhat(sock=sock, tracker_add=tracker_add, subnet=network_addr)
    
    if response["role"] == "supernode":
        behave_as_supernode(sock=sock, broadcast_ip=broadcast_ip, supernodes=response["supernode"])
    if response["role"] == "user":
        behave_as_ordinary_node(sock=sock, broadcast_ip=broadcast_ip)
        






def connect_to_educhat(sock, tracker_add, subnet):
    connection_payload = {
        "application": "educhat",
        "public_id": "user-111", #this will remain the same for life (while ip can change)
        "message_type": "connection-request",
        "subnet": subnet
    }


    #sending the initial connection request
    sock.sendto(str(connection_payload).encode(), tracker_add)
    response, addy = sock.recvfrom(1024)

    response = response.decode()
    return json.loads(response)



#getting the broadcast ip    
def get_broadcast_ip(sock):
    sock.connect(("8.8.8.8", 80))
    local_ip = sock.getsockname()[0]
    sock.close()

    subnet_mask = '255.255.255.0'
    network = ipaddress.IPv4Interface(f"{local_ip}/{subnet_mask}").network

    return (network.broadcast_address, network.network_address)




if __name__ == "__python__":
    main()

