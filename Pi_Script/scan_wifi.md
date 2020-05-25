```
#!/bin/bash

function scan_wifi() {
	local bandwidth=$1
	local channel=$2

	local chanSpec=$(mcp -C 1 -N 1 -c "$channel/$bandwidth")

	pkill wpa_supplicant
	ifconfig wlan0 up

	nexutil -Iwlan0 -s500 -b -l34 "-v$chanSpec"

	# setting up monitor fails when it already exists. Can be happily ignored.
	iw phy `iw dev wlan0 info | gawk '/wiphy/ {printf "phy" $2}'` interface add mon0 type monitor 2> /dev/null
	ifconfig mon0 up
}

scanwifi 80 161
timeout 10 tcpdump -i wlan0 dst port 5500 -c 10000 -w "./scans/test_80_161.pcap"
```