from Game.Bataille import Bataille
import random
import numpy as np

class Joeur():
    def __init__(self):
        self.bataille = Bataille()
        
class JoeurAleatoire(Joeur):
    def __init__(self):
        super().__init__()
        
    def reset(self):
        self.bataille.reset()
             
    def joue(self):
        cpt=0
        # matrice pour savoir si on deja jouer le coup 
        while not self.bataille.victoire(): # tant que tous les bateau ne sont pas couler
            # on choisis les coordonnées
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if self.bataille.matrice_coup.grille[y][x] == 0: # on a jamais jouer le coup
                cpt+=1
                self.bataille.joue((x, y))
        self.reset()
        return cpt
    
    def genere_ncoups(self,n=100):
        return [self.joue() for _ in range(n)]

class JoeurHeuristique(Joeur):
    def __init__(self):
        super().__init__()
        
    def reset(self):
        self.bataille.reset()
        
    def joue(self):
        cpt=0
        choisis=(-1,-1)
        pile=[]
        while not self.bataille.victoire():  # tant que tous les bateau ne sont pas couler
             # on choisi sles coordonnée 
            if pile != []:          # on a toucher un bateau   
                x,y = choisis
            else:  # on a pas toucher de  bateau   
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                
            if self.bataille.matrice_coup.grille[y][x] == 0: 
                cpt+=1
                if self.bataille.joue((x, y)):
                    liste_possible = self.bataille.case_conexe_possible((x,y)) # on prend tout les cases connexe jouable
                    pile+=liste_possible
            if pile != []: 
                choix = random.randint(0, len(pile)-1)
                choisis = pile.pop(choix) # on choisis une des cases connexe       
        self.reset()
        return cpt
    
    def genere_ncoups(self,n=100):
        return [self.joue() for _ in range(n)]
    
class JoeurProbabilisteSimplifiée(Joeur):
    def __init__(self):
        super().__init__()
    
    def reset(self):
        self.bataille.reset()
        
    def max_matrice(matrice):
        # renvoie les coordonnées du plus grand element d'un matrice
        return np.unravel_index( np.argmax(matrice) , matrice.shape) 
    
    def joue(self):
        cpt=0
        # matrice pour savoir si on deja jouer le coup 
        while not self.bataille.victoire(): # tant que tous les bateau ne sont pas couler
            matrice_proba = self.bataille.matrice_coup.matrice_possible_multi()
            x,y = JoeurProbabilisteSimplifiée.max_matrice(matrice_proba)
            self.bataille.joue((y,x))
            cpt+=1
        
        self.reset()
        return cpt

    def genere_ncoups(self,n=100):
        return [self.joue() for _ in range(n)]
    
class JoeurMonteCarlo(Joeur):
    def __init__(self):
        super().__init__()   
    
    def reset(self):
        self.bataille.reset() 
    
    def max_matrice(self,matrice):
        # renvoie les coordonnées du plus grand element d'un matrice
        if np.all(matrice == 0): 
            x =random.randint(0, 9)
            y = random.randint(0, 9)
            while self.bataille.matrice_coup.grille[x][y] !=0:
                x =random.randint(0, 9)
                y = random.randint(0, 9)
            return (x,y)
        x,y =  np.unravel_index( np.argmax(matrice) , matrice.shape) 
        if self.bataille.matrice_coup.grille[x][y] == -2:
            matrice[x][y] = 0
            return self.max_matrice(matrice)
        else:  return x,y

    def joue(self,n=20):
        cpt=0
        # matrice pour savoir si on deja jouer le coup 
        while not self.bataille.victoire(): # tant que tous les bateau ne sont pas couler
            matrice_proba = self.bataille.matrice_coup.monte_carlo(n)
            x,y = self.max_matrice(matrice_proba)
            self.bataille.joue((y,x))
            cpt+=1
            print(cpt)

        self.reset()
        return cpt

    def genere_ncoups(self,n=100):
        return [self.joue() for _ in range(n)]