from socket import *
import scapy
import struct


def startUdpSocket(port):
    """
    Create UDP socket and receive message
    """
    UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
    UDPclientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPclientSocket.bind(('', port))
    print("Client started, listening for offer requests... ")
    
    # recive message from server
    msg_from_server, serverAddress = UDPclientSocket.recvfrom(28)
    msg = struct.unpack('Ibh', msg_from_server)
    if msg[0] != 0xfeedbeef or msg[1] != 0x2:
        print('unvalid message received from server: ' + str(msg))
        return False
    port = msg[2]
    UDPclientSocket.close()
    return (serverAddress[0], port)


def createTcpSocket(server_ip, port, team_name):
    """
    create TCP socket
    """
    TCPclientSocket = socket(AF_INET, SOCK_STREAM)
    TCPclientSocket.connect(("localhost", port))
    TCPclientSocket.send((team_name +  '\n').encode())


team_name = 'smelly_cat'
serverPort = 13117

while True:
    serverAns = startUdpSocket(serverPort)
    if serverAns != False:
        serverIp = serverAns[0]
        tcpServerPort = serverAns[1]
        createTcpSocket(serverIp, tcpServerPort, team_name)
