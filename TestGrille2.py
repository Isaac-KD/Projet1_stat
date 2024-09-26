from Game.Grille import Grille
from Game.Bateau import Bateau
import numpy as np

class TestGrille():
    def __init__(self):
        self.taille =10
        self.g = Grille.grille_test()
        self.g0 = Grille.grille_test()
        self.g0.grille =  np.zeros((self.taille, self.taille))
        self.croiseur = Bateau(3,2)
        self.prt_avion = Bateau(5,1)
        self.grille_toucher = Grille()
        self.grille_toucher.grille = np.zeros((self.taille,self.taille))
        self.grille_toucher.grille[7][2] = -2
        self.grille_toucher.grille[8][2] = -2
        self.grille_toucher.grille[9][2] = -2
        self.grille_toucher.grille[7][4] = -2
        self.grille_toucher.grille[7][5] = -2
        self.grille_toucher.liste_bateau.append(self.croiseur)
        self.grille_toucher.liste_bateau.append(self.prt_avion)
        

    def test_find_patern(self):
        assert(self.grille_toucher.find_patern((2,7)) == ([(2, 7)], [(2, 7), (2, 8), (2, 9)]))
        assert(self.grille_toucher.find_patern((5,7)) == ([(4, 7), (5, 7)], [(5, 7)]))
        
    def find_toucher_pos(self,bateau,pos):
        assert(self.grille_toucher.find_toucher_pos(self.croiseur,(2,7))  == ([(2, 7), (1, 7), (0, 7)], [(2,7)], False,False, True))
        assert(self.grille_toucher.find_toucher_pos(self.croiseur,(5,7)) == ([(4, 7), (3, 7)], [(5, 7), (5, 6), (5, 5)], True,False,False))
     
    def find_toucher(self):
        assert(self.grille_toucher.find_toucher() == (2,7))
        self.grille_toucher.grille[7][2] = 0
        assert(self.grille_toucher.find_toucher() == (2, 8))
        self.grille_toucher.grille[7][2] = -2
    
    def matrice_possibilite(self,bateau):
        res = (self.g0.matrice_possibilite(self.croiseur))
        assert(np.sum(res)>0.9999 and np.sum(res)<1.0000)
        
    def matrice_possible_toucher(self,bateau,pos):
        res = self.grille_toucher.matrice_possible_toucher(self.croiseur,(5,7))
        res[7][3]-=0.5
        res[7][6]-= 0.5
        assert( Grille.eq(res,np.zeros((10,10))))
        res = self.grille_toucher.matrice_possible_toucher(self.croiseur,(2,7))
        assert( Grille.eq(res,np.zeros((10,10))))
        
    def matrice_possible_totaux(self,pos):
        self.grille_toucher.matrice_possible_totaux()
        self.g0.matrice_possible_totaux()
    
    def matrice_possible_toucher_all_bis(self,pos):
        pos = self.grille_toucher.find_toucher()
        print(pos)
        print(self.grille_toucher.matrice_possible_toucher_all(pos))
    
    def test_grille(self):
        pos=(-1,-1)
        bateau = self.croiseur
        self.matrice_possible_toucher_all(pos)
        self.matrice_possible_totaux(pos)
        self.matrice_possible_toucher(bateau,pos)
        self.matrice_possibilite(bateau)
        self.find_toucher()
        self.find_toucher_pos(bateau,pos)
        self.test_find_patern()
            
if __name__ == '__main__':
    test = TestGrille()
    test.test_grille()
   # print(test.grille_toucher.grille)
    #test.g.affiche()
        