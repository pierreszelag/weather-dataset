import datetime
import sqlite3
import requests
import time
from Affichage import Affichage

class BaseDeDonnee:
    
    def __init__(self, fichierVilles, fichierBDD, cleAPI):
        #Elements fournis par l'utilisateur
        self.fichierVilles = fichierVilles  #Le fichier qui va nous permettre de recuperer la liste des villes
        self.fichierBDD = fichierBDD  #Le fichier qui va gerer la base de donnee (Type : Data Base File)
        self.cleAPI = cleAPI  #Cle api openweathermap
        
        #Permet de mettre en lien le thread avec le programme principal. Permet egalement de cut la recherche de requetes qui peut parfois etre longue
        self.finProgramme = False
        
        #Informations sur les villes
        self.listeVilles = []  #La liste des villes recuperee a partie du fichier villes
        self.tailleVilles = None  #Taille de la liste des villes
        
        #Utilises pour mettre a jour la BDD
        self.ouvrirBDDautorise = True  #Si l'utilisateur ouvre la BDD pour faire une recherche, elle ne peut pas s'ouvrir en parallele pour la mettre à jour.
        self.numeroVille = None  #Le numero de la ville qu'on est en train d'enregistrer dans la bdd
        self.tempsDernieresRequetes = None  #Variable de temps utilisee pour ne pas depasser nos 60 requetes par minutes autorisees.
        
        
    ##GETTERS
    def getListeVilles(self):
        return self.listeVilles
    
        
    #SETTERS
    def setFinProgramme(self): #Le programme doit s'arreter.
        self.finProgramme = True
        

    ##INITIALISATION DE LA BDD ET DE LA LISTE DE VILLES    
    def initialiser(self):
        ##CREE LE FICHIER BASE DE DONNEE (Type : Data Base File) S'IL N'EXISTE PAS ENCORE
        #Normalement nous vous fournissons deja une base de donnee avec quelques donnees pre-enregistrees.
        conn = sqlite3.connect(self.fichierBDD)   #Etablie la connection avec la bdd
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS meteo(   
                       id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                       ville TEXT,
                       date TEXT,
                       temperature INTEGER,
                       temps TEXT
                       )
                   """)   #Cree la table si elle n'existe pas
        conn.commit()   #commit les modifications
        conn.close()   #ferme la connection
        
        ##RECUPERE LA LISTE DES VILLES DU DOCUMENT ANNEXE
        f = open(self.fichierVilles, "r")
        self.numeroVille = int(f.readline()) #La premiere ligne du fichier correspond au numero de la ville a laquelle on a arrete l'enregistrement la derniere fois.
        ligne = f.readline()
        while ligne != "":
            self.listeVilles += [supprimerRetourLigne(ligne)]  #On recupere les villes en enlevant le \t\n
            ligne = f.readline()
        f.close()
        self.tailleVilles = len(self.listeVilles) -1 #La premiere ligne n'est pas une ville    
        
        
    ##MISE A JOUR DE LA BDD   
    def enregistrer(self):
        
        #On recupere d'abord toutes les requetes
        listeRequetes = []
        for i in range(60) : #On dispose de 60 requetes par minute
            if self.finProgramme == True :
                return None
            ville = self.listeVilles[(self.numeroVille +i)%self.tailleVilles]
            req = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+ville+",fr&appid="+self.cleAPI)  #Recupere la meteo d'une ville avec notre cle API
            data = req.json()  #Convertie la reponse au bon format
            if data['cod'] != '404' :   #On verifie que la ville ait ete trouvee
                #On ajoute le resultat dans la liste de requetes
                listeRequetes += [[ville, getDate(data), getTemperature(data), getTemps(data)]]
        self.tempsDernieresRequetes = datetime.datetime.now() #On enregistre l'heure de la derniere serie de requete pour attendre 60 secondes
        #Si l'utilisateur ouvre la BDD pour une recherche, on attend qu'il la ferme avant de l'ouvrir pour la mettre à jour (cela ne devrait pas prendre plus de quelques millisecondes en théorie)
        while self.ouvrirBDDautorise == False :
            time.sleep(0.5)
            
        #On les ajoute toutes maintenant dans la BDD (permet de garder le fichier ouvert moins longtemps) 
        conn = sqlite3.connect(self.fichierBDD)   #Etablie la connection avec la bdd
        cursor = conn.cursor()
        for requete in listeRequetes :
            cursor.execute("""
                           INSERT INTO meteo(ville, date, temperature, temps) 
                           VALUES(?, ?, ?, ?)""",(requete[0], requete[1], requete[2], requete[3]))
        conn.commit()   #commit les modifications
        conn.close()   #ferme la connection
        self.numeroVille = (self.numeroVille+60)%self.tailleVilles #On indente les 60 villes que maintenant, au cas où on cut le programme pendant les requetes. (des villes n'auraient pas ete enregistrees)        
        #On recupere le texte du document villes
        recup = open(self.fichierVilles, "r")
        lignes = recup.readlines()  #On enregistre a quelle ville on s'est arrete dans le document.
        recup.close()
        
        #On change la valeur de sauvegarde
        lignes[0] = str(self.numeroVille)+"\t\n"
        
        #On le re-enregistre
        enreg = open(self.fichierVilles, "w")
        enreg.writelines(lignes)
        enreg.close()
    
    
    ##RECUPERATION DE LA BDD    
    def recuperer(self, ville):
        listeReponses = []
        self.ouvrirBDDautorise = False  #On s'apprete à ouvrir la BDD pour la lire, on interdit donc son ouverture pour l'ecriture. (On rappelle que le programme run plusieurs choses à la fois)
        conn = sqlite3.connect('meteoBDD.db')   #Etablie la connection avec la bdd
        cursor = conn.cursor()
        cursor.execute("""SELECT ville, date, temperature, temps FROM meteo WHERE ville = ?""", (ville,))
        rows = cursor.fetchall()
        for row in rows :
            listeReponses += [('{0}   date : {1} - temperature : {2}°C - temps : {3}'.format(row[0], row[1], int(row[2]-273), row[3]))]
        conn.close()   #ferme la connection
        self.ouvrirBDDautorise = True #On a ferme la BDD, on autorise donc l'autre partie du programme à l'ouvrir pour la mettre à jour.
        return listeReponses
         
            
##FONCTIONS UTILISEES POUR TRAITER LES REPONSES DE OPENWEATHERMAP (ne necessitant pas d'etre dans la classe BaseDeDonnee)
def supprimerRetourLigne(ligne):
    newLigne = ""
    for i in ligne :
        if ord(i) != 10 :
            newLigne += i
    return newLigne
        

def getTemperature(dataRequest):   #Recupere la temperature a partir du resultat de la requete
    return(dataRequest['main']['temp'])

def getDate(dataRequest):   #Recupere la date et l'heure a laquelle la meteo a ete prise pour la derniere fois a partir du resultat de la requete
    return(datetime.datetime.fromtimestamp(dataRequest['dt']))

def getTemps(dataRequest):   #Recupere le temps a partir du resultat de la requete
    return(dataRequest['weather'][0]['main'])
