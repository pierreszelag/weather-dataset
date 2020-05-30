# -*- coding: utf-8 -*-
import pygame

class Affichage:
    
    def __init__(self, bdd):
        self.screen = pygame.display.set_mode((800,600)) #Screen à utiliser
        self.bdd = bdd
        
        
    def display(self,   #On met tout en argument (les arguments vides ne seront pas utilises). 
                        #Cela permet d'avoir une classe Controle plus claire et de gerer l'affichage uniquement grasse à la classe affichage.
                barreRecherche,
                villesCherchees,
                numeroVilleCherchee,
                listeReponses,
                numeroReponse,
                typeAffichage):
        
        self.screen.fill((255,255,255)) #Efface l'ecran
        pygame.draw.rect(self.screen,(0,0,0),(50,50,500,500), 2) #grand rectangle de gauche
        pygame.draw.rect(self.screen,(0,0,0),(575,120,200,430), 2) #grand rectangle de droite
        pygame.draw.rect(self.screen,(0,0,0),(450,10,30,30), 2) #bouton retour
        pygame.draw.rect(self.screen,(0,0,0),(50,10,30,30), 2) #bouton retour affichage
        pygame.draw.polygon(self.screen, (0,0,0), [(55,25), (75,15), (75, 35)]) #triangle retour de gauche
        pygame.draw.polygon(self.screen, (0,0,0), [(455,25), (475,15), (475, 35)]) #triangle retour de droite
        pygame.draw.rect(self.screen,(0,0,0),(500,10,30,30), 2) #bouton suivant
        pygame.draw.polygon(self.screen, (0,0,0), [(505,15), (525,25), (505, 35)]) #triangle suivant
        
        for i in range(9):
            pygame.draw.line(self.screen, (0,0,0), (50, 100+50*i), (550, 100+50*i), 2) #Commencer le tableau
        
        self.displayBarreDeRecherche(barreRecherche) #dessine la barre de recherche avec le texte
        self.displayMisesAJours() #Ecrit les mises à jours effectuees.
        
        if typeAffichage == "Villes" :
            self.displayVilles(villesCherchees, numeroVilleCherchee)
        
        else :
            self.displayReponses(listeReponses, numeroReponse)
            
        
        pygame.display.flip()
            
    def displayMisesAJours(self):
        font = pygame.font.SysFont("Arial", 16)
        text = font.render("Villes recherchées :", True, (0, 0, 0))
        self.screen.blit(text, (580, 100))
        
        for i in range(21):
            font = pygame.font.SysFont("Arial", 16)
            text = font.render(self.bdd.changements[21 -1 -i], True, (0, 0, 0))
            self.screen.blit(text, (580, 120 + 20*i))
        
    
    def displayBarreDeRecherche(self, barreRecherche) :#Dessine la barre de recherche avec le texte
        pygame.draw.rect(self.screen,(0,0,0),(575,50,140,40), 2) #dessine la barre de recherche  
        font = pygame.font.SysFont("Arial", 16)
        if barreRecherche == "":
            text = font.render("Barre de recherche", True, (100, 100, 100))
        else :
            text = font.render(barreRecherche, True, (0,0,0))
        self.screen.blit(text, (580, 57))
        
    def displayVilles(self, villesCherchees, numeroVilleCherchee) : #Trace la grille pour les villes et affiche les resultats
        pygame.draw.line(self.screen, (0,0,0), (300, 50), (300, 550), 2) #Trait vertical
        for i in range(20) :
            if (numeroVilleCherchee + i) < len(villesCherchees) :
                font = pygame.font.SysFont("Arial", 16)
                text = font.render(villesCherchees[numeroVilleCherchee+i], True, (0, 0, 0))
                self.screen.blit(text, (55 +250*(i//10), 55 +50* (i%10)))
                
    def displayReponses(self, listeReponses, numeroReponse):
        for i in range(10) :
            if (numeroReponse + i) < len(listeReponses) :
                font = pygame.font.SysFont("Arial", 16)
                text = font.render(listeReponses[numeroReponse+i], True, (0, 0, 0))
                self.screen.blit(text, (55 +250*(i//10), 55 +50* (i%10)))
