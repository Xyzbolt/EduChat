import socket

# Configuration
LISTEN_IP = "127.0.0.1"  # Use "0.0.0.0" to listen on all network interfaces
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Create a TCP socket (SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((LISTEN_IP, PORT))
    s.listen()
    print(f"[TCP Receiver] Listening on {LISTEN_IP}:{PORT}...")

    # Wait for a connection
    conn, addr = s.accept()
    with conn:
        print(f"[TCP Receiver] Connected by {addr}")
        while True:
            # Receive data (buffer size 1024 bytes)
            data = conn.recv(1024)
            if not data:
                break  # Connection closed by sender
            print(f"[TCP Receiver] Received: {data.decode('utf-8')}")

            # Optional: Send a reply back to the sender
            conn.sendall(b"Message received loud and clear!")
