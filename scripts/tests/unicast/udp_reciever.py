import socket

# Configuration
LISTEN_IP = "0.0.0.0"  # Use "0.0.0.0" to listen on all interfaces
PORT = 5000

# Create a UDP socket (SOCK_DGRAM)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((LISTEN_IP, PORT))
    print(f"[UDP Receiver] Waiting for data on {LISTEN_IP}:{PORT}...")

    while True:
        # recvfrom returns both the data and the address of the sender
        data, addr = s.recvfrom(1024)
        print(f"[UDP Receiver] Received from {addr}: {data.decode('utf-8')}")
