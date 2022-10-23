from socket import *
import struct
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


while T: 
    [read,_,_] = select.select(clients,[],[])
    for s in read:  
        if s == mysocket:  
            (socketclient,addr) = s.accept()
            clients.append(socketclient) 
            namesocket = addr
        else:
            msg = s.recv(1000)
            message = str(namesocket)+":"
            message += str(msg, 'utf-8')
            print("SERVER: "+message)
            if len(msg) == 0:
                s.close()
                clients.remove(s)
            else:
                # On écrit cela dans le but de retransmettre le message: 
                for i in clients:
                  if i != s and i != mysocket:
                    i.send(bytes(message,'utf-8'))
for z in clients:
    z.close()

mysocket.close()
