
from socket import *
import sys
#Renvoie le mot "caché" en fonction des lettres déjà trouvés
def lettreTrouve(wordSecret, correctLetters):
    blanks = '_' * len(wordSecret)
    res = ''
    k = -1
    for i in wordSecret:
        k += 1
        if i in correctLetters:
            blanks = blanks[:k]+i+blanks[k+1:]
    for letter in blanks:
        res+=" "+letter
    return res
#Envoyer un message au socketClient
def sent(message):
    message = bytes(str(message), 'utf-8')
    socketClient.send(message)

#Afficher le pendu en fonction de la vie du client
def affichagePendu(vie, tableauAffichagePendu):
    return tableauAffichagePendu.get(vie)


def affichageWrongLetter(nbVie, tableauAffichagePendu,clientCharsSoFar):
    tmpVie = nbVie
    MessageTampon1 = ""
    MessageTampon1 += str(str(affichagePendu((tmpVie+1),tableauAffichagePendu))+"\n")
    MessageTampon1 += "Cette lettre a déjà été utilisé , Essai(s) restant: = "+str(tmpVie)+"\n"
    MessageTampon1 += "Lettres déjà utilisées : "+(",".join(clientCharsSoFar))
    return MessageTampon1

etat7="      _______     \n \
     |       |    \n \
     |            \n \
     |        \\  \n \
     |            \n \
     |            \n \
     |          \n \
     |          \n \
     |            \n \
     |            \n \
     |            \n \
"

etat6="      _______     \n \
           |       |     \n \
         |       _     \n \
         |      / \\  \n \
             |      \\_/  \n \
             |            \n \
              |            \n \
               |            \n \
             |            \n \
                |            \n \
                |            \n \
"

etat5="      _______     \n \
     |       |    \n \
     |       _    \n \
     |      / \\  \n \
     |      \\_/  \n \
     |      _|_   \n \
     |      | | \n \
     |      |_| \n \
     |            \n \
     |            \n \
     |            \n \
"

etat4="      _______     \n \
     |       |    \n \
     |       _    \n \
     |      / \\  \n \
     |      \\_/  \n \
     |      _|_   \n \
     |    / | | \n \
     |   /  |_|  \n \
     |            \n \
     |            \n \
     |            \n \
"

etat3="      _______     \n \
     |       |    \n \
     |       _    \n \
     |      / \\  \n \
     |      \\_/  \n \
     |      _|_   \n \
     |    / | | \\\n \
     |   /  |_|  \\ \n \
     |            \n \
     |            \n \
     |            \n \
"

etat2="      _______     \n \
     |       |    \n \
     |       _    \n \
     |      / \\  \n \
     |      \\_/  \n \
     |      _|_   \n \
     |    / | | \\\n \
     |   /  |_|  \\ \n \
     |     //^     \n \
     |    //        \n \
     |   //         \n \
    "

etat7=    "  _______    \n \
     |       |   \n \
         |       _   \n \
         |      / \\ \n \
         |      \\_/ \n \
             |           \n \
             |           \n \
             |           \n \
             |           \n \
             |           \n \
             |           \n \
    "

etat1=   "  _______     \n\
         |       |    \n\
         |       _    \n\
         |      / \\  \n\
         |      \\_/  \n\
         |      _|_   \n\
         |    / | | \\ \n\
         |   /  |_|  \\ \n\
         |     //^\\\\     \n\
         |    //   \\\\     \n\
         |   //     \\\\    \n\
        "

tableauAffichagePendu = { 
    1 : etat1,
    2 : etat2,
    3 : etat3,
    4 : etat4,
    5 : etat5,
    6 : etat6,
    7 : etat7,
    8 : etat7,

}
    
#Connection socket
mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(1)
(socketClient,_) = mysocket.accept()


#Message de présentation du jeu
Message1 = "Bienvenu sur le jeu du Pendu! Veuillez saisir un char pour jouer au Pendu!"
sent(Message1)

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
while nbVie > 0 and not gagne:
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
                sent("Bravo vous avez gagné la partie , vous avez trouvé le mot qui était "+wordSelected)
                gagne = True
            MessageWin +=lettreTrouve(wordSelected, alreadyUsedLetter)
            MessageWin +=" Pendu : Vie restante: "
            MessageWin += str(nbVie)+"\n"
            MessageWin += "Lettres déjà utilisées : "+(",".join(clientCharsSoFar))
            sent(MessageWin)
        elif msg in alreadyUsedLetter:
            #Cas ou la lettre est dans le mot, mais elle est déjà utilsiée
            nbVie -=1
            clientCharsSoFar+=msg
            sent(affichageWrongLetter(nbVie,tableauAffichagePendu,clientCharsSoFar))
        else:
            nbVie -=1
            clientCharsSoFar+=msg
            sent(affichageWrongLetter(nbVie,tableauAffichagePendu,clientCharsSoFar))
    elif len(msg) == len(wordSelected):
        #Cas ou c'est un test
        if msg == wordSelected:
            #win
            sent("Vous avez gagné ! Bravo !")
            gagne = True
        else:
            sent("Vous avez totalement perdu car vous avez tenté un tout ou rien et c'etais faux.")
            break
    else:
        sent("Vous avez totalement perdu car votre mot ne fait pas la taille du mot recherché")
        #Cas ou il faut renvoyer la demande de char
        break
    if nbVie <= 0:
        sent("\nyou died, hasta la vista baby")
    
    #sent(affichagePendu(nbVie,tableauAffichagePendu))

if(nbVie > 0):
    print("le client a gagné la partie et a fini de jouer")
else:
    print("le client a perdu la partie et a fini de jouer")
    

socketClient.close()
mysocket.close()