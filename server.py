from socket import *
import scapy
import time
import struct
import threading
import random
import concurrent.futures

### GLOBALS ###
clients = {}  # dictionary. {team_name: clientSocket}
group1 = []
group2 = []
group1_score = 0
group2_score = 0

def start_udp_server(port):
    """
    create and return UDP socket for broadcasting
    """
    print('starting udp server')
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
    print('starting tcp server')
    TCPServerSocket = socket(AF_INET, SOCK_STREAM)
    TCPServerSocket.bind(("localhost", port))
    TCPServerSocket.settimeout(10)
    TCPServerSocket.listen(10)
    return TCPServerSocket


def accept_clients(socket):
    """
    accept clients
    """
    timer = time.time() + 10
    while time.time() < timer:
        try:
            clientSocket, clientAddress = socket.accept()
            team_name = clientSocket.recv(1024).decode()
            if team_name and clientSocket:
                print('client: ' + team_name)
                clients[team_name] = clientSocket
                assign_group(team_name)
        except:
            pass


def assign_group(team_name):
    """
    assign a team to a random group
    """
    n = random.randint(1, 3)
    if n == 1:
        print('added ' + team_name + ' to group 1')
        group1.append(team_name)
    else:
        print('added ' + team_name + ' to group 2')
        group2.append(team_name)


def broadcast_announcements(socket, udp_port, tcp_port):
    """
    send 10 broadcast announcments over UDP. one every second.
    """
    for i in range(10):
        print('broadcast #' + str(i))
        msg = struct.pack('Ibh', 0xfeedbeef, 0x2, tcp_port)
        socket.sendto(msg, ('<broadcast>', udp_port))
        time.sleep(1)
    socket.close()


def generate_welcome_message():
    welcome_message = 'Welcome to Keyboard Spammers!\n'
    welcome_message += 'Group 1:\n==\n'
    for team in group1:
        welcome_message += team
    welcome_message += 'Group 2:\n==\n'
    for team in group2:
        welcome_message += team
    welcome_message += '\nStart pressing keys on your keyboard as fast as you can!!'
    return welcome_message


def listen_to_your_client(socket, limit):
    print('Listening to your client for ' + str(limit - time.time()) + ' seconds')
    counter = 0
    while time.time() < limit:
        socket.recv(28)
        print('X')
        counter += 1
    print('Done listening to your client. ' + str(counter))
    return counter


def start_game():
    global group1_score
    global group2_score
    print('Game started!')
    welcome_message = generate_welcome_message()
    decoded = welcome_message.encode()
    time_limit = time.time() + 10
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for team in clients:
            clients[team].send(decoded)
            t = executor.submit(listen_to_your_client, clients[team], time_limit)
            c = t.result()
            if team in group1:
                group1_score += c
            else:
                group2_score += c


udpServerPort = 13117
tcpServerPort = 2099

udpServerSocket = start_udp_server(udpServerPort)
tcpServerSocket = start_tcp_server(tcpServerPort)

t1 = threading.Thread(target=broadcast_announcements, args=(udpServerSocket, udpServerPort, tcpServerPort, ))
t2 = threading.Thread(target=accept_clients, args=(tcpServerSocket, ))

t1.start()  # broadcast announcements
t2.start()  # accepting clients and assigning groups
t1.join()
t2.join()

t3 = threading.Thread(target=start_game())
t3.start()

print('Group 1: ' + str(group1_score) + '. Group 2: ' + str(group2_score))
