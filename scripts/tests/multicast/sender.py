import socket
import time

# Multicast configuration (Must match the receiver)
MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5007

# Time-to-live (TTL)
# 1 = restricted to the same subnet (won't cross routers)
# 2+ = can cross routers (if the routers are configured for multicast)
MULTICAST_TTL = 1


def start_sender():
    # 1. Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # 2. Set the Time-to-Live (TTL) for the multicast packets
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    print(f"Sending multicast to {MCAST_GRP}:{MCAST_PORT}...")
    print("Press Ctrl+C to stop.\n")

    counter = 1
    try:
        while True:
            message = f"Hello Multicast World! (Packet #{counter})"

            # Strings must be encoded into bytes before sending
            sock.sendto(message.encode("utf-8"), (MCAST_GRP, MCAST_PORT))

            print(f"Sent: '{message}'")
            counter += 1
            time.sleep(2)  # Wait 2 seconds before sending the next message

    except KeyboardInterrupt:
        print("\nSender stopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    start_sender()
