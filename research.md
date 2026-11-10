#FOR THE APP

## Upon starting

**Step 1 (Local Shout):** The app broadcasts a UDP packet to its current VLAN: "WHO_IS_TRACKER?"

**Step 2 (Instant Local Reply):** If anyone (a Supernode or even a normal user) is online in that VLAN, their app automatically replies: "TRACKER_IS_10.7.42.15". Zero internet required!

**Step 3 (Fallback):** If nobody replies after 2 seconds (meaning you are the very first person on that VLAN), the app checks the hardcoded last-known IP, or checks the GitHub Gist to find the ESP32.


#FOR THE TRACKER
An ESP32 can only handle 10-16 connections over TCP at a time, with UDP it can do thousands of packets. So any and all communication with the tracker should be done through UDP packets. For supernode checking we will use constant 'awake' pings.
