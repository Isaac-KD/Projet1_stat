from Game.Grille import Grille
from Game.Bateau import Bateau
import numpy as np
import copy

class TestGrille():
    def __init__(self):
        self.grille = Grille()
        self.croiseur = Bateau(3,2)
        
    def test_grille(self):
        if self.grille.peut_placer(self.croiseur,(5,5),'H'): print("test peut placer check #1")
        else : print("Error test peut_placer #1")
        
        if self.grille.peut_placer(self.croiseur,(0,0),'H'): print("test peut placer check #2")
        else : print("Error test peut_placer #2")
        
        if not self.grille.peut_placer(self.croiseur,(9,9),'H'): print("test peut placer check #3")
        else : print("Error test peut_placer #3")
        
        if self.grille.peut_placer(self.croiseur,(5,5),'V'): print("test peut placer check #4")
        else : print("Error test peut_placer #4")
        
        if not self.grille.peut_placer(self.croiseur,(0,0),'V'): print("test peut placer check #5")
        else : print("Error test peut_placer #5")
        
        if self.grille.peut_placer(self.croiseur,(9,9),'V'): print("test peut placer check #6")
        else : print("Error test peut_placer #6")
    
        # test eq
        grilleA = np.array([[3,3],[4,4]])
        grilleB = np.zeros((2,2))
        grilleC = np.array([[3,3],[4,4]])
        
        if not Grille.eq(grilleA,grilleB): print("test eq check #1")
        else : print("Error test eq check #1")
        
        if Grille.eq(grilleA,grilleC): print("test eq check #2")
        else : print("Error test eq check #2")
        
        # test ADD
        self.grille.add(self.croiseur,(5,5),'H')
        for i in range(self.croiseur.taille):
       
            if not self.grille.grille[5][5+i] == self.croiseur.value:
                print("TEST ERRROR add check #1")
                break
        print("TEST add check #1")
            
        self.grille.add(self.croiseur,(9,9),'V')
        for i in range(self.croiseur.taille):
            if not self.grille.grille[9-i][9] == self.croiseur.value:
                print("TEST ERRROR add check #2")
                break
        print("TEST add check #2")

        # TEST ALEA 
        tmp = copy.deepcopy(self.grille.grille)
        self.grille.place_alea(self.croiseur)
        if Grille.eq(tmp,self.grille.grille): print("test ERRROT alea check #1")
        else: print("test alea check #1")
        
        #Test Genere_grille
        g=Grille.genere_grille()
        #g.affiche()
                                                     
if __name__ == '__main__':
    test = TestGrille()
    test.test_grille()   
    new = Grille.genere_grille()
    new.affiche()
    #test.grille.affiche() 