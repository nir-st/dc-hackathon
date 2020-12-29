import socket
import scapy


ipaddress = '127.0.0.1'
serverPort = 13117

# create UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind('', serverPort)
serverSocket.sendto('listening on IP address ' + ipaddress('<broadcast>', serverPort))

# send 10 broadcast announcments every second
for i in range(10):
    serverSocket.sendto('listening on IP address ' + ipaddress, ('<broadcast>', serverPort))
    time.sleep(1)
    