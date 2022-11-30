from email import message
from socket import *
import sys
import select
from _thread import *
from utils import *
import time
import datetime
compteurJoueur=0
lancerLaPartie=0
lobby = 0
hostGame = 0
tempsDebutPartie = 0
host = 0
compteurFini = 0
viePartieGagnante = -100


def resetVariables():
    global compteurJoueur
    global lancerLaPartie
    global lobby
    global hostGame
    global tempsDebutPartie
    global host
    global compteurFini
    global viePartieGagnante
    compteurJoueur = 0
    lancerLaPartie = 0
    lobby = 0
    hostGame = 0
    tempsDebutPartie = 0
    host = 0
    compteurFini = 0
    viePartieGagnante = -100

mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(1)
clientsNJ=[mysocket]

clients=[mysocket]
T = True

#Envoie un message a tout les sockets connectés
def broadcast(msg):
    for client in clients:
        if client != mysocket:
            send(client,str(msg))



#Supprime une connection au socket
def remove(connection):
    if connection in clients:
        clients.remove(connection)


#Fonction gérant le chat
def chatThread(socket,addr, pseudo):
    print("chatThread: "+pseudo)
    MessageDebut = "Bienvenu sur notre chat! Votre pseudo est: "+pseudo+"\n"
    send(socket,MessageDebut)
    while True:
        msg = socket.recv(1024)
        #Si not msg, on ferme le socket.
        if not msg:
            socket.close()
            sys.exit()
        msg = msg.decode()
        #Parsing du message
        message = pseudo+":"
        messageTest = message+msg

        print(str(addr[1])+":"+messageTest)
        #Broadcast du message
        broadcast(messageTest)

#Menu gèrer côté serveur pour gérer le replay multijoueurs
def menu(c, port) -> None:
    #On reset toute les variables
    send(c,"""\n
            1.Jouer au pendu 1 Joueur
            2.Jouer au pendu N joueurs
            3.Chat
            4.Exit/Quit
            """)
    while True:
        msg = c.recv(1024)
        msg = msg.decode()
        rep = msg         

        if not msg:
            c.close()
            sys.exit()
        if rep=="1":
            print("\nPendu 1J")
            checker2(c,port,"CODE001")
            break
        elif rep=="2":
            print("\n Pendu NJ")
            checker2(c,port,"CODE002")
            break
        elif rep=="3":
            print("\n Chat")
            checker2(c,port,"CODE003")
            break            
        elif rep=="4":
            print("\n Quitter") 
            send(c,"quitter")
        else:
            send(c,"\n Veuillez selectionner un choix valide")
    



#Gestion d'une fin de partie multijoueur
def endGame(c,port, vie, gagne):
    global compteurFini
    global compteurJoueur
    global viePartieGagnante
    compteurFini+=1
    print("endGame")
    send(c,"\nEn attente que les joueurs aient finit leur partie eux aussi...")
    while True:
        #Si tout les joueurs ont finit leur parties
        if(compteurFini==compteurJoueur):
            #Cas ou il n'a pas trouvé le mot
            if gagne == 0:
                sendToPort(c,"\nVous avez perdu la partie",str(port[1]))
            #Cas ou il a trouvé le mot
            elif gagne == 1:
                sendToPort(c,"\n"+str(port[1])+" ,vous avez trouvé le bon mot, il vous restait: "+str(vie)+" vie",port[1])
            #Cas ou il a trouvé le mot, et qu'il a le nombre de vie mini
            if viePartieGagnante==vie:
                broadcast("\nLe joueur "+str(port[1])+" a gagné la partie")
            
            resetVariables()
            time.sleep(5)
            #Retour au menu
            menu(c,port)


