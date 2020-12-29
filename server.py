from socket import *
import scapy
import time


ipaddress = '127.0.0.1'
serverPort = 13117

# create UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print('listening on IP address ' + ipaddress)

# send 10 broadcast announcments every second
for i in range(10):
    msg = '0xfeedbeef'
    serverSocket.send(msg.encode(), ('<broadcast', serverPort))
    time.sleep(1)
