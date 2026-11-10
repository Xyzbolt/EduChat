

# Outline
---
1. Eduroam
2. Nodes
3. ESP-32


# Eduroam
---

## Broadcast (intra-Vlan)
- [ ] Test if UDP broadcast works in a V-Lan
- [ ] Test if UDP multicast works in a V-Lan
	- [ ] Test if multiple nodes can send on the same multicast

## P2P (inter-Vlan)
- [ ] Test if UDP works between V-Lans for p2p
- [ ] Test if TCP works between V-lans for p2p
- [ ] Test for inter V-lan multicast

## Ethernet:
- [ ] Test if ethernet maintains static IP across days
- [ ] Test if ethernet allows sockets with wifi 


# Android
---

## Packets:

- [ ] Test if android allows receiving multicast/broadcast
	- [ ] in foreground
	- [ ] in background

## Permissions:

- [ ] Non-root permissions:
    - [ ] Receiving/sending packets (multicast/broadcast)
    - [ ] Staying in foreground/background


# ESP-32
---


## Hardware:

- [ ] Test if hardware is capable of TCP/UDP - UDP ONLY, TCP IS TOO HIGH LOAD
	- [ ] What amount of load can it handle
- [ ] Test if battery is long enough to not die on high traffic - USES LESS THAN 1W DURING NORMAL OPERATION, WILL LAST A COUPLE DAYS ON A 10kmAh POWERBANK BUT BETTER TO PLUG INTO A RANDOM USB PORT 

## Storage:

- [ ] Test if storage is enough to store:
	- [ ] IP and ID database
	- [ ] Offline DM transfers
