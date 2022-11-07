from socket import *
import sys
from utils import *
from _thread import *
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
            pseudo = input("Veuillez choisir votre pseudo!\n")
            send(socket,"CODE003"+":"+pseudo)
            rep = None
        elif rep=="4":
            print("\n Jouer contre le serveur")
            motCaches = input("Veuillez choisir le mot que le serveur doit deviner\n")
            send(socket,"CODE004"+":"+motCaches)
            rep = None
        elif rep=="5":
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



def Sending(c):
    while True:
        message = input("> ")
        if(message.strip() == "exit" or message.strip() == ""):
            print("au revoir")
            s.close()
            #break
        message_bytes = bytes(message, "utf-8")
        sent = s.send(message_bytes)

menu(s)
compteur = 0
while True:
    try:
        message_recu = s.recv(1000)
        message_recu = str(message_recu,'utf-8')
        print(message_recu)
        if compteur == 0:
            start_new_thread(Sending, (s,))
            compteur+=1
    except:
        continue
   
s.close()