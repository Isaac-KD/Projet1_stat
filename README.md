# Projet1_stat

## Description
Ce projet est un exercice universitaire dans le cadre de l'unité d'enseignement de statistiques. Il s'agit d'une application Python qui permet d'effectuer des simulations et des analyses statistiques à l'aide de plusieurs modules, incluant des tests unitaires.

## Table des matières
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Tests](#tests)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Installation
    ```bash
    pip install -r requirements.txt
    ```
## Utilisation

    Lancer la simulation : Une fois que tout est en place, vous pouvez exécuter le script de simulation pour voir comment les différentes stratégies se comportent :
    ```bash
    python Simulation.py
    ```
    ### Exécution des Tests
    Des tests unitaires ont été écrits pour valider les principaux composants du projet. Afin de vérifier que tout fonctionne comme prévu, exécutez la suite de tests en utilisant unittest :
    ```bash
    python -m unittest discover -s Test
    ```    
## Structure du Projet

    Le projet est divisé en plusieurs modules et dossiers, chacun ayant une fonction bien définie pour assurer une séparation claire des responsabilités.

    1. Simulation principale

        •	Simulation.py : Le point d’entrée du projet. Ce fichier contient le code permettant de lancer les simulations. Il orchestre l’interaction entre les différents composants du jeu, tels que la grille, les bateaux, et les joueurs.

    2. Modules du jeu (dossier Game/)

        •	Grille.py : Ce module gère la structure de la grille où les bateaux sont placés. Il contient les méthodes pour initialiser la grille, vérifier les collisions, et afficher l’état des cases.
        •	Bateau.py : Gère la définition et le comportement des bateaux. Chaque bateau a une taille, une position et un état (coulé ou non).
        •	Bataille.py : Ce module contient la logique principale de la bataille. Il contrôle les interactions entre les joueurs, les attaques, et la résolution des coups portés sur les bateaux.
        •	Joueur.py : Gère les joueurs et leurs stratégies. Ce fichier définit les différentes façons dont un joueur peut effectuer ses mouvements (probabilité, heuristique).

    3. Tests unitaires (dossier Test/)

        •	test_grille.py : Contient les tests pour s’assurer du bon fonctionnement des méthodes associées à la grille.
        •	test_bateau.py : Valide que les bateaux sont correctement initialisés, placés et qu’ils interagissent correctement avec la grille.
        •	test_bataille.py : Teste la logique des batailles, incluant les interactions entre les joueurs et l’application des règle
