# Outline
---
1. Features
2. Limitations
3. Roadmap


# Features
---

- Local Vlan Chat channels
- University Wide Chat Channel
- DMs
- high speed File transfer

# Limitations
---

1. Vlans
	- p2p is allowed, even across Vlans
	- Multicasting And Broadcasting is allowed inside a Vlan
	- broadcasting on a different Vlan is not allowed
	- Cannot send too many p2p packets, server lags
- Users:
	- IP addresses constantly change as users reconnect
	- Cannot put too much strain (storage or compute) on users, as that will cause battery drainage
- Serverless
	- Cannot create persistent storage, must create a psuedo-ephemeral chat

# Roadmap
---

## UDP/TCP:

### 1. Local VLAN Chat

- Send packets to a multicast 
- Everyone listens to the multicast and can also message to it, allowing a simple chat application
- Each message has a message id to avoid duplicates

### 2. Identity and Security (Peer IDs)

- IPs change, so on first install the app create a public/private key pair.
- The public key is also used as an ID to identify the device, regardless of IP changes.
- messages signed using ED25519 algorithm for identity
- The keys are also used for E2E encryption in DMs
### 3. University Wide:

- Use a tracker (simple ESP) with a static IP that saves IP addresses
- Every user provides IP and ID to tracker
- Tracker Selects one supernode for each sub-net
- Users broadcast in their vlan. Supernode then p2p to other supernodes which then UDP broadcast it to their respective sub-net
- If a supernode goes off a new supernode is decided by the tracker and failed packets routed to it

### 4. Pseudo-Persistence:

- The supernode is selected on the basis of stability and number of messages it has.
- new user to vlan broadcasts a ‘New User’ message
- SuperNode Reads this and sends the user the messages it has stored over TCP
- Persistence of upto 100 messages, allowing for good trade off of context.

### 5. Recovery:

- SuperNodes provide a NACK based reliablity system
- SuperNodes broadcast ids of messages 
- Nodes check if they don’t have a certain message, if they don’t they ask for the SuperNode to send it

### 6. Direct Chat and Message Queuing:

- p2p is allowed on the network, even across subnets
- Simple direct TCP between DM participants
- In case of one being offline, the messages are saved by sender and sent once reciever is online.

### 7. File Sharing:

- use direct TCP for speed.
- Allow users to send files in DMs and other users to accept recieving.



# RoadBlocks
---

## Android

- how to keep process running?
- Permissions required by the app

## ESP

- can it handle the workload with 300 kb ram?
- Bootstrap node for DHT?


# Future Reference
---


## Bootstrap node and Distributed Hash Table(DHT):

- A shared hash table
- the hash table has a method of sharing between users
- Find the IP through the users (Tracker only needed to start the setup)

## Online tracker

- Have the tracker be on supabase/firebase
- Everything else works serverless

