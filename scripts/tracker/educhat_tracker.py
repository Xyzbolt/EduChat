#this script will act as the tracker, simplified for testing the supernode and normal node code

import socket
import threading
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.bind(('0.0.0.0', 5000))

connected_devices = []

supernodes = []


def main():
    start_listening_for_connections()

def start_listening_for_connections(sock=sock):
    while True:
        connection_response_payload_supernode = {}
        connection_response_payload_user = {}
        data, node_addr = sock.recvfrom(1024)
        try:
            message_str = data.decode("utf-8")
            payload = json.loads(message_str)

            if isinstance(payload, dict) and payload.get("application") == "educhat" and payload.get("message-type") == "connection-request":
                subnet = payload.get("subnet")

                supernode_exists = any(subnet_x == subnet for subnet_x, supernode in supernodes)
                if supernodes.get(subnet) == None:  #have to change this because supernodes is now a list of dicts, with the key as the index
                    supernodes[subnet] = node_addr
                    connected_devices.append({
                        "public_id": payload.get("public_id"),
                        "supernode": True,
                        "subnet": subnet,
                        "device_addr": node_addr
                    })
                    connection_response_payload_supernode = {
                        "role": "supernode",
                        "supernodes": supernodes, #list of all supernode addresses   
                    }
                    sock.sendto(str(connection_response_payload_supernode).encode(), node_addr)
                else:
                    connected_devices.append({
                        "public_id": payload.get("public_id"),
                        "supernode": False,
                        "subnet": subnet,
                        "device_addr": node_addr
                    })
                    connection_response_payload_user = {
                        "role": "ordinary_node",
                    }
                    sock.sendto(str(connection_response_payload_user).encode(), node_addr)
                print(f"{payload["public_id"]} with ip {node_addr} is now connected to educhat")

        except (UnicodeDecodeError, json.JSONDecodeError, KeyError):
            #ignoring unrelated broadcasts
            continue


def ping_supernodes(supernodes: dict):
    for supernode in supernodes.items:
        supernode_addr = supernode

if __name__ == "__python__":
    main()