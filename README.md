# OhMyFridge

---------------------------------

PRESENTATION DE L'APPLICATION

L'objectif de l'application est de proposer à l'utilisateur des recettes adaptées à ce qu'il possède chez lui.
L'idée n'était pas d'être uniquement un inventaire de recettes mais de permettre d'utiliser les restes pour éviter le gachis alimentaire.

L'utilisateur renseigne, ingrédient par ingrédient (en anglais et en minuscule) ce qu'il possède ou ce qu'il souhaite utiliser.
Il renseigne également s'il souhaite utiliser uniquememnt les ingrédients qu'il renseigne ou si l'application peut lui proposer des recettes utilisant des ingrédients supplémentaires.

L'application lui propose ensuite quelques recettes.
Pour chaque recette, on affiche le titre, la liste d'ingrédients et les instructions.
On affiche également le nutriscore, si la recette est végétarienne et si elle est sans gluten.

---------------------------------

FONCTIONNEMENT DE L'APPLICATION

On part du dataset disponible sur Kaggle : https://recipenlg.cs.put.poznan.pl
Il contient plus d'un million de recettes (en anglais), avec le titre de la recette, les quantités, les insctructions, etc...

Avant de lancer l'application, on effectue un pré-processing en ne conservant que certaines colonnes et en rajoutant la colonne nutriscore.
On calcule le nutriscore à la main avec un système de points négatifs et positifs en lançant le script 'data_processing.py'.

L'application fonctionne avec la partie static (css et javascript), la partie logic (script python) et la partie HTML.
On lance l'application avec le script 'app.py'.

Pour le déploiement de l'application, nous avons du stocker le dataset pré-processé sur un serveur.

Lien de l'application : https://infrastructure-tawny.vercel.app/