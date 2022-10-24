from email import message
from socket import *
import sys
import select
from _thread import *
from utils import *
mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(1)

clients=[mysocket]
T = True

def playerThread(c):
    #Message de présentation du jeu
    MessageDebut = "Bienvenu sur le jeu du Pendu! Veuillez saisir un char pour jouer au Pendu!"
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
    partie = True
    lost = False
    messageQuitter  = "appuyer sur ENTRER pour quitter"

    while (nbVie > 0 and not gagne)or lost:
        msg = c.recv(1024)
        msg = msg.decode()
        print("le client a envoyé : ",msg)
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
        
        #sent(affichagePendu(nbVie,tableauAffichagePendu))

    if(nbVie > 0 and not lost):
        print("le client a gagné la partie et a fini de jouer")
    else:
        print("le client a perdu la partie et a fini de jouer")



portSocket = "-1"
compteur = -1
while T: 
    [read,_,_] = select.select(clients,[],[])
    for s in read:
        compteur+=1
        if s == mysocket:  
            (socketclient,addr) = s.accept()
            clients.append(socketclient)
            portSocket = addr[1]
            #messageIdentifiant = str(compteur)+":"+str(portSocket)
            #send(socketclient, "identifiants:"+messageIdentifiant)
            start_new_thread(playerThread, (socketclient,))
        else:
            portSocket = addr[1]
            msg = s.recv(1000)
            message = str(msg, 'utf-8')
            if len(msg) == 0:
                s.close()
                clients.remove(s)
          #  else:
                #Message speciique
                #sendToPort(s,message+" envoyé à un port specifique",portSocket)

                #Broadcast
              #  broadcast(clients, message+" envoyé en broadcast")
for z in clients:
    z.close()

mysocket.close()
