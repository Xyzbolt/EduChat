#this modules handles the behaviour of a supernode over educhat

"""supernode responsibilites:
1. listen for broadcasts over their subnet and then transmit the message request to other subnets (supernodes)
2. listen for p2p connections from other supernodes (subnets) and then broadcast the message request to their subnet
"""

import socket
import json
import threading


def behave_as_supernode(sock, broadcast_ip, supernodes):
    start_listening_for_connections(sock=sock, supernodes=supernodes, broadcast_ip=broadcast_ip)
    listening_thread = threading.Thread(target=start_listening_for_connections, daemon=True)
    listening_thread.start()
    start_broadcast_commmunication(sock=sock, broadcast_ip=broadcast_ip)




def start_broadcast_commmunication(sock, broadcast_ip):
    sock.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_BROADCAST,
    1
    )
    while True:
        message = input("") 
        message_payload = {
            "application": "educhat",
            "public_id": "user-111", #this will remain the same for life (while ip can change)
            "message_type": "communication",
            "message": message
        }     
        sock.sendto(str(message_payload).encode(), (broadcast_ip, 6000))


#supernode listening for connections:
def start_listening_for_connections(sock: socket.socket, supernodes, broadcast_ip):
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            message_str = data.decode("utf-8")
            payload = json.loads(message_str)
            
            #sending subnet messages to all supernodes
            if isinstance(payload, dict) and payload.get("application") == "educhat" and payload.get("message-type") == "communication":
                print(f"{payload["public_id"]}: {payload["message"]}")
                cross_subnet_payload = {
                        "application": "educhat",
                        "message-type": "broadcast-request",
                        "payload": payload
                    }
                for supernode_addr in supernodes:
                    sock.sendto(str(cross_subnet_payload).encode(), supernode_addr)

            #broadcasting supernode messages to your subnet
            if isinstance(payload, dict) and payload.get("application") == "educhat" and payload.get("message-type") == "broadcast-request":
                broadcast_payload = payload.get("payload")
                sock.sendto(str(broadcast_payload).encode(), (broadcast_ip, 6000))
                print(f"{broadcast_payload["public_id"]}: {broadcast_payload["message"]}")

            
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError):
            #ignoring unrelated broadcasts
            continue

