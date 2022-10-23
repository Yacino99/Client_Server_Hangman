from socket import *
import sys
import select

def sent(message):
    message = bytes(str(message), 'utf-8')
    mysocket.send(message)



mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(1)

(socketClient,_) = mysocket.accept()
(socketClient2,_) = mysocket.accept()
clients = [ socketClient, socketClient2]   
sent("Test")

while len(clients) > 0:
    [read,_,_] = select.select(clients,[],[])
    for s in read:
        msg = s.recv(1000)
        if len(msg) == 0:
            s.close()
            clients.remove(s)
        else:
            message = str(msg, 'utf-8')
            print(message)
mysocket.close()
