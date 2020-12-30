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

def start_udp_server(ip_address, port):
    """
    create and return UDP socket for broadcasting
    """
    print('starting udp server')
    UDPserverSocket = socket(AF_INET, SOCK_DGRAM)
    UDPserverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    UDPserverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPserverSocket.settimeout(0.2)
    print('listening on IP address ' + ip_address)
    return UDPserverSocket


def start_tcp_server(ip_address, port):
    """
    create and return a TCP socket
    """
    print('starting tcp server')
    TCPServerSocket = socket(AF_INET, SOCK_STREAM)
    TCPServerSocket.bind((ip_address, port))
    TCPServerSocket.settimeout(10)
    TCPServerSocket.listen()
    return TCPServerSocket


def accept_clients(socket):
    """
    accept clients
    """
    timer = time.time() + 10
    while time.time() < timer:
        try:
            clientSocket, clientAddress = socket.accept()
            team_name = clientSocket.recv(1024).decode('utf-8')
            if team_name and clientSocket:
                print(team_name[:len(team_name) - 1] + ' has joined')
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
        print(team_name[:len(team_name) - 1] + ' was added to group 1')
        group1.append(team_name)
    else:
        print(team_name[:len(team_name) - 1] + ' was added to group 2')
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
    counter = 0
    while time.time() < limit:
        socket.recv(28)
        counter += 1
    print('Done listening to your client. ' + str(counter))
    return counter


def start_game():
    global group1_score
    global group2_score
    print('Game started!')
    welcome_message = generate_welcome_message()
    print(welcome_message)
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


def calculate_winners_message():
    global group1_score
    global group2_score
    msg = '====================\nGame over!\n'
    if group1_score > group2_score:
        winner = 'Group 1'
        score = group1_score
    else:
        winner = 'Group 2'
        score = group2_score
    msg += 'Group 1 typed in ' + str(group1_score) + ' characters. Group 2 typed in ' + str(group2_score) + ' characters.\n'
    msg += winner + ' wins!\n\n'
    msg += 'Congratulations to the winners:\n==\n'
    if winner == 'Group 1':
        for team in group1:
            msg += team
    if winner == 'Group 2':
        for team in group2:
            msg += team + '======================\n'
    return msg        


def send_results_to_clients():
    results_msg = calculate_winners_message()
    print(results_msg)
    for team in clients:
        clients[team].send(results_msg.encode())


def run_server():
    global clients
    global group1
    global group2
    global group1_score
    global group2_score

    ip_address = '192.168.0.42'
    udpServerPort = 13117
    tcpServerPort = 2099

    udpServerSocket = start_udp_server(ip_address, udpServerPort)
    tcpServerSocket = start_tcp_server(ip_address, tcpServerPort)

    t1 = threading.Thread(target=broadcast_announcements, args=(udpServerSocket, udpServerPort, tcpServerPort, ))
    t2 = threading.Thread(target=accept_clients, args=(tcpServerSocket, ))

    t1.start()  # broadcast announcements
    t2.start()  # accepting clients and assigning groups
    t1.join()
    t2.join()

    t3 = threading.Thread(target=start_game())
    t3.start()
    t3.join()

    send_results_to_clients()

    clients = {}
    group1 = []
    group2 = []
    group1_score = 0
    group2_score = 0

while True:
    run_server()
