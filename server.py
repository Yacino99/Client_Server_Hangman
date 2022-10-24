
from socket import *
import sys
from utils import *
#Renvoie le mot "caché" en fonction des lettres déjà trouvés
    
#Connection socket
mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(1)
(socketClient,_) = mysocket.accept()

#message pour indiquer au client qu'il faut appuyer sur entrer pour fermer le socket de sont coté
messageQuitter  = "appuyer sur ENTRER pour quitter"

#Message de présentation du jeu
Message1 = "Bienvenu sur le jeu du Pendu! Veuillez saisir un char pour jouer au Pendu!"
send(socketClient, Message1)

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
while (nbVie > 0 and not gagne)or lost:
    msg = socketClient.recv(1024)
    msg = msg.decode()
    print("le client a envoyé : ",msg)
    msg = msg.lower()
    #Verifier la chaine de charactère
    if len(msg)  == 0:
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
                send(socketClient,"Bravo vous avez gagné la partie , vous avez trouvé le mot qui était "+wordSelected+" "+messageQuitter)
                gagne = True
            MessageWin +=lettreTrouve(wordSelected, alreadyUsedLetter)
            MessageWin +=" Pendu : Vie restante: "
            MessageWin += str(nbVie)+"\n"
            MessageWin += "Lettres déjà utilisées : "+(",".join(clientCharsSoFar))
            send(socketClient,MessageWin)
        else:
            #Cas ou la lettre est dans le mot, mais elle est déjà utilsiée
            clientCharsSoFar+=msg
            nbVie -=1
            if(nbVie <= 0):
                lost = True
                send(socketClient,"Vous avez perdu ! \n"+affichagePendu(nbVie+1, tableauAffichagePendu)+messageQuitter)
                break
            else:
                send(socketClient,affichageWrongLetter(nbVie,tableauAffichagePendu,clientCharsSoFar))
    elif len(msg) == len(wordSelected):
        #Cas ou c'est un test
        if msg == wordSelected:
            #win
            send(socketClient,"Vous avez gagné ! Bravo ! "+messageQuitter)
            gagne = True
        else:
            send(socketClient,"Vous avez totalement perdu car vous avez tenté un tout ou rien et c'etais faux. "+messageQuitter)
            lost = True
            break
    else:
        send(socketClient,"Vous avez totalement perdu car votre mot ne fait pas la taille du mot recherché "+messageQuitter)
        lost = True
        #Cas ou il faut renvoyer la demande de char
        break
    if nbVie <= 0:
        send(socketClient,"\nyou died, hasta la vista baby "+messageQuitter)
        break
    
    #sent(affichagePendu(nbVie,tableauAffichagePendu))

if(nbVie > 0 and not lost):
    print("le client a gagné la partie et a fini de jouer")
else:
    print("le client a perdu la partie et a fini de jouer")
    

socketClient.close()
mysocket.close()