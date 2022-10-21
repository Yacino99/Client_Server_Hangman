from socket import *
import time
import sys
import select
if len(sys.argv) != 3:
    sys.exit(-1)

#Connection socket
host = sys.argv[1]
port = int(sys.argv[2])
s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
s.connect((host, port))


while True:
    message_recu = s.recv(1000)
    message_recu = str(message_recu,'utf-8')
    print(message_recu)
    message = input("> ")
    #cas d'un message envoie vide
    if(message.strip() == "exit" or message.strip() == ""):
        print("au revoir")
        s.close()
        break
    time.sleep(1)
    message_bytes = bytes(message, "utf-8")
    sent = s.send(message_bytes)
"""
while True:
    socket_list = [sys.stdin, s]
    read_sockets, write_sockets, error_sockets = select.select(
        socket_list, [], [])
    for sock in read_sockets:
        if sock == s:
            data = sock.recv(1024)
            if not data:
                print('\nDisconnected from server')
                break
            else:
                print(data.decode())
        else:
            msg =input("> ")
            s.send(bytes(str(msg),'utf-8'))
            
"""



s.close()