from socket import *
import sys
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
    if(message_recu.endswith("baby")):
        print("fin de la communication")
        s.close()
        break
    else:
        message = input("> ")
    #cas d'un message envoie vide
    if(message.strip() == "exit" or message.strip() == ""):
        print("au revoir")
        s.close()
        break
    message_bytes = bytes(message, "utf-8")
    sent = s.send(message_bytes)

s.close()