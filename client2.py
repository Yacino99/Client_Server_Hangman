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
pseudo = "-1"
portSocket = "-1"
identifiant = "-1"
"""if pseudo == "-1":
    print("Veuillez choisir votre Pseudo: ")
    pseudo = input("<")
"""
pseudoAttribution = 0
identifiantAttribution = 0

T = True
while T:
    [read,_,_] = select.select(rcv,[],[])
    if sys.stdin in read:
        msg = sys.stdin.readline()
        if msg == "FIN\n":
            T = False
        else:
            #On attribue le pseudo
           """ if pseudoAttribution == 0:
                message = "CODE001:"+str(pseudo)
               # send(mysocket,message)
                pseudoAttribution = 1
           # else:"""
        messageInput = input("> ")

        if(message.strip() == "exit" or message.strip() == ""):
            print("au revoir")
            mysocket.close()
            break
        send(mysocket, messageInput)
        #sent = mysocket.send("Test jeu")
    if mysocket in read :
        message= mysocket.recv(1000)
        msg = str(message,"utf-8")
        print(msg)
          
#fermeture du socket server
mysocket.close()


"""if identifiantAttribution== 0 and msg.__contains__("identifiant"):
                identifiantTampon = msg.split(":")
                portSocket = identifiantTampon[1]
                identifiant = identifiantTampon[2]
              #  print("Je suis"+portSocket+":"+identifiant)
                identifiantAttribution = 1
            else:

"""