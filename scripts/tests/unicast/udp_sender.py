import socket

# Configuration
TARGET_IP = "0.0.0.0"  # IP address of the receiver
PORT = 5000
MESSAGE = "A message approaches!"

# Create a UDP socket (SOCK_DGRAM)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # No .connect() is needed for UDP. We use .sendto() instead.
    print(f"[UDP Sender] Sending to {TARGET_IP}:{PORT} -> '{MESSAGE}'")
    s.sendto(MESSAGE.encode("utf-8"), (TARGET_IP, PORT))
    print("[UDP Sender] Message sent.")