#Fonction gèrant les N joueurs sur une partie
def twoPlayerThread(c, port):
    global host
    global viePartieGagnante
    global compteurJoueur

    #Attente de la fin du compteur pour le début de la partie
    while True:
        if host == 1:
            print(host)
            break
    #Fin du compteur: la partie peut débuter
    if host == 1:
        print("twoPlayerThread")
        MessageDebut = "Bienvenu sur le jeu du Pendu en version 2 joueurs! Veuillez saisir un char pour jouer au Pendu!"
        send(c,MessageDebut)
        #Mot selectionner pour le jeu du Pendu
        wordSelected = "Bateau"
        wordSelected = wordSelected.lower()

        #Tampon pour le mot "gagnant"
        tampon = wordSelected

        #Lettres valide utilisés
        alreadyUsedLetter = ""
        #Toutes les lettres utilisés
        clientCharsSoFar = ""
        #Nombre de vie du client
        nbVie = 7
        while True:
            msg = c.recv(1024)
            if not msg:
                compteurJoueur-=1
                c.close()
                sys.exit()

          

            msg = msg.decode()

        

            print("le client "+str(port)+" a envoyé : ",msg)
            msg = msg.lower()
            if len(msg) == 1 and msg.isalpha():  #test si c'est un char
                #Cas ou y a un seul charactère 
                print ("Tu as envoye un charatères : ",msg)
                #Liste des char déjà utilisé
                if msg not in alreadyUsedLetter and msg in wordSelected:
                #Bingo: bonne lettre
                    MessageWin = "Bien joué! Vous avez trouver une lettre "
                    clientCharsSoFar += msg
                    tampon = tampon.replace(msg,"")
                    alreadyUsedLetter+=msg
                    print("tampon : "+tampon)
                    if tampon=="":
                        send(c,"Bravo vous avez gagné la partie , vous avez trouvé le mot qui était "+wordSelected)
                        #Un minimum > 0 globale pour déterminer le gagnant
                        if(nbVie>viePartieGagnante):
                            viePartieGagnante = nbVie
                            print(viePartieGagnante)
                        #Fonction fin de partie
                        endGame(c,port,nbVie, 1)
                    MessageWin +=lettreTrouve(wordSelected, alreadyUsedLetter)
                    MessageWin +=" Pendu : Vie restante: "
                    MessageWin += str(nbVie)+"\n"
                    MessageWin += "Lettres déjà utilisées : "+(",".join(clientCharsSoFar))
                    send(c,MessageWin)
                else:
                    #Cas ou la lettre est dans le mot, mais elle est déjà utilsiée
                    clientCharsSoFar+=msg
                    nbVie -=1
                    if(nbVie <= 0):
                        send(c,"Vous avez perdu ! \n"+affichagePendu(nbVie+1, tableauAffichagePendu))
                        endGame(c,port,nbVie, 0)
                    else:
                        send(c,affichageWrongLetter(nbVie,tableauAffichagePendu,clientCharsSoFar))
            elif len(msg) == len(wordSelected):
                #Cas ou c'est un test
                if msg == wordSelected:
                    #win
                    send(c,"Vous avez gagné ! Bravo !")
                    if(nbVie>viePartieGagnante):
                        viePartieGagnante = nbVie
                    endGame(c,port,nbVie, 1)
                else:
                    send(c,"Vous avez totalement perdu car vous avez tenté un tout ou rien et c'etais faux. ")
                    nbVie = 0
                    endGame(c,port,nbVie, 0)
            else:
                send(c,"Vous avez totalement perdu car votre mot ne fait pas la taille du mot recherché ")
                #Cas ou il faut renvoyer la demande de char
                nbVie = 0
                endGame(c,port,nbVie, 0)



#Gestion du serveur pendu pour N joueur, partie non multijoueur
def playerThread(c, port, tailleMot):    
    #Message de présentation du jeu
    MessageDebut = "Bienvenu sur le jeu du Pendu! Veuillez saisir un char pour jouer au Pendu!"
    send(c,MessageDebut)
    wordSelected = importMotFichier(tailleMot)
    print("Le mot que le client doit trouver est :"+wordSelected)
    #Tampon pour le mot "gagnant"
    tampon = wordSelected
    #Lettres valide utilisés
    alreadyUsedLetter = ""
    #Toutes les lettres utilisés
    clientCharsSoFar = ""
    #Nombre de vie du client
    nbVie = 7
    messageQuitter  = "Votre mot était: "+wordSelected+"\nEnvoyer REPLAY pour rejouer, exit pour quitter"
    while True:
        msg = c.recv(1024)
        if not msg:
            c.close()
            sys.exit()

        
        msg = msg.decode()
        #Si message = REPLAY on rejoue
        if msg.find("REPLAY")!=-1:
            playerThread(c,port,tailleMot)
        #Sinon jeu du pendu
        else:
            print("le client "+str(port)+" a envoyé : ",msg)
            msg = msg.lower()
            #Cas ou y a un seul charactère 
            if len(msg) == 1 and msg.isalpha():
                #Liste des char déjà utilisé
                #Bingo: bonne lettre
                if msg not in alreadyUsedLetter and msg in wordSelected:
                    MessageWin = "Bien joué! Vous avez trouver une lettre "
                    clientCharsSoFar += msg
                    tampon = tampon.replace(msg,"")
                    alreadyUsedLetter+=msg
                    print("tampon : "+tampon)
                    #Si tampon vide, gain de la partie
                    if tampon=="":
                        send(c,"Bravo vous avez gagné la partie , vous avez trouvé le mot qui était "+wordSelected+" "+messageQuitter)
                    else:
                        MessageWin +=lettreTrouve(wordSelected, alreadyUsedLetter)
                        MessageWin +=" Pendu : Vie restante: "
                        MessageWin += str(nbVie)+"\n"
                        MessageWin += "Lettres déjà utilisées : "+(",".join(clientCharsSoFar))
                        send(c,MessageWin)
                else:
                    #Cas ou la lettre est dans le mot, mais elle est déjà utilsiée
                    clientCharsSoFar+=msg
                    nbVie -=1
                    if(nbVie <= 0):
                       send(c,"Vous avez perdu ! \n"+affichagePendu(nbVie+1, tableauAffichagePendu)+messageQuitter)
                    else:
                       send(c,affichageWrongLetter(nbVie,tableauAffichagePendu,clientCharsSoFar))
            elif len(msg) == len(wordSelected) and msg != "REPLAY":
                #Cas ou c'est un test
                if msg == wordSelected:
                    #win
                    send(c,"Vous avez gagné ! Bravo ! "+messageQuitter)
                else:
                    send(c,"Vous avez totalement perdu car vous avez tenté un tout ou rien et c'etais faux. "+messageQuitter)
            else:
                if(msg!="REPLAY"):
                    send(c,"Vous avez totalement perdu car votre mot ne fait pas la taille du mot recherché "+messageQuitter)       



