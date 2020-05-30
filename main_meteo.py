# -*- coding: utf-8 -*-
import datetime
import threading
from BaseDeDonnee import BaseDeDonnee
from Controle import Controle
import pygame
import time

pygame.init()  #Initialisation pygame
pygame.font.init()  #Initialisation font (pour les textes)
#screen = pygame.display.set_mode((600,600))  #Initialisation du screen à utiliser

##/!\
##ATTENTION : Nous sommes limites a 60 requetes par minutes. Si plusieures personnes utilisent ce programme avec la meme cle API, il risque d'y avoir des problemes.

##NOUS VOUS FOURNISSONS NOTRE CLE API OPENSTREETWEATHER. SI VOUS SOUHAITEZ UTILISER LA VOTRE, CHANGEZ LA LIGNE SUIVANTE :
cleAPI = "2fd760807b08fc97be68c52954281198"

##IL VOUS A NORMALEMENT ETE FOURNI LE FICHIER "meteoBDD.db". SI VOUS SOUHAITEZ UTILISE UN AUTRE FICHIER OU EN CREER UN NOUVEAU, CHANGEZ LA LIGNE SUIVANTE :
fichierBDD = "meteoBDD.db"
#Dans le cas où vous mettez un nouveau nom, le programme creera le fichier lui-meme. N'oubliez pas l'extension ".db".

##NOUS VOUS AVONS EGALEMMENT FOUNI LA LISTE DES VILLES A ETUDIER. VOUS POUVEZ METTRE LE VOTRE EN CHANGEANT LA LIGNE SUIVANT :
fichierVilles = "villes.txt"
#Si vous creez votre propre fichier villes, la première ligne doit être un "0". C'est une valeur de sauvegarde qui servira au programme à reprendre là où il en etait la prochaine fois.


bdd = BaseDeDonnee(fichierVilles, fichierBDD, cleAPI)
bdd.initialiser() #Cree le fichier BDD s'il n'existe pas. 
                  #Recupere les villes du fichier villes. 
                  #Retrouve a quelle ville il s'en etait arrete (premiere ligne du fichier villes)
                  #redefinie la taille de la liste des villes (on peut ainsi en rajouter)

controle = Controle(bdd)  #Va mettre en relation les differentes classes, et gerer les inputs
controle.initialiser()
  
def mettreAJourBDD(BDD):
    while bdd.finProgramme == False :
        if (BDD.tempsDernieresRequetes == None) or (datetime.datetime.now() - BDD.tempsDernieresRequetes).seconds >= 60 :
            BDD.enregistrer()
            time.sleep(60 - (datetime.datetime.now() - BDD.tempsDernieresRequetes).seconds)
            
x = threading.Thread(target=mettreAJourBDD, args=(bdd,))
x.start()

while bdd.finProgramme == False :
    controle.display()
    
    for event in pygame.event.get() :
        if event.type == pygame.QUIT: #Si on clique sur le croix rouge
            pygame.quit()  #On ferme la fenetre
            bdd.setFinProgramme()  #On coupe le programme (on n'oublie pas le thread). 
        
        else :  #Si on appuie sur la sourie ou sur le clavier on envoie l'information au controleur
            if event.type == pygame.MOUSEBUTTONDOWN :
                controle.inputMouse(event) 
            elif event.type == pygame.KEYDOWN :
                controle.inputKeyboard(event)
