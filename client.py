from socket import *
import scapy


team_name = 'smelly_cat'
serverPort = 13117

# create UDP socket
clientSocket = socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Client started, listening for offer requests... ")

# recive message from server
msg_from_server, serverAddress = clientSocket.recvfrom(2048)
print('Received offer from ' + serverAddress + ', attempting to connect...')
clientSocket.close()

# create TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverAddress, serverPort))
clientSocket.send(team_name, + '\n')

clientSocket.close()
