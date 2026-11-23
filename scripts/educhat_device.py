#this script will act as user_1 (the code for any user trying to join educhat)
import socket
import threading
import ipaddress
import json
from supernode import behave_as_supernode
from ordinary_node import behave_as_ordinary_node

is_supernode = False

def main():
    #creating a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_ip, network_addr = get_network_info()
    print(f"network_information: {broadcast_ip, network_addr}")
    tracker_add = ('10.21.240.149', 5000) #the trackers address

    #reserving port 5001 for this socket (choosing different sockets only because were communicating on the same ip)
    # sock.bind(('0.0.0.0', 5001))
    sock.settimeout(1.0)

    #sending connection request to tracker
    response = connect_to_educhat(sock=sock, tracker_add=tracker_add, subnet=network_addr)
    print(response)
    
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
    sock.sendto(json.dumps(connection_payload).encode(), tracker_add)

    while True:
            
            try:
                data, addr = sock.recvfrom(1024)
                message_str = data.decode("utf-8")
                payload = json.loads(message_str)
                print(f"payload: {payload}")
    
                if isinstance(payload, dict) and payload.get("application") == "educhat":
                    response = f"{payload}"
                    print(f"response: {response}")
            except socket.timeout:
                 continue
            except KeyboardInterrupt:
                print("\nShutting down...")
                break
            except (UnicodeDecodeError, json.JSONDecodeError, KeyError):
                #ignoring unrelated broadcasts
                continue


    return response



#getting the broadcast ip    

import psutil

def get_network_info():
    # 1. Use a temporary socket so your main socket's bind is untouched
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_sock:
        temp_sock.connect(("8.8.8.8", 80))
        local_ip = temp_sock.getsockname()[0]

    # 2. Match that local IP against your network interfaces to find the real mask
    subnet_mask = "255.255.255.0"  # Fallback default
    for interface_addrs in psutil.net_if_addrs().values():
        for addr in interface_addrs:
            if addr.family == socket.AF_INET and addr.address == local_ip:
                subnet_mask = addr.netmask
                break

    network = ipaddress.IPv4Interface(f"{local_ip}/{subnet_mask}").network
    return (network.broadcast_address, network.network_address)





if __name__ == "__main__":
    main()

