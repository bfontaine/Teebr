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

Technos :

* SQLite (pour le schéma et l’économie de mémoire par rapport à ES)
* Python w/ tweepy

---

Pas possible de recommander des tweets si on ne s'intéresse pas à ce dont ils
parlent, on pense au TF/IDF mais on a une infinité de mots/hashtags possibles.

--> enter nltk (initialiser avec `nltk.download()`) : voir si on peut extraire
les noms des tweets pour déjà réduire les possiblités.
