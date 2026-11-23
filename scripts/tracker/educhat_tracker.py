#this script will act as the tracker, simplified for testing the supernode and normal node code

import socket
import threading
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.bind(('0.0.0.0', 5000))
sock.settimeout(1.0)
connected_devices = []

supernodes = {}


def main():
    start_listening_for_connections()

def start_listening_for_connections(sock=sock):
    print("Tracker listening on port 5000...")
    while True:
        connection_response_payload_supernode = {}
        connection_response_payload_user = {}
        
        try:
            data, node_addr = sock.recvfrom(1024)
            message_str = data.decode("utf-8")
            payload = json.loads(message_str)
            print(payload)
            if isinstance(payload, dict) and payload.get("application") == "educhat" and payload.get("message_type") == "connection-request":
                subnet = payload.get("subnet")

                if supernodes.get(subnet) == None:  #have to change this because supernodes is now a list of dicts, with the key as the index
                    supernodes[subnet] = node_addr
                    connected_devices.append({
                        "public_id": payload.get("public_id"),
                        "supernode": True,
                        "subnet": subnet,
                        "device_addr": node_addr
                    })
                    connection_response_payload_supernode = {
                        "application": "educhat",
                        "role": "supernode",
                        "supernodes": supernodes, #list of all supernode addresses   
                    }
                    sock.sendto(json.dumps(connection_response_payload_supernode).encode('utf-8'), node_addr)
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
                    sock.sendto(json.dumps(connection_response_payload_user).encode(), node_addr)
                print(f"{payload["public_id"]} with ip {node_addr} is now connected to educhat")
            else:
                print("not a dict or something")
        except socket.timeout:
                         continue
        except KeyboardInterrupt:
            print("\nShutting down...")
            break

        except (UnicodeDecodeError, json.JSONDecodeError, KeyError):
            #ignoring unrelated broadcasts
            continue


def ping_supernodes(supernodes: dict):
    for supernode in supernodes.items:
        supernode_addr = supernode

if __name__ == "__main__":
    main()
