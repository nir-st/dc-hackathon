from socket import *
import scapy
import time
import struct
import threading



def start_udp_server(port):
    """
    create UDP socket for broadcasting
    """
    UDPserverSocket = socket(AF_INET, SOCK_DGRAM)
    UDPserverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    UDPserverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPserverSocket.settimeout(0.2)
    print('listening on IP address ' + ipaddress)
    return UDPserverSocket


def start_tcp_server(port):
    """
    create TCP socket
    """
    TCPServerSocket = socket(AF_INET, SOCK_STREAM)
    TCPServerSocket.bind(("localhost", port))
    TCPServerSocket.listen(200)
    return TCPServerSocket


def accept_clients(socket):
    clients = {}
    timer = time.time() + 10
    while time.time() < timer:
        clientSocket = socket.accept()
        print('client accepted!')
        team_name = clientSocket.recv(1024).decode()
        if team_name and clientSocket:
            clients[team_name] = clientSocket
    return clients


def broadcast_announcements(socket, udp_port, tcp_port):
    """
    send 10 broadcast announcments over UDP every second
    """
    print('Starting to broadcast')
    for i in range(10):
        print('sending message ' + str(i+1))
        msg = struct.pack('Ibh', 0xfeedbeef, 0x2, tcp_port)
        socket.sendto(msg, ('<broadcast>', udp_port))
        print("message sent")
        time.sleep(1)
    socket.close()


ipaddress = '127.0.0.1'
udpServerPort = 13117
tcpServerPort = 2099

udpServerSocket = start_udp_server(udpServerPort)
tcpServerSocket = start_tcp_server(tcpServerPort)

t1 = threading.Thread(target=broadcast_announcements, args=(udpServerSocket, udpServerPort, tcpServerPort, ))
t2 = threading.Thread(target=accept_clients, args=(tcpServerSocket, ))
t1.start()
t2.start()

