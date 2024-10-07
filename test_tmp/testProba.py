from Game.Grille import *
from Game.Bateau import *
import numpy as np

grille = Grille.genere_grille()
grille.grille = np.zeros((10,10))
matrice_coups = Grille()
matrice_coups.liste_bateau = grille.liste_bateau
#matrice_coups.grille[0][0] = -2
matrice_coups.grille[1][2] = -2
matrice_coups.grille[5][5] = -2
matrice_coups.grille[8][2] = -2

#print(grille.monte_carlo_multi(matrice_coups,10))
print(matrice_coups.monte_carlo(50))

