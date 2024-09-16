from Game.Joueur import *

class TestJoeur():
    def __init__(self):
        self.j_alea = JoeurAleatoire()
        self.j_heur = JoeurHeuristique()
    def test(self):
        a = self.j_alea.joue()
        b = self.j_heur.joue()
        print(a, b)
        
if __name__ == '__main__':
    testj = TestJoeur()
    testj.test()
    