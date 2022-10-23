from socket import *
import time
import sys
import select
def send(socket, msg):
     socket.send(bytes(msg,'utf-8'))

if len(sys.argv) != 3:
    sys.exit(-1)

host = sys.argv[1]
port = int(sys.argv[2])
mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
myself = gethostname()
mysocket.connect((host, port))

rcv = [sys.stdin , mysocket]
identite = ""
pseudo = ""
T = True
while T:
    [read,_,_] = select.select(rcv,[],[])
    if sys.stdin in read:
        msg = sys.stdin.readline()
        if msg == "FIN\n":
            T = False
        if len(msg)==5:
            identite = msg
        if(identite!=""):
            msg = identite + " : " + msg
            send(mysocket,msg)
        else :
            msg = myself + " : " + msg
            message = bytes(msg, "utf-8")
            sent = mysocket.send(message)

        if pseudo != "":
            pseudo = input("\nVeuillez choisir votre pseudo")
            sent = send(mysocket, "Mon pseudo est "+pseudo)


    if mysocket in read :

        
        message= mysocket.recv(1000)
        msg = str(message,"utf-8")

        if len(msg)==5:
            identite = msg 
        print(msg)
#fermeture du socket server
mysocket.close()