#Compte a rebours
def countdown(num_of_secs):
    global lancerLaPartie
    global host
    global hostGame
    hostGame = 1
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        print(min_sec_format, end='/r')
        time.sleep(1)
        num_of_secs -= 1
    lancerLaPartie = 1
    host = 1
    print('Lancer la partie!.')

#Fonction checker2 pour la gestion du CODE du menu côté serveur
def checker2(c,addr,CODE):
    global lancerLaPartie
    global hostGame
    global tempsDebutPartie
    global tempsCompteur
    global compteurJoueur
    try:
        msg = c.recv(1024)
    except:
        c.close()
        sys.exit()

    if not msg:
        c.close()
        sys.exit()
    else:
        msg = msg.decode()
        if CODE == "CODE001":
            playerThread(c,addr,6)
        elif CODE == "CODE002":
            compteurJoueur+=1
            clientsNJ.append(c)
            #Etape1: Rejoindre le lobby
            if lancerLaPartie == 0:
                if hostGame == 0:
                    #Si le host join la game
                    #On créé le compteur, pour commencer la partie
                    tempsCompteur = 5
                    tempsDebutPartie = addSecs(datetime.datetime.now().time(),tempsCompteur)
                    sendToPort(c,"En attente de joueurs. \nTemps avant début de la partie: "+str(tempsCompteur)+"s"
                    +"\nLa partie commencera a "+str(tempsDebutPartie),addr[1])
                    countdown(tempsCompteur)
                    twoPlayerThread(c,addr)
                    hostGame=1
                elif hostGame ==1:
                    joiningMessage = str(addr[1])+" a rejoint la partie\n"
                    sendToPort(c,"En attente de joueurs. \nTemps avant début de la partie: "+str(tempsCompteur)+"s"
                    +"\nLa partie commencera a "+str(tempsDebutPartie),addr[1])
                    broadcast(joiningMessage)
                    twoPlayerThread(c,addr)
            else:
                sendToPort(c,"La partie est déjà lancé!",addr[1])
                compteurJoueur-=1
                time.sleep(1)
                menu(c,addr)

       
        elif CODE == "CODE003":
            print(msg)
            chatThread(c,addr,str(addr[1]))
        if len(msg) == 0:
            c.close()
            clients.remove(c)


#fonction qui envoie les sockets vers différents mode de jeu
def checker(c,addr):
    global lancerLaPartie
    global hostGame
    global tempsDebutPartie
    global tempsCompteur
    global compteurJoueur
    try:
        msg = c.recv(1024)
    except:
        c.close()
        sys.exit()

    if not msg:
        c.close()
        sys.exit()
    else:
        msg = msg.decode()
        if msg.find("CODE001")!=-1:
            tailleMot = msg.split(":")[1]
            playerThread(c,addr,tailleMot)
        elif msg in "CODE002":
            compteurJoueur+=1
            #Etape1: Rejoindre le lobby
            if lancerLaPartie == 0:
                if hostGame == 0:
                    #Si le host join la game
                    #On créé le compteur, pour commencer la partie
                    tempsCompteur = 5
                    tempsDebutPartie = addSecs(datetime.datetime.now().time(),tempsCompteur)
                    sendToPort(c,"En attente de joueurs. \nTemps avant début de la partie: "+str(tempsCompteur)+"s"
                    +"\nLa partie commencera a "+str(tempsDebutPartie),addr[1])
                    countdown(tempsCompteur)
                    twoPlayerThread(c,addr)
                    hostGame=1
                elif hostGame ==1:
                    joiningMessage = str(addr[1])+" a rejoint la partie\n"
                    sendToPort(c,"En attente de joueurs. \nTemps avant début de la partie: "+str(tempsCompteur)+"s"
                    +"\nLa partie commencera a "+str(tempsDebutPartie),addr[1])
                    broadcast(joiningMessage)
                    twoPlayerThread(c,addr)
            else:
                sendToPort(c,"La partie est déjà lancé!",addr[1])
                compteurJoueur-=1
                time.sleep(1)
                menu(c,addr)


        elif msg.find("CODE003")!=-1:
            print(msg)
            pseudo = msg.split(":")[1]
            chatThread(c,addr,pseudo)
        if len(msg) == 0:
            c.close()
            clients.remove(c)


#Boucle initial pour la liaison des sockets
while T: 
    [read,_,_] = select.select(clients,[],[])
    for s in read:
        if s == mysocket:
            (socketclient,addr) = mysocket.accept()
            clients.append(socketclient)
            try:
                start_new_thread(checker, (socketclient,addr))
            except:
                clients.remove(socketclient)
        if(s.fileno()<0):
            clients.remove(s)
            s.close()
for z in clients:
    z.close()

mysocket.close()
