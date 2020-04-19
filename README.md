Ce programme gère une base de donnée contenant la météo des villes fournies au cours du temps.

Le programme utilise l'API de OpenWeatherMap pour recupérer les informations météorologique d'une ville. Comme l'utilisation de l'API est limitée, nous devons nous contenter de 60 requetes par minutes.


•FONCTIONNALITES :

Ce programme permettra les choses suivantes :
-Enregistrement de la météo de 60 villes par minutes (ville, date/heure, temperature, temps).
-Recuperation de toutes les données météorologique d'une ville (date/heure, temperature, temps).


•CAHIER DES CHARGES :

-Nous pouvons utiliser notre propre liste de villes à enregistrer(suivre guide plus bas).

-La mise a jour de la BDD (60 requetes par minute) doit se faire pendant que l'utilisateur utilise le programme, sans géner son utilisation (threading, voir plus bas).

-La fin de programme doit se faire proprement. Pas de crash dans le thread, pas de fermeture si la BDD n'a pas été close(), etc...

-Utilisation d'une interface graphique.

-Utilisation d'une barre de recherche pour chercher un ville. Le nom de la ville n'a pas besoin d'être complet. Après chaque lettre tapée (ou touche delete), le programme nous affiche la liste de villes pouvant correspondre. Il nous suffit de cliquer sur celle que l'on souhaite.

-Cliquer sur la barre de recherche nous permet d'écrire dedans. Cliquer à côté nous enlève cette possibilité.

-Après avoir selectionné une ville, la liste des resultats météorologiques associés est affichée.

-Que ce soit pour la liste des villes ou la liste des resultats, si la liste est trop longue pour être affichée sur une page, il y aura un bouton "retour" et un bouton "suivant" permettant de voir les éléments non affichés.


•INSTALLATION :

Pour utiliser le programme, il vous faudra copier/coller, installer les fichiers suivants :

-main_meteo (fichier à run)
-BaseDeDonnee (permet la gestion de la BDD)
-Controle (permet de gerer les inputs utilisateurs et d'organiser les autres classes
-Affichage (interface graphique)
-villes.txt /!\ Vous pouvez creer votre propre liste de villes. Pour cela, lire le guide plus bas. /!\
-meteoBDD.db /!\ FACULTATIF /!\ Si vous lancez le programme sans ce fichier, le programme créé un fichier BDD vierge lui même. Nous vous fournissons un fichier pré-rempli pour que vous aillez plus de valeurs à manipuler. Si vous décidez d'utiliser votre propre liste de ville, il est conseillé de ne pas utiliser le fichier meteoBDD.db fourni.


•THREADING :

La base de donnée est mise à jour de 60 villes par minutes pendant que le programme tourne.
L'utilisateur doit continuer à pouvoir utiliser le programme et accéder à la base de donnée pendant ce temps.
Pour cela, on utilise une méthode de threading (le programme run deux endroit en même temps).
La difficulté est qu'un fichier base de donnée (.db) ne peut être ouvert à deux endroits en même temps.

On a mis plusieurs manipulations en place pour remedier à cela :

-On a mis en place une variable qui autorise l'ouverture de la BDD pour la mettre à jour (l'utilisateur est prioritaire).
Quand l'utilisateur demande des informations dans la BDD, la variable devient "False". La BDD est donc ouverte pour l'utilisateur, les données recupérées, puis la BDD se ferme. La variable redevient donc "True".
Dans ce cas là, la BDD ne peut être ouverte par le thread pour être mise à jour. Le thread attend donc que la BDD soit refermée de l'autre côté et que la variable soit repassée à "True" pour l'ouvrir à son tour.

-Le programme recuperer d'abord le resultats des 60 requetes qu'il enregistre dans une liste. Cela permet une fois les 60 requetes acquises d'ouvrir la BDD, les rentrer dedans, et fermer là BDD instantanément. Cela ne prend donc que quelques millisecondes (alors qu'enregistrer les requetes une après l'autre peut garder la BDD ouverte plusieurs secondes).

Nous avons récupérés une grosse base de donnée de 36700 villes françaises avec beaucoup d'informations qui ne sont pas utiles, il y a donc un programme qui permet de trier les 3000 villes les plus peuplées de france et qui écrit ces dernières dans un fichier csv.


...

