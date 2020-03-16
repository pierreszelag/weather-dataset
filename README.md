# weather-dataset
A dataset of hourly weather informations for 3000 french cities

Nous voulons créer un programme capable de récupérer l’API à partir d’un site web (on utilisera open weather map), le but du programme sera d’utiliser cette API pour récupérer les informations sur le temps de villes que l’on choisi nous-même, ensuite nous récupérons uniquement les informations qui nous intéressent sur toutes celles renvoyées par l’API et de créer un fichier texte pouvant stocker ces informations.
Ensuite nous créons une méthode qui va modifier le texte à écrire dans notre document texte afin de traduire les informations en SQL. Le but de la méthode sera d’écrire en SQL la création et modifications des tables de la base de donnée dans laquelle nous stockerons nos résultats (ville + temps).

A program use the OpenWeatherMap API in order to get weather data for a city. As the usage of the API is limited if we want to have hourly result we need to have a dataset with less than 3600 cities.

We recovered a large dataset of 36700 french cities. A program read this dataset, sort cities by descending population and write a new file that will be used to make the request.

...
