from Game.Grille import Grille
from Game.Bateau import Bateau
g = Grille()
b0 = Bateau(5,1)
b1 = Bateau(3,2)
b2 = Bateau(3,3)
b3 = Bateau(4,5)
g.liste_bateau = [b0,b1,b2,b3]
g.matrice_possibilite_solo(b0)
g.matrice_possible_multi()


