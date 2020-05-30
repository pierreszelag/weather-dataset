# -*- coding: utf-8 -*-
from BaseDeDonnee import BaseDeDonnee
from Affichage import Affichage

class Controle :
    def __init__(self, bdd):
        #instances en lien avec celle-ci
        self.bdd = bdd
        self.affichage = Affichage(self.bdd)
        
        #Gestion de resultats et de l'affichage
        self.listeVilles = None
        self.ecrire = False #dit si on est en train d'ecrire dans la barre de recherche
        self.barreRecherche = "" #texte ecrit dans la barre de recherche
        self.villesCherchees = [] #liste des villes qu'il faudra afficher
        self.numeroVilleCherchee = 0 #numero de la premiere ville qu'on affiche
        self.listeResultats = [] #liste des responses recuperees dans la bdd
        self.numeroResultat = 0 #numero de la premiere reponse qu'on affiche
        self.typeAffichage = "Villes" #Si on doit afficher le tableau "Ville" ou le tableau "Resultats"
        
        
    #INITIALISATION    
    def initialiser(self):
        self.listeVilles = self.bdd.getListeVilles()
        self.villesCherchees = self.bdd.getListeVilles()
    
    #TOUCHES DE CLAVIER    
    def inputKeyboard(self, event):
        if self.ecrire == False : #Si on a pas le droit d'écrire on passe.
            pass
        elif (33 <= event.key <= 122) and len(self.barreRecherche) <= 15:
            self.barreRecherche += event.unicode
            self.correspondanceSuivante() #prend l'ancienne liste villesCherchees et cherche les elements qui peuvent toujours correspondre à la barre de recherche
            self.numeroVilleCherchee = 0 #On revient en premiere page.
            
        elif (event.key == 8) and self.barreRecherche != "" :
            self.barreRecherche = self.barreRecherche[:-1]  #On supprime la derniere lettre
            self.correspondance() #On recherche a partie de la listeVilles de base
            self.numeroVilleCherchee = 0 #On revient en premiere page.
        
    #ON VA TESTER LES BOUTONS. CHAQUE BOUTON QUI NE CORRESPOND PAS VA APPELER LE SUIVANT
    def inputMouse(self, event):
        x = event.pos[0]
        y = event.pos[1]
        self.clicBarreRecherche(x,y)
    
    def clicBarreRecherche(self, x, y): #clic sur la barre de recherche
        if (575 <= x <= 715) and (50 <= y <= 90):
            self.ecrire = True
        else :
            self.ecrire = False #On a clique en dehors de la barre de recherche. On ne peut plus ecrire dedans.
            self.clicRetourAffichage(x, y) #clic sur le bouton retour de gauche
            
    def clicRetourAffichage(self, x,y) :  #clic sur le bouton retour de gauche
        if (50 <= x <= 80) and (10 <= y <= 40) and self.typeAffichage == "Resultats":
            self.typeAffichage = "Villes"
        else :
            self.clicResultats(x, y) #clic sur la zone des resultats
            
    def clicResultats(self, x, y): #clic sur la zone des resultats
        if (50 <= x <= 550) and (50 <= y <= 550) and self.typeAffichage == "Villes":
            self.demanderResultats(x,y) #Recupere la liste des resultats a afficher.
        else :
            self.clicRetour(x, y) #clic sur le bouton retour
                
    def clicRetour(self, x, y): #clic sur le bouton retour
        if (450 <= x <= 480) and (10 <= y <= 40) and self.typeAffichage == "Villes":
            self.setNumeroVilleDown()
        elif (450 <= x <= 480) and (10 <= y <= 40) and self.typeAffichage == "Resultats":
            self.setNumeroResultatDown()
        else :
            self.clicSuivant(x, y) #clic sur le bouton suivant
            
    def clicSuivant(self, x, y): #clic sur le bouton suivant
        if (500 <= x <= 530) and (10 <= y <= 40) and self.typeAffichage == "Villes":
            self.setNumeroVilleUp()
        elif (500 <= x <= 530) and (10 <= y <= 40) and self.typeAffichage == "Resultats":
            self.setNumeroResultatUp()       
        
    #FONCTIONS UTILES
    def setNumeroVilleDown(self):  #Descend le numeroVilleCherchee pour revenir une page en arriere
        if self.numeroVilleCherchee >= 20 :
            self.numeroVilleCherchee -= 20
        else :
            self.numeroVilleCherchee = 0
            
    def setNumeroVilleUp(self):  #Monte le numeroVilleCherchee pour aller une page en avant
        if self.numeroVilleCherchee + 20 < len(self.villesCherchees):
            self.numeroVilleCherchee += 20

    def setNumeroResultatDown(self):  #Descend le numeroVilleCherchee pour revenir une page en arriere
        if self.numeroResultat >= 10 :
            self.numeroResultat -= 10
        else :
            self.numeroResultat = 0
            
    def setNumeroResultatUp(self):  #Monte le numeroVilleCherchee pour aller une page en avant
        if self.numeroResultat + 10 < len(self.listeResultats):
            self.numeroResultat += 10

            
    def correspondanceSuivante(self):  #Cherche quels mots contiennent la nouvelle chaine de caractere. On se base sur la liste précédente.
        newListeVilles = []
        for k in self.villesCherchees :
            if k.find(self.barreRecherche) != -1 :
                newListeVilles += [k]
        self.villesCherchees = newListeVilles
        
    def correspondance(self):  #Cherche quels mots contienne la nouvelle chaine de caractere. On se base sur la liste de depart listeVilles.
        newListeVilles = []
        for k in self.listeVilles :
            if k.find(self.barreRecherche) != -1 :
                newListeVilles += [k]
        self.villesCherchees = newListeVilles
            
    def demanderResultats(self, x, y):  #On clique sur une ville. On demande ses resultats à la bdd.
        num = self.numeroVilleCherchee + ((y - 50) //50) + ((x - 50) //250)*10
        if num < len(self.villesCherchees) :
            self.numeroResultat = 0 #On reinitialise le numero de la premiere reponse a afficher
            ville = self.villesCherchees[num]
            self.listeResultats = self.bdd.recuperer(ville)
            self.typeAffichage = "Resultats"
        
    #INTERFACE GRAPHIQUE
    def display(self):  #On met tout en argument (les arguments vides ne seront pas utilises), la classe Affichage se chargera du tri.
                        #On aurait pu faire l'affichage dans cette classe. L'utilite est de gagner en clarte.
        self.affichage.display(self.barreRecherche,
                               self.villesCherchees,
                               self.numeroVilleCherchee,
                               self.listeResultats,
                               self.numeroResultat,
                               self.typeAffichage)
        
        
