#Fichier contenant nos fonctions

import random

def sendToPort(socket, msg, port):
    socket.sendto(bytes(msg,'utf-8'), ("127.0.0.1",int(port)))

def send(socket, msg):
     socket.send(bytes(msg,'utf-8'))


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
     |            \n \
     |            \n \
     |            \n \
     |          \n \
     |          \n \
     |            \n \
     |            \n \
     |            \n \
"

etat6="      _______     \n \
     |       |    \n \
     |       _    \n \
     |      / \\  \n \
     |      \\_/  \n \
     |            \n \
     |          \n \
     |          \n \
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
}

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


def importMotFichier(n):
    liste_mots = []
    n = int(n)
    with open('mots.txt') as f:
        for line in f.readlines():
            if(len(line.strip()) == n):
                liste_mots.append(line)
    taille_liste = len(liste_mots)
    mot_choisi = liste_mots[random.randint(0, taille_liste-1)] 
    return mot_choisi.lower().strip()

