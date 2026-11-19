#this module handles the behavour of any ordinary node in a subnet

"""Ordinary node responsibilites:
"""
import socket
import threading
import json

def behave_as_ordinary_node(sock, broadcast_ip):
    start_broadcast_listening(sock=sock)
    listening_thread = threading.Thread(target=start_broadcast_listening, daemon=True)
    listening_thread.start()
    start_broadcast_commmunication(sock=sock, broadcast_ip=broadcast_ip)




# this section handles the listening part
# a seperate thread is used for this function to avoid blocking
def start_broadcast_listening(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            message_str = data.decode("utf-8")
            payload = json.loads(message_str)

            if isinstance(payload, dict) and payload.get("application") == "educhat":
                print(f"{payload["public_id"]}: {payload["message"]}")
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError):
            #ignoring unrelated broadcasts
            continue


#sock is the socket, addr is used when devide is a normal user and has to send a message to their subnets supernode
#if device itself is a supernode, then it must send to every supernode
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