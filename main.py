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
print("Il y a un ",g.configuration_pour_un_bateau(liste_bateau[3])," configuration possible pour le sous-marrins")
# Genere une matrice invalide 
grille_invalide = Grille()
grille_invalide.liste_bateau = liste_bateau
grille_invalide.genere_invalide_grille()
#grille_invalide.affiche()      # pour afficher la grille

# trouver le nombre de convifuration
g.grille = np.zeros((g.taille,g.taille)) 
print("Il y'a ",g.configuration_pour_un_bateau(g.liste_bateau[0]), " configuration possible pour le port-avion") # pour le porte avions
print("Il y'a ",g.configuration_pour_liste_bateau(liste_bateau[2:])," configuration possible avec 3 bateau")

# trouver_grille_egale
g = Grille.genere_grille(liste_bateau[3:])      # on recrée une grille avec seulement 2 bateau
print("Il y a eu ",g.trouver_grille_egale(liste_bateau[3:])," essayent pour trouver uen grille similaire a g") 

# Trouver un sous-marrin echouer
grille_sous_marrin = Grille()
x ,y= int(np.random.uniform(0, 10)) ,int(np.random.uniform(0, 10)) 
grille_sous_marrin.grille[x][y] = 1
print("Il a fallut ",grille_sous_marrin.find_sous_marrin(),"coups pour trouver le sous-marrin")

