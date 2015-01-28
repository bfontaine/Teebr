Projet divisé en deux parties :

- partie récupération des données
- partie utilisation desdites données

## Récupération

Buts :

* Un programme doit tourner en permanence et récupérer des tweets selon des
  règles pré-définies (e.g. tweets contenant tel mot-clef ou de tel compte)
* On doit pouvoir ajouter/modifier/supprimer les règles à chaud, i.e. sans
  relancer le programme (solution possible : le programme intercepte un signal
  qui veut dire qu’il faut recharger le fichier de règles, le programme qui
  valide la modification des règles le notifie avec ce signal)
