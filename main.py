from Game.Grille import Grille
from Game.Bateau import Bateau
import numpy as np

# Intialization des données dont on besoin 
g = Grille()
#porte_avions 
g.liste_bateau.append( Bateau(5,1,(-1,-1),g))
#croiseur
g.liste_bateau.append( Bateau(4,2,(-1,-1),g))
#contre_torpilleurs
g.liste_bateau.append(Bateau(3,3,(-1,-1),g))
#sous_marin
g.liste_bateau.append( Bateau(3,4,(-1,-1),g))
#torpilleur 
g.liste_bateau.append( Bateau(2,5,(-1,-1),g))

liste_bateau = g.liste_bateau

# nombre de combinaison pour un bateau
print(" Il y a un ",g.configuration_pour_un_bateau(liste_bateau[3])," configuration possible pour le sous-marrins")
# Genere une matrice invalide 
grille_invalide = Grille()
grille_invalide.liste_bateau = liste_bateau
grille_invalide.genere_invalide_grille()
grille_invalide.affiche()

g.grille = np.zeros((g.taille,g.taille)) 
tmp = Grille()
print("Il y'a ",g.configuration_pour_un_bateau(g.liste_bateau[0]), " configuration possible pour le port-avion") # pour le porte avions

# trouver_grille_egale
g = Grille.genere_grille(liste_bateau[3:])      # on recrée une grille avec seulement 2 bateau
print(" Il y a eu ",g.trouver_grille_egale(liste_bateau[3:])," essayent pour trouver uen grille similaire a g") 


        

