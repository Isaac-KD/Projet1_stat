from Game.Bataille import Bataille
from Game.Bateau import Bateau
from Game.Grille import Grille
import numpy as np
class TestBattaille():
    def __init__(self):
        self.bataille = Bataille()
    
    def test_bataille(self):
        
        b = Bataille()
        self.bataille.grille = Grille.grille_test()
        b.grille.grille = np.zeros((10,10))
        croiseur = Bateau(3,4,(-1,-1),b.grille)
        croiseur.pdv=-1
        b.grille.liste_bateau=[croiseur]
        if self.bataille.joue((0,9)): print(" check joue ok #1")
        else :print(" check joue faill #1")
        
        if not self.bataille.joue((9,9)): print(" check joue ok #2")
        else  :print(" check joue faill #2")
        
        if not self.bataille.victoire(): print(" check victoire ok #1")
        else: print(" check victoir faill #1")
        
        if b.victoire(): print(" check victoire ok #2 ")
        else:print(" check victoir faill #2 ")
        
        if self.bataille.case_conexe_possible((1,9)) == [(2, 9), (1, 8)] : print(" check case connexe ok #1")
        else : print(" check case connexe Faill #1")
        if (self.bataille.case_conexe_possible((1,8)) == [(0, 8), (2, 8), (1, 7), (1, 9)]):print(" check case connexe ok #2")
        else : print(" check case connexe Faill #2")
        
if __name__ == '__main__':
    testB = TestBattaille()
    testB.test_bataille()
    
        