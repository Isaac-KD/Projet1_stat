from Game.Grille import *
from Game.Bateau import *
grille = Grille.genere_grille()
grille.grille[5][5]=-2
grille.grille[5][3]=-2
grille.grille[5][4]=-2
port_avion = Bateau(5,1,(-1,-1),grille)
res = grille.matrice_possible_totaux((5,5))
np.savetxt('matrice.txt',res , fmt='%.15f') 
res2 = grille.matrice_possible_toucher_all((5,3))
np.savetxt('matrice2.txt',res2 , fmt='%.1f') 
g = Grille()
g.grille = res2
g.grille[5][3]=-2
g.grille[5][5]=-2
g.grille[5][4]=-2
#g.affiche()