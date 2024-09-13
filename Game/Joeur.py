from Game.Battaile import Bataille
import random
class Joeur():
    def __init__(self):
        self.bataille = Bataille()
        
class JoeurAleatoire(Joeur):
    def __init__(self):
        super().__init__()
        
    def joue(self):
        cpt=0
        # matrice pour savoir si on deja jouer le coup 
        matrice_coups = np.zeros((self.bataille.grille.taille, self.bataille.grille.taille), dtype=int)
        while self.bataille.victoire(): # tant que tous les bateau ne sont pas couler
            # on choisi sles coordonnée 
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            cpt+=1
            if matrice_coups[y][x] != 0: pass # on deja jouer ce coup
            self.bataille.joue((x, y))
        return cpt

class JoeurHeuristique(Joeur):
    def __init__(self):
        super().__init__()
        
    def joue(self):
        cpt=0
        # matrice pour savoir si on deja jouer le coup 
        matrice_coups = np.zeros((self.bataille.grille.taille, self.bataille.grille.taille), dtype=int)
        toucher=False # peremet de savoir si on toucher un bateau au tour precedent
        new_pos=(-1,-1) # pos du coup précedent
        while self.bataille.victoire():  # tant que tous les bateau ne sont pas couler
             # on choisi sles coordonnée 
            if toucher:          # on a toucher un bateau   
                x,y = choisis
                toucher=False
            else:  # on a pas toucher de  bateau   
                x = random.randint(0, 10)
                y = random.randint(0, 10)
            cpt+=1
            if matrice_coups[y][x] != 0: pass # on a deja jouer ce coup
            if self.bataille.joue((x, y)):
                liste_possible = self.bataille.case_conexe_possible() # on prend tout les cases connexe jouable
                chosis = random.randint(0, len(liste_possible)-1) # on choisis une des cases connexe
                toucher=True
        return cpt

class JoeurProbabilisteSimplifiée(Joeur):
    def __init__(self):
        super().__init__()

class JoeurMonteCarlo(Joeur):
    def __init__(self):
        super().__init__()      