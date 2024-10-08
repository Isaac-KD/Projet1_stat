import matplotlib.pyplot as plt
from Game.Joueur import *
import numpy as np

def dessin_graphique_un_joueur2(liste_joueur, avg_joueur, nom_joueur):
    # Filtrer les indices pour éviter les multiples de 5
    indices = [i for i in range(len(liste_joueur)) if i % 5 != 0]

    # Récupérer les scores correspondants
    scores = [liste_joueur[i] for i in indices]

    # Créer le graphique
    plt.figure(figsize=(14, 8))

    # Histogramme pour le joueur (avec les indices filtrés)
    plt.barh(indices, scores, color='#1f77b4', label=f'{nom_joueur} AVG = {avg_joueur}')  # couleur bleu

    # Ajouter des titres et des labels
    plt.title(f'Performance de {nom_joueur}', fontsize=16)
    plt.xlabel('Score', fontsize=14)
    plt.ylabel('Nombre de Tours (sans multiples de 5)', fontsize=14)

    # Créer des ticks personnalisés pour l'axe des ordonnées
    plt.yticks(indices, [str(i) for i in indices], fontsize=8)  # Utiliser les indices pour l'axe Y

    # Ajuster la largeur des barres
    plt.tight_layout()

    # Ajouter une légende et une grille
    plt.legend(fontsize=12)
    plt.grid(axis='x')  # La grille s'affiche sur l'axe des X

    # Ajuster l'axe des ordonnées
    plt.ylim(-0.5, len(scores) - 0.5)  # Ajuster les limites de l'axe Y

    # Afficher le graphique
    plt.show()
    
def dessin_graphique_un_joueur(liste_joueur, avg_joueur, nom_joueur):
    # Créer le graphique
    plt.figure(figsize=(14, 8))

    # Créer des indices pour les barres
    indices = np.arange(len(liste_joueur))

    # Largeur des barres
    largeur = 0.5

    # Histogramme pour le joueur
    plt.bar(indices, liste_joueur, largeur, label=f'{nom_joueur} AVG = {avg_joueur}', color='#1f77b4')  # couleur bleu

    # Ajouter des titres et des labels
    plt.title(f'Performance de {nom_joueur}', fontsize=16)
    plt.xlabel('Nombre de Tours', fontsize=14)
    plt.ylabel('Score', fontsize=14)

    # Créer des ticks personnalisés pour l'axe des abscisses
    plt.xticks(indices, rotation=90, ha='right', fontsize=8)

    # Ajuster la largeur des barres
    plt.tight_layout()

    # Ajouter une légende et une grille
    plt.legend(fontsize=12)
    plt.grid(axis='y')

    # Ajuster l'axe des abscisses pour éviter le chevauchement
    plt.xlim(-0.5, len(liste_joueur) - 0.5)  # Ajuster les limites de l'axe x

    # Afficher le graphique
    plt.show()
    
def dessin_graphique_duo(liste_alea, liste_heur):
    # Créer le graphique
    plt.figure(figsize=(10, 5))

    # Créer des indices pour les barres
    indices = np.arange(len(liste_alea))

    # Largeur des barres
    largeur = 0.35

    # Histogramme pour les deux joueurs
    plt.bar(indices - largeur/2, liste_alea, largeur, label='Joueur proba', color='blue')
    plt.bar(indices + largeur/2, liste_heur, largeur, label='Joueur Heuristique', color='red')

    # Ajouter des titres et des labels
    plt.title('Comparaison des joueurs Aléatoire et Heuristique')
    plt.xlabel('Nombre de Tours')
    plt.ylabel('Score')
    plt.xticks(indices)  # Positionner les ticks en fonction des indices
    plt.legend()
    plt.grid(axis='y')

    # Afficher le graphique
    plt.show()

def dessin_graphique_all(liste_alea, liste_heur, liste_proba, liste_mc, avg_alea, avg_heur, avg_proba, avg_mc):
    # Créer le graphique
    plt.figure(figsize=(14, 8))

    # Créer des indices pour les barres
    indices = np.arange(len(liste_alea))

    # Largeur des barres
    largeur = 0.2  # Réduit la largeur des barres pour un meilleur espacement

    # Histogramme pour les quatre joueurs avec des couleurs attrayantes
    plt.bar(indices - 1.5 * largeur, liste_alea, largeur, label='Joueur Aléatoire, AVG = ' + str(avg_alea), color='#1f77b4')  # bleu
    plt.bar(indices - 0.5 * largeur, liste_heur, largeur, label='Joueur Heuristique, AVG = ' + str(avg_heur), color='#ff7f0e')  # orange
    plt.bar(indices + 0.5 * largeur, liste_proba, largeur, label='Joueur Probabiliste simplifiée, AVG = ' + str(avg_proba), color='#2ca02c')  # vert
    plt.bar(indices + 1.5 * largeur, liste_mc, largeur, label='Joueur Monte-Carlo, AVG = ' + str(avg_mc), color='#d62728')  # rouge

    # Ajouter des titres et des labels
    plt.title('Comparaison des joueurs', fontsize=16)
    plt.xlabel('Nombre d’essais', fontsize=14)
    plt.ylabel('Score', fontsize=14)

    # Créer des ticks personnalisés pour l'axe des abscisses
    plt.xticks(indices, rotation=90, ha='right', fontsize=8)

    # Ajuster la largeur des barres
    plt.tight_layout()

    # Ajouter une légende et une grille
    plt.legend(fontsize=12)
    plt.grid(axis='y')

    # Ajuster l'axe des abscisses pour éviter le chevauchement
    plt.xlim(-0.5, len(liste_alea) - 0.5)  # Ajuster les limites de l'axe x

    # Afficher le graphique
    plt.show()

if __name__ == '__main__':
    j_alea = JoeurAleatoire()
    j_heur = JoeurHeuristique()
    j_proba = JoeurProbabilisteSimplifiée()
    j_monte_carlo = JoeurMonteCarlo()
    
    nb_tour = 100
    a = j_alea.genere_ncoups( nb_tour)
    h = j_heur.genere_ncoups( nb_tour)
    p = j_proba.genere_ncoups( nb_tour)
    m = j_monte_carlo.genere_ncoups( nb_tour) # temps de calucle un peu long
    
    avg_mc = sum(m)/len(m)
    avg_proba=  sum(p)/len(p)
    avg_heur=  sum(h)/len(h)
    avg_alea=  sum(a)/len(a)
    
    dessin_graphique_un_joueur(a,avg_alea,"Joueur Aléatoire" )
    dessin_graphique_un_joueur(h,avg_heur,"Joueur Heuristique" )
    dessin_graphique_un_joueur(p,avg_proba,"Joueur Probabiliste simplifiée" )
    dessin_graphique_un_joueur(m,avg_mc,"Joueur Monte-Carlo" )
    dessin_graphique_all(a,h,p,m,avg_alea,avg_heur,avg_proba,avg_heur)

# section pour jouer de façon unitaire 
    #print(j_alea.joue())   
    #print(j_heur.joue())   
    #print(j_proba.joue())
    #print(j_monte_carlo.joue())