from Game.Grille import Grille

class Bataille():
    """
    Classe représentant le jeu de bataille navale.

    Cette classe gère la génération des grilles de jeu, le suivi des coups joués,
    la détection des touches, la vérification des conditions de victoire, et la réinitialisation du jeu.
    """
    
    def __init__(self):
        """
        Initialise une nouvelle partie de bataille navale.

        Génère une grille de jeu principale avec les bateaux placés aléatoirement
        et initialise une matrice des coups pour suivre les tentatives du joueur.
        """
        self.grille = Grille.genere_grille()
        self.matrice_coup = Grille()
        self.matrice_coup.liste_bateau = self.grille.liste_bateau
        
    def joue(self,position)-> bool: 
        """
        Joue un coup à la position spécifiée.

        Vérifie si la position choisie touche un bateau. Si c'est le cas, 
        la méthode `toucher` est appelée pour gérer la touche. Sinon, 
        la matrice des coups est mise à jour pour indiquer un manque.

        Args:
            position (Tuple[int, int]): Coordonnées du coup sous la forme (x, y).

        Returns:
            bool: `True` si le coup touche un bateau, `False` sinon.
        """
        x,y = position
        if (self.grille.grille[y][x] > 0) and (self.matrice_coup.grille[y][x] == 0):    # si la case est valide on appel la fonction toucher 
            self.toucher(position)
            return True
    
        self.matrice_coup.grille[y][x] -=1  # sinon on marque le coup comme un echec
        return False
    
    def victoire(self) -> bool:
        """
        Vérifie si tous les bateaux ont été coulés.

        Parcourt la liste des bateaux et vérifie si chacun d'eux est coulé.

        Returns:
            bool: `True` si tous les bateaux sont coulés, `False` sinon.
        """
        for bateau in self.grille.liste_bateau:
            if bateau.est_vivant(): return False
        return True
    
    def reset(self):
        """
        Réinitialise la partie en générant une nouvelle grille de jeu.

        Remplace la grille actuelle par une nouvelle grille avec des bateaux 
        repositionnés aléatoirement et réinitialise la matrice des coups.
        """
        self.grille = Grille.genere_grille()
        self.matrice_coup = Grille()
        self.matrice_coup.liste_bateau = self.grille.liste_bateau
        
    def toucher(self,pos):
        """
        Gère la logique lorsqu'un bateau est touché à une position donnée.

        Met à jour la matrice des coups pour indiquer une touche,
        réduit les points de vie du bateau touché, et si le bateau est coulé,
        marque toutes ses positions comme coulées.

        Args:
            pos (Tuple[int, int]): Coordonnées de la touche sous la forme (x, y).
        """
        x,y = pos
        if self.grille.grille[y][x] > 0 :
            self.matrice_coup.grille[y][x]=-2
            b = self.grille.find(pos)  # cherche le bateau toucher 
            b.pdv-=1
            if not b.est_vivant(): # check si le bateau a encore au moins une case non toucher
                for pos_old in b.body: # remplace les cases -2 par -1
                    x,y = pos_old
                    self.matrice_coup.grille[y][x] = -1
                
    def case_conexe_possible(self,pos):
        """
        Renvoie les cases adjacentes jouables à une position donnée.

        Les cases adjacentes doivent être à l'intérieur des limites de la grille
        et ne doivent pas avoir déjà été jouées.

        Args:
            pos (Tuple[int, int]): Coordonnées de référence sous la forme (x, y).

        Returns:
            List[Tuple[int, int]]: Liste des positions adjacentes jouables.
        """
        x,y= pos
        liste_possible=[]
        if x-1>=0 and self.grille.grille[y][x-1]>=0 and self.matrice_coup.grille[y][x-1]>=0: 
                liste_possible.append((x-1,y))
                
        if x+1<=9  and self.grille.grille[y][x+1]>=0 and self.matrice_coup.grille[y][x+1]>=0:
                liste_possible.append((x+1,y))
                
        if y-1>=0  and self.grille.grille[y-1][x]>=0 and self.matrice_coup.grille[y-1][x]>=0:
                liste_possible.append((x,y-1))
        if y+1<=9  and self.grille.grille[y+1][x]>=0 and self.matrice_coup.grille[y+1][x]>=0:
                liste_possible.append((x,y+1))     
        return liste_possible      
        
        