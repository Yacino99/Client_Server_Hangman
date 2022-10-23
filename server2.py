from socket import *
import sys
import select
mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(1)

clients=[mysocket]
T = True
while T: 
    [read,_,_] = select.select(clients,[],[])
    for s in read:    
        if s == mysocket:  
            (socketclient,_) = s.accept()
            clients.append(socketclient) 
        else:
            msg = s.recv(1000)
            message = str(msg, 'utf-8')
            if len(msg) == 0 or message[-4:-1] == "FIN":
                s.close()
                clients.remove(s)
            else:
                print(message)
                # On écrit cela dans le but de retransmettre le message: 
                for i in clients:
                    if i != s and i != mysocket:
                        i.send(bytes(message, 'utf-8'))

for z in clients:
    z.close()

mysocket.close()
