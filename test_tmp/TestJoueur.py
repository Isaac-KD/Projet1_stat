from Game.Joueur import *

class TestJoeur():
    def __init__(self):
        self.j_alea = JoeurAleatoire()
        self.j_heur = JoeurHeuristique()
        self.j_proba = JoeurProbabilisteSimplifiée()
        self.j_mont  =  JoeurMonteCarlo()
    def test(self):
        #a = self.j_alea.joue()
        b = self.j_heur.joue()
        #c = self.j_proba.joue()
        #d = self.j_mont.joue()
        print(b)
if __name__ == '__main__':
    testj = TestJoeur()
    testj.test()
    