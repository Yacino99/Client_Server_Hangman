from email import message
from socket import *
import sys
import select
from _thread import *
from utils import *
import time
compteurJoueur=0
lancerLaPartie=0



mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(1)

clients=[mysocket]
T = True
def broadcast(msg):
    for client in clients:
        if client != mysocket:
            send(client,str(msg))


def remove(connection):
    if connection in clients:
        clients.remove(connection)

def chatThread(socket,addr, pseudo):
    print("chatThread: "+pseudo)
    MessageDebut = "Bienvenu sur notre chat! Votre pseudo est: "+pseudo+"\n"
    send(socket,MessageDebut)
    while True:
        msg = socket.recv(1024)
        msg = msg.decode()
        print(msg)
        message = pseudo+":"
        messageTest = message+msg
        print(messageTest)
        broadcast(messageTest)

def countdown(num_of_secs):
    global lancerLaPartie
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        print(min_sec_format, end='/r')
        time.sleep(1)
        num_of_secs -= 1
    lancerLaPartie = 1
    print('Lancer la partie!.')

def twoPlayerThread(c, port):
    if lancerLaPartie:
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
        gagne = False
        lost = False
        messageQuitter  = "appuyer sur ENTRER pour quitter"
        while (nbVie > 0 and not gagne)or lost:
            msg = c.recv(1024)
            msg = msg.decode()
            print("le client "+str(port)+" a envoyé : ",msg)
            msg = msg.lower()
            #Verifier la chaine de charactère
            if len(msg)  == 0:
                print("Le client veut partir")
                # n'arrive que si le client est parti
                break
            elif len(msg) == 1 and msg.isalpha():  #test si c'est un char
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
                        send(c,"Bravo vous avez gagné la partie , vous avez trouvé le mot qui était "+wordSelected+" "+messageQuitter)
                        gagne = True
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
                        lost = True
                        send(c,"Vous avez perdu ! \n"+affichagePendu(nbVie+1, tableauAffichagePendu)+messageQuitter)
                        break
                    else:
                        send(c,affichageWrongLetter(nbVie,tableauAffichagePendu,clientCharsSoFar))
            elif len(msg) == len(wordSelected):
                #Cas ou c'est un test
                if msg == wordSelected:
                    #win
                    send(c,"Vous avez gagné ! Bravo ! "+messageQuitter)
                    gagne = True
                else:
                    send(c,"Vous avez totalement perdu car vous avez tenté un tout ou rien et c'etais faux. "+messageQuitter)
                    lost = True
                    break
            else:
                send(c,"Vous avez totalement perdu car votre mot ne fait pas la taille du mot recherché "+messageQuitter)
                lost = True
                #Cas ou il faut renvoyer la demande de char
                break
            if nbVie <= 0:
                send(c,"\nyou died, hasta la vista baby "+messageQuitter)
                break
        if(nbVie > 0 and not lost):
            print("le client a gagné la partie et a fini de jouer")
            messageGainDePartie = "Le client "+str(port)+"a gagné la partie"
            broadcast(messageGainDePartie)
        else:
            print("le client a perdu la partie et a fini de jouer")
            messagePerteDePartie = "Le client "+str(port)+"a perdu la partie"
            broadcast(messagePerteDePartie)




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
    gagne = False
    lost = False
    messageQuitter  = "Votre mot était: "+wordSelected+"\nappuyer sur ENTRER pour quitter"
    while (nbVie > 0 and not gagne)or lost:
        msg = c.recv(1024)
        if not msg:
            c.close()
            sys.exit()

        msg = msg.decode()

      

        print("le client "+str(port)+" a envoyé : ",msg)
        msg = msg.lower()
        #Verifier la chaine de charactère
        if len(msg)  == 0:
            print("Le client veut partir")
            # n'arrive que si le client est parti
            c.close()
            break
        elif len(msg) == 1 and msg.isalpha():  #test si c'est un char
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
                    send(c,"Bravo vous avez gagné la partie , vous avez trouvé le mot qui était "+wordSelected+" "+messageQuitter)
                    gagne = True
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
                    lost = True
                    send(c,"Vous avez perdu ! \n"+affichagePendu(nbVie+1, tableauAffichagePendu)+messageQuitter)
                    break
                else:
                    send(c,affichageWrongLetter(nbVie,tableauAffichagePendu,clientCharsSoFar))
        elif len(msg) == len(wordSelected):
            #Cas ou c'est un test
            if msg == wordSelected:
                #win
                send(c,"Vous avez gagné ! Bravo ! "+messageQuitter)
                
                gagne = True
            else:
                send(c,"Vous avez totalement perdu car vous avez tenté un tout ou rien et c'etais faux. "+messageQuitter)
                lost = True
                break
        else:
            send(c,"Vous avez totalement perdu car votre mot ne fait pas la taille du mot recherché "+messageQuitter)
            lost = True
            #Cas ou il faut renvoyer la demande de char
            break
        if nbVie <= 0:
            send(c,"\nyou died, hasta la vista baby "+messageQuitter)
            break
    if(nbVie > 0 and not lost):
        print("le client a gagné la partie et a fini de jouer")
        print(msg)
        nbVie = 7
        gagne = 1
        lost = 0
        playerThread(c,addr,tailleMot)
            
    else:
        print("le client a perdu la partie et a fini de jouer")
       

def playAgainstServer(c,addr,motCacheDuServeur):
    #Message de présentation du jeu
    MessageDebut = "Bienvenu sur le jeu du Pendu! Veuillez me laisser deviner votre mot!"
    send(c,MessageDebut)


#Fonction qui reset les variable dans le but de pouvoir rejouer.
def reset():
    global lancerLaPartie
    lancerLaPartie=0



def checker(c,addr):
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
            if(lancerLaPartie==0):
                countdown(5)
                compteurJoueur+=1
                print(compteurJoueur)
                broadcast("En attente de joueurs")
                joiningMessage = str(addr[1])+" a rejoint la partie"
                broadcast(joiningMessage)
                twoPlayerThread(c,addr)
            else:
                sendToPort(c,"En attente de joueurs",addr[1])
        elif msg.find("CODE003")!=-1:
            print(msg)
            pseudo = msg.split(":")[1]
            chatThread(c,addr,pseudo)
        elif msg.find("CODE004")!=-1:
            print(msg)
            motCacheDuServeur = msg.split(":")[1]
            playAgainstServer(c,addr,motCacheDuServeur)
        if len(msg) == 0:
            c.close()
            clients.remove(c)


while T: 
    [read,_,_] = select.select(clients,[],[])
    for s in read:
        print(s.fileno())
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
