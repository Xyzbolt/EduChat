import socket

# Configuration
TARGET_IP = "127.0.0.1"  # IP address of the receiver
PORT = 65432  # Must match the receiver's port
MESSAGE = "Hello via TCP Unicast!"

# Create a TCP socket (SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"[TCP Sender] Connecting to {TARGET_IP}:{PORT}...")
    s.connect((TARGET_IP, PORT))

    # Send the message (must be encoded to bytes)
    print(f"[TCP Sender] Sending: {MESSAGE}")
    s.sendall(MESSAGE.encode("utf-8"))

    # Optional: Wait for response from receiver
    response = s.recv(1024)
    print(f"[TCP Sender] Server replied: {response.decode('utf-8')}")
