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

def broadcast(clients, msg):
    for i in clients:
        if i != mysocket:
            send(i,str(msg))

def sendToPort(socket, msg, port):
    socket.sendto(bytes(msg,'utf-8'), ("127.0.0.1",int(port)))

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
            portSocket = addr[1]
            msg = s.recv(1000)
            message = str(msg, 'utf-8')
            if len(msg) == 0:
                s.close()
                clients.remove(s)
            else:
                #Message speciique
                sendToPort(s,message+" envoyé à un port specifique",portSocket)

                #Broadcast
                broadcast(clients, message+" envoyé en broadcast")
for z in clients:
    z.close()

mysocket.close()
