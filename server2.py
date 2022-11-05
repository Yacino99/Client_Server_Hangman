from email import message
from socket import *
import sys
import select
from _thread import *
from utils import *
mysocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

port = int(sys.argv[1])
mysocket.bind(('',port))
mysocket.listen(5)

clients=[mysocket]
T = True
def broadcast(clients, msg):
    for i in clients:
        if i != mysocket:
            send(i,str(msg))

def chatThread(socket, client, pseudo):
    print("chatThread: "+pseudo)
    MessageDebut = "Bienvenu sur notre chat! Votre pseudo est: "+pseudo+"\n"
    send(socket,MessageDebut)

    
    while True:
        msg = socket.recv(1024)
        message = pseudo+":"
        messageTest = message+str(msg,'utf-8')+"\n"
        broadcast(client,messageTest)


def playerThread(c, port):
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
        
        #sent(affichagePendu(nbVie,tableauAffichagePendu))

    if(nbVie > 0 and not lost):
        print("le client a gagné la partie et a fini de jouer")
    else:
        print("le client a perdu la partie et a fini de jouer")



portSocket = "-1"
compteur = -1
Jeu = 0
while T: 
    [read,_,_] = select.select(clients,[],[])
    for s in read:
        compteur+=1
        if s == mysocket:  
            (socketclient,addr) = s.accept()
            clients.append(socketclient)
        else: 
            msg = s.recv(1000)
            message = str(msg, 'utf-8')
            if message in "CODE001":
                print("start new thread from port "+str(addr[1]))
                start_new_thread(playerThread, (socketclient,addr[1]))
            elif message in "CODE002":
                print("Jeu = 2")
            elif message.find("CODE003")!=-1:
                print("Jeu = 3")
                pseudo = message.split(":")[1]
                start_new_thread(chatThread, (socketclient,clients,pseudo,))
            if len(msg) == 0:
                s.close()
                clients.remove(s)
for z in clients:
    z.close()

mysocket.close()


          #  else:
                #Message speciique
                #sendToPort(s,message+" envoyé à un port specifique",portSocket)

                #Broadcast
              #  broadcast(clients, message+" envoyé en broadcast")
