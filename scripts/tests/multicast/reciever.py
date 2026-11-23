import socket
import struct

# Multicast configuration
MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5007
BUFFER_SIZE = 1024


def start_receiver():
    # 1. Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # 2. Allow multiple sockets to use the same PORT number
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 3. Bind to the port on all interfaces
    # Note: On Windows, you MUST bind to '' (all interfaces).
    # On Linux/Mac, you can bind to MCAST_GRP, but '' works everywhere.
    sock.bind(("", MCAST_PORT))

    # 4. Tell the operating system to add the socket to the multicast group
    # on all interfaces (INADDR_ANY).
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening for multicast on {MCAST_GRP}:{MCAST_PORT}...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            # Receive data from the socket
            data, address = sock.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8")
            print(
                f"Received from {address[0]}:{address[1]} -> '{message}'"
            )

    except KeyboardInterrupt:
        print("\nReceiver stopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    start_receiver()
