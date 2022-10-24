from email import message
from socket import *
import sys
import select

mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(1)

clients=[mysocket]
T = True

def send(socket, msg):
     socket.send(bytes(msg,'utf-8'))

portSocket = "-1"
compteur = -1
while T: 
    [read,_,_] = select.select(clients,[],[])
    for s in read:
        compteur+=1
        if s == mysocket:  
            (socketclient,addr) = s.accept()
            clients.append(socketclient)
            portSocket = addr[1]
            messageIdentifiant = str(compteur)+":"+str(portSocket)
            send(socketclient, "identifiants:"+messageIdentifiant)

        else:
            msg = s.recv(1000)
            message = str(msg, 'utf-8')
            if len(msg) == 0:
                s.close()
                clients.remove(s)

for z in clients:
    z.close()

mysocket.close()
