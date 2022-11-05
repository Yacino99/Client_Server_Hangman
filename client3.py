from socket import *
import sys
from utils import *

if len(sys.argv) != 3:
    sys.exit(-1)



def menu(socket):
    rep=True
    while rep:
        print("""
        1.Jouer au pendu 1 Joueur
        2.Jouer au pendu 2 joueurs
        3.Chat
        4.Exit/Quit
        """)
        rep=input("Que voulez-vous faire? ")
        if rep=="1":
            print("\nPendu 1J")
            send(socket,"CODE001")
            rep = None
        elif rep=="2":
            print("\n Pendu 2J")
            send(socket,"CODE002")
            rep = None
        elif rep=="3":
            print("\n Chat")
            pseudo = input("Veuillez choisir votre pseudo!")
            send(socket,"CODE003"+":")
            rep = None
        elif rep=="4":
            print("\n Quitter") 
            rep = None
            socket.close()
            break
        else:
            print("\n Veuillez selectionner un choix valide")
#Connection socket
host = sys.argv[1]
port = int(sys.argv[2])
s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
s.connect((host, port))

menu(s)
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
    message_bytes = bytes(message, "utf-8")
    sent = s.send(message_bytes)
s.close()