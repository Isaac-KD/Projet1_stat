from Game.Bataille import Bataille

from abc import ABC, abstractmethod
import random
import numpy as np

class Joeur(ABC):
    """
    Classe de base représentant un joueur.
    
    Attributes:
        bataille (Bataille): Instance de la classe Bataille gérant l'état du jeu.
    """
    def __init__(self):
        """
        Initialise une nouvelle instance de Joeur en créant une instance de Bataille.
        """
        self.bataille = Bataille()
    
    def reset(self):
        """
        Réinitialise l'état de la bataille.
        """
        self.bataille.reset()
        
    @abstractmethod
    def joue(self):  # Méthode abstraite
        """
        Simule une partie complète en jouant des coups aléatoires jusqu'à la victoire.

        Returns:
            int: Nombre de coups joués pour remporter la partie.
        """
        pass
    
    def genere_ncoups(self,n=100):
        """
        Génère une liste de résultats de n parties jouées de manière aléatoire.

        Args:
            n (int, optional): Nombre de parties à simuler. Par défaut à 100.

        Returns:
            List[int]: Liste des nombres de coups joués pour chaque partie.
        """
        return [self.joue() for _ in range(n)]
        
class JoeurAleatoire(Joeur):
    """
    Joueur qui choisit ses coups de manière aléatoire jusqu'à ce que tous les bateaux soient coulés.
    """
    def __init__(self):
        super().__init__()
             
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
    

class JoeurHeuristique(Joeur):
    """
    Joueur utilisant une approche heuristique. Lorsqu'un bateau est touché, il privilégie les tirs sur les cases adjacentes potentielles.
    """
    def __init__(self):
        super().__init__()
        
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
    
class JoeurProbabilisteSimplifiée(Joeur):
    """
    Joueur utilisant une approche probabiliste simplifiée. Le joueur calcule une matrice de probabilités pour déterminer les meilleures cases à viser.
    """
    def __init__(self):
        super().__init__()
    
    @staticmethod   
    def max_matrice(matrice):
        """
        Renvoie les coordonnées de l'élément maximum dans une matrice.

        Args:
            matrice (numpy.ndarray): Matrice dans laquelle rechercher le maximum.

        Returns:
            Tuple[int, int]: Coordonnées (x, y) de l'élément maximum.
        """
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
    
class JoeurMonteCarlo(Joeur):
    """
    Joueur utilisant l'algorithme Monte Carlo. Il simule plusieurs scénarios possibles pour estimer les meilleures cases à viser.
    """
    def __init__(self):
        super().__init__()   

    def max_matrice(self,matrice):
        """
        Renvoie les coordonnées de l'élément maximum dans une matrice, en évitant les cases déjà jouées dans la matrice de probabilitée.( la moyenne des matrices trouver grace a la methode de Monte-Carlo)

        Args:
            matrice (numpy.ndarray): Matrice dans laquelle rechercher le maximum.

        Returns:
            Tuple[int, int]: Coordonnées (x, y) de l'élément maximum valide.
        """
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

    def joue(self,n=10):
        cpt=0
        # matrice pour savoir si on deja jouer le coup 
        while not self.bataille.victoire(): # tant que tous les bateau ne sont pas couler
            matrice_proba = self.bataille.matrice_coup.monte_carlo(n)
            x,y = self.max_matrice(matrice_proba)
            self.bataille.joue((y,x))

            cpt+=1

        self.reset()
        return cpt