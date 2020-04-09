import requests
import datetime
import sqlite3
import math
import csv
from time import process_time


def getTemperature(dataRequest):   #Recupere la temperature a partir du resultat de la requete
    return(dataRequest['main']['temp'])

def getDate(dataRequest):   #Recupere la date et l'heure a laquelle la meteo a ete prise pour la derniere fois a partir du resultat de la requete
    return(datetime.datetime.fromtimestamp(dataRequest['dt']))

def getTemps(dataRequest):   #Recupere le temps a partir du resultat de la requete
    return(dataRequest['weather'][0]['main'])


def ajouterLigneBDD(ville, cursor):   #Ajoute la une ligne dans la bdd. On prend la ville choisie en argument. On indique aussi cursor pour etre liee a la bonne BDD.
    req = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+ville+",fr&appid=2fd760807b08fc97be68c52954281198")
    data = req.json()
    if data['cod'] != '404' :   #On verifie que la ville soit trouvable
        print("ajout de "+ville)
        cursor.execute("""
                   INSERT INTO meteo(ville, date, temperature, temps) 
                   VALUES(?, ?, ?, ?)""",(ville, getDate(data), getTemperature(data), getTemps(data)))
    else :
        print(ville+" n'existe pas")
                           
    
def creerTable():
    conn = sqlite3.connect('meteoBDD.db')   #Etablie la connection avec la bdd
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

def ajouterPlusieursLignes(listeVilles): #On est limité à 60 requetes par minute avec l'API
    conn = sqlite3.connect('meteoBDD.db')   #Etablie la connection avec la bdd
    cursor = conn.cursor()
    for ville in listeVilles:
        ajouterLigneBDD(ville, cursor)
    conn.commit()   #commit les modifications
    conn.close()   #ferme la connection

def recupererMeteoVille(ville) :  #donne les resultats d'une ville dans la bdd
    conn = sqlite3.connect('meteoBDD.db')   #Etablie la connection avec la bdd
    cursor = conn.cursor()
    cursor.execute("""SELECT ville, date, temperature, temps FROM meteo WHERE ville = ?""", (ville,))
    rows = cursor.fetchall()
    for row in rows :
        print('{0}   date : {1} - temperature : {2}°C - temps : {3}'.format(row[0], row[1], int(row[2]-273), row[3]))
    conn.close()   #ferme la connection
    
def subdivisionListeVilles(listeVilles):   #On a 3000 villes mais on ne peut en traiter que 50 par minute car l'API est limitee
    newListe = [[] for i in range(60)]  #1 liste par minute dans 1h
    n = len(listeVilles)
    nombreParMinute = math.ceil(3000//60)
    for k in range(n) :
        newListe[k//nombreParMinute] += [listeVilles[k]]
    return newListe


def main(subdListeVilles):
    minute = -1   #Compte les minutes, le programme fait des boucles d'une heure
    arret = False
    while arret == False :
        minute = (minute+1)%60
        t_start = process_time()
        ajouterPlusieursLignes(subdListeVilles[minute])   #on ajoute toute les villes qui doivent etre ajoutees a cette minute precise
        t_stop = process_time()
        print("attente de "+str(60-(t_stop - t_start))+" seconde pour avoir plus de requetes possibles")
        while (t_stop - t_start) < 60 and arret == False:   #Si le programme run trop vite, on attend la fin de la minute avant de passer aux villes suivantes
            ##C'EST ICI QU'ON VEUT METTRE L'INPUT
            ##APPAREMENT IL FAUT UTILISER GETCH() MAIS CA NE MARCHE PAS SUR MON PC
            t_stop = process_time()


      
listeVilles = [] #On cree subdListeVilles plus bas, la subdivision de la liste pour en faire 60 plus petites
with open('./cities/sortedcities3000.csv') as csvFile:
    csvReader = csv.reader(csvFile)
    for row in csvReader:
        listeVilles.append(row[0])


subdListeVilles = subdivisionListeVilles(listeVilles)
creerTable()
main(subdListeVilles)