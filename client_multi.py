from socket import *
import sys
import threading
import _thread

from utils import *
from _thread import *
quit = 0    

if len(sys.argv) != 3:
    sys.exit(-1)
def menu(socket):
    rep=True
    while rep:
        print("""
        1.Jouer au pendu 1 Joueur
        2.Jouer au pendu N joueurs
        3.Chat
        4.Exit/Quit
        5.Jouer au pendu chronométré
        """)
        rep=input("Que voulez-vous faire? ")
        if rep=="1":
            print("\nPendu 1J")
            tailleMot: str = input("Veuillez choisir la taille du mot entre 3 et 9: ")
            if tailleMot.isnumeric() and int(tailleMot)>2 and int(tailleMot)<10:
                send(socket,"CODE001:"+tailleMot)
                rep = None
            else: 
                print("Veuillez entrer une taille valide (entre 3 et 9 compris\n")
                rep = 1
        elif rep=="2":
            print("\n Pendu NJ")
            send(socket,"CODE002")
            rep = None
        elif rep=="3":
            print("\n Chat")
            pseudo = input("Veuillez choisir votre pseudo!\n")
            send(socket,"CODE003"+":"+pseudo)
            rep = None
        elif rep=="4":
            print("\n Quitter") 
            rep = None
            socket.close()
            sys.exit()
        elif rep=="5":
            tailleMot: str = input("Veuillez choisir la taille du mot entre 3 et 9: ")
            if tailleMot.isnumeric() and int(tailleMot)>2 and int(tailleMot)<10:
                send(socket,"CODE010:"+tailleMot)
            rep = None
        else:
            print("\n Veuillez selectionner un choix valide")
#Connection socket
host = sys.argv[1]
port = int(sys.argv[2])
s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
s.connect((host, port))



def Sending(c):
    global quit
    while True:
        message = input("> ")
        if(message.strip() == "exit"):
            print("Au revoir")
            quit = 1
            c.close()
            sys.exit
        else:
            message_bytes: bytes = bytes(message, "utf-8")
            c.send(message_bytes)

menu(s)
compteur = 0
while True:
    if(quit==0):
        try:
            message_recu = s.recv(1000)
            if not message_recu:
                s.close()
                sys.exit()
            message_recu = str(message_recu,'utf-8')
            if(message_recu in "quitter"):
                quit = 1
            elif message_recu:
                print(message_recu)
            if compteur == 0:
                thread = start_new_thread(Sending, (s,))
                compteur+=1
        except:
            continue
    else:
        s.close()
        sys.exit()
