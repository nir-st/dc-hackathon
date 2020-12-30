from socket import *
import scapy
import time
import struct
import threading
import random


clients = {}  # dictionary. {team_name: clientSocket}
group1 = []
group2 = []


def start_udp_server(port):
    """
    create and return UDP socket for broadcasting
    """
    UDPserverSocket = socket(AF_INET, SOCK_DGRAM)
    UDPserverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    UDPserverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPserverSocket.settimeout(0.2)
    print('listening on IP address ' + 'localhost')
    return UDPserverSocket


def start_tcp_server(port):
    """
    create and return a TCP socket
    """
    TCPServerSocket = socket(AF_INET, SOCK_STREAM)
    TCPServerSocket.bind(("localhost", port))
    TCPServerSocket.listen(200)
    return TCPServerSocket


def accept_clients(socket):
    """
    accept clients
    """
    timer = time.time() + 10
    while time.time() < timer:
        clientSocket = socket.accept()
        team_name = clientSocket.recv(1024).decode()
        if team_name and clientSocket:
            clients[team_name] = clientSocket
        assign_group(team_name)


def assign_group(team_name):
    """
    assign a team to a random group
    """
    n = random.randint(1, 3)
    if n == 1:
        group1.append(team_name)
    else:
        group2.append(team_name)


def broadcast_announcements(socket, udp_port, tcp_port):
    """
    send 10 broadcast announcments over UDP. one every second.
    """
    for i in range(10):
        msg = struct.pack('Ibh', 0xfeedbeef, 0x2, tcp_port)
        socket.sendto(msg, ('<broadcast>', udp_port))
        time.sleep(1)
    socket.close()


def generate_welcome_message():
    welcome_message = 'Welcome to Keyboard Spammers!\n'
    welcome_message += 'Group 1:\n=='
    for team in group1:
        welcome_message += team + '\n'
    welcome_message += '\n'
    welcome_message += 'Group 2:\n=='
    for team in group1:
        welcome_message += team + '\n'
    welcome_message += '\nStart pressing keys on your keyboard as fast as you can!!'
    return welcome_message


def start_game():
    welcome_message = generate_welcome_messsage()
    decoded = welcome_message.decode()
    for socket in clients:
        socket.send(decoded)


udpServerPort = 13117
tcpServerPort = 2099

udpServerSocket = start_udp_server(udpServerPort)
tcpServerSocket = start_tcp_server(tcpServerPort)

t1 = threading.Thread(target=broadcast_announcements, args=(udpServerSocket, udpServerPort, tcpServerPort, ))
t2 = threading.Thread(target=accept_clients, args=(tcpServerSocket, ))

t1.start()  # broadcast announcements
t2.start()  # accepting clients and assigning groups
time.sleep(10)
