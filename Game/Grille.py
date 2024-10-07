import numpy as np 
import matplotlib.pyplot as plt
from Game.Bateau import Bateau
import copy 
import random

class Grille:
    """
    Représente une grille de jeu pour un jeu de bataille navale.

    Attributs :
        taille (int): La taille de la grille, par défaut 10.
        grille (numpy.ndarray): Matrice de taille (taille, taille) initialisée à zéro.
        liste_bateau (list): Liste des bateaux placés sur la grille.

    Méthodes :
        affiche(): Affiche la grille à l'aide de matplotlib.
        eq(grilleA, grilleB): Vérifie si deux grilles sont égales.
        add(bateau, position, direction): Ajoute un bateau à la grille.
        add_monte_carlo(bateau, position, direction): Ajoute un bateau à la grille avec vérification.
        peut_placer(bateau, position, direction): Vérifie si un bateau peut être placé à une position donnée.
        place(bateau, position, direction): Place un bateau sur la grille si possible.
        place_alea(bateau): Place un bateau de manière aléatoire sur la grille.
        case_possible(bateau, position, direction): Vérifie si un bateau peut être placé sur une case.
        find(pos): Cherche un bateau en fonction d'une position donnée.
        genere_grille(): Crée une grille générée aléatoirement avec des bateaux.
        grille_test(): Génère une grille de test avec des bateaux prédéfinis.
        peut_etre_placer(bateau, position, direction): Vérifie si un bateau peut être placé sans chevauchement.
        matrice_possibilite_solo(bateau): Crée une matrice représentant les positions possibles d'un bateau.
        matrice_possible_multi(): Calcule la matrice des positions possibles pour plusieurs bateaux.
        tous_combler(matrice_coups): Vérifie si toutes les cases de la matrice de coups sont couvertes.
        place_monte_carlo(bateau, matrice_coups): Place un bateau de manière aléatoire en respectant une matrice de coups.
        monte_carlo_solo(liste_bateau, matrice_coups, temps_max): Effectue une recherche Monte Carlo pour placer des bateaux.
        monte_carlo_find_matrice(matrice_coups, temps_max): Trouve une matrice valide pour le placement des bateaux.
        monte_carlo_multi(matrice_coups, n, temps_max): Exécute plusieurs simulations Monte Carlo pour trouver des solutions.
        monte_carlo(n, temps_max=1000): Effectue une recherche Monte Carlo pour placer les bateaux et retourne la grille.
    """
    
    def __init__(self,taille=10):
        """
        Initialise une nouvelle grille.

        Args:
            taille (int): La taille de la grille, par défaut 10.
        """
        self.taille = taille
        self.grille = np.zeros((taille, taille), dtype=int) # matrice de 0 de taille taille et de type int 
        self.liste_bateau=[] # liste des bateau dans la grille
        
    def affiche(self): 
        """Affiche la grille à l'aide de matplotlib."""
        plt.imshow(self.grille, cmap = 'viridis', vmin=self.grille.min(), vmax=self.grille.max())
        plt.show()
        
    @staticmethod
    def eq(grilleA,grilleB):
        """Vérifie si deux grilles sont égales.

        Args:
            grilleA (numpy.ndarray): La première grille.
            grilleB (numpy.ndarray): La deuxième grille.

        Returns:
            bool: True si les grilles sont égales, sinon False.
        """
        return np.array_equal(grilleA,grilleB) 
    
    def add(self, bateau, position,direction):
        """Ajoute un bateau à la grille à la position donnée dans la direction spécifiée.
           Attention:
               Il n'y a pas de vérification pour s'assurer que le bateau ne sort pas du tableau ; la fonction ajoute le bateau sur la grille sans vérification préalable.

        Args:
            bateau (Bateau): L'objet bateau à ajouter.
            position (tuple): Les coordonnées (x, y) de la position de départ.
            direction (str): La direction ('H' pour horizontal, 'V' pour vertical).
        """

        # Il n'y a pas de check sur le fait que le batau sort du tableau, la fonction ajoute le bateau sur la grille
        x,y = position 
        if direction == 'V':
            for i in range(bateau.taille):
                self.grille[y-i][x]= bateau.value
                bateau.body.append((x,y-i))
        else :
            for i in range(bateau.taille):
                self.grille[y][x+i]= bateau.value
                bateau.body.append((x+i,y))
                
    """    suppression a faire     
    def add_monte_carlo(self,bateau,position,direction): # Il n'y a pas de check sur le fait que le batau sort du tableau, la fonction ajoute le bateau sur la grille
        x,y = position 
        if direction == 'V':
            for i in range(bateau.taille):
                if self.grille[y-i][x] != -2:
                    self.grille[y-i][x]= bateau.value
                bateau.body.append((x,y-i))
        else :
            for i in range(bateau.taille):
                if self.grille[y-i][x] != -2:
                    self.grille[y][x+i]= bateau.value
                bateau.body.append((x+i,y))
      """          
    def peut_placer(self, bateau, position, direction):
        """Vérifie si un bateau peut être placé à une position donnée dans une direction.

        Args:
            bateau (Bateau): L'objet bateau à vérifier.
            position (tuple): Les coordonnées (x, y) de la position de départ.
            direction (str): La direction ('H' ou 'V').

        Returns:
            bool: True si le bateau peut être placé, sinon False.
        """
        x,y = position
        if x<0 or x>9 :return False
        if y<0 or y>9 :return False
        if direction == 'H' and bateau.taille+x >9: return False # check si le bateau est hors de la grille
        if direction == 'V' and y-bateau.taille <0 : return False
        if direction == 'H':
            for i in range(bateau.taille): # check si le bateau peut etre pacer sur la grille
                if not self.grille[y][x+i] == 0 : return False 
        if direction == 'V':
            for i in range(bateau.taille):
                if not self.grille[y-i][x] == 0: return False
        return True
            
    def place( self, bateau, position, direction): 
        """Place un bateau sur la grille si possible.

        Args:
            bateau (Bateau): L'objet bateau à placer.
            position (tuple): Les coordonnées (x, y) de la position de départ.
            direction (str): La direction ('H' ou 'V').

        Returns:
            bool: True si le bateau a été placé avec succès, sinon False.
        """
        if self.peut_placer(bateau, position, direction): # check de si c'est possible de placer le bateau
            self.add(bateau,position,direction) # ajoute du  bateau dans la grille 
            self.liste_bateau.append(bateau) # ajoute du  bateau dans la liste
            bateau.position = position
            return True
        else: 
            return False 

    def place_all(self): # permet de placer tout les bateau de base
        liste_non_placer = []
        #porte_avions 
        liste_non_placer.append( Bateau(5,1,(-1,-1),self))
        #croiseur
        liste_non_placer.append( Bateau(4,2,(-1,-1),self))
        #contre_torpilleurs
        liste_non_placer.append(Bateau(3,3,(-1,-1),self))
        #sous_marin
        liste_non_placer.append( Bateau(3,4,(-1,-1),self))
        #torpilleur 
        liste_non_placer.append( Bateau(2,5,(-1,-1),self))
        
        while liste_non_placer:
            x = liste_non_placer.pop()  # Extraire un bateau à placer
            placed = False  # Initialiser à False
            while not placed:  # Continuer jusqu'à placer le bateau
                placed = self.place_alea(x)
        
    def place_alea(self, bateau):
        """Place un bateau de manière aléatoire sur la grille.

        Args:
            bateau (Bateau): L'objet bateau à placer.

        Returns:
            bool: True si le bateau a été placé avec succès, sinon False.
        """
        # genere les coordonner aleatoirement
        x = int(np.random.uniform(0, 10)) 
        y = int(np.random.uniform(0, 10))
        if  np.random.uniform(0, 1)>0.5: return self.place(bateau,(x,y),'H')
        else: return self.place(bateau,(x,y),'V') # meme fonctionnement 
            
    
    def case_possible(self,bateau,position, direction):
        """Vérifie si un bateau peut être placé sur une case en tenant compte que 
           les cases touchées (-2) sont des cases où l'on peut placer une partie d'un bateau. 

        Args:
            bateau (Bateau): L'objet bateau à vérifier.
            position (tuple): Les coordonnées (x, y) de la position de départ.
            direction (str): La direction ('H' ou 'V').

        Returns:
            bool: True si la case est valide, sinon False.
        """
        x,y = position
        if x<0 or x>9 :return False
        if y<0 or y>9 :return False
        if direction == 'H' and bateau.taille+x >9: return False # check si le bateau est hors de la grille
        if direction == 'V' and y-bateau.taille <0 : return False
        if direction == 'H':
            for i in range(bateau.taille): # check si le bateau peut etre pacer su rla grille
                if not (self.grille[y][x+i] == 0 or self.grille[y][x+i] == -2): return False 
        if direction == 'V':
            for i in range(bateau.taille):
                if not( self.grille[y-i][x] == 0 or self.grille[y-i][x] == -2): return False
        return True
    
    def find(self,pos): 
        """Cherche un bateau en fonction d'une position donnée.

        Args:
            pos (tuple): Les coordonnées (x, y) à rechercher.

        Returns:
            Bateau: L'objet bateau trouvé à cette position ou None si aucun bateau n'est trouvé.
        """
        x,y = pos
        if self.grille[y][x] <= 0 :
            return None
        else :
            for bat in self.liste_bateau:
                if pos in bat.body: # cheche si la pos est dans les position possible du bateau
                    return bat
        return None
                
    @staticmethod                  
    def genere_grille():
        """Crée une grille générée aléatoirement avec des bateaux."""
        new = Grille()
        new.place_all()
        return new
    
    @staticmethod
    def grille_test(): 
        """Génère une grille de test avec des bateaux prédéfinis."""
        g = Grille()
        #porte_avions 
        g.place(Bateau(5,1,(-1,-1),g),(0,9),'V')
        #croiseur
        g.place( Bateau(4,2,(-1,-1),g),(1,9),'V')
        #contre_torpilleurs
        g.place(Bateau(3,3,(-1,-1),g),(2,9),'V')
        #sous_marin
        g.place(Bateau(3,4,(-1,-1),g),(3,9),'V')
        #torpilleur 
        g.place( Bateau(2,5,(-1,-1),g),(3,6),'V')
        return g
        
                    
    def peut_etre_placer(self,bateau,position,direction):
        """Vérifie si un bateau peut être placé sans chevauchement, en considérant que les cases touchées (-2) 
           sont acceptables, mais que le bateau ne doit pas être uniquement sur des cases touchées.
        Args:
            bateau (Bateau): L'objet bateau à vérifier.
            position (tuple): Les coordonnées (x, y) de la position de départ.
            direction (str): La direction ('H' ou 'V').

        Returns:
            bool: True si le bateau peut être placé, sinon False.
        """
        # check si le bateau n'est pas de la meme longueur que la trace
        x,y = position
        if x<0 or x>9 :return False
        if y<0 or y>9 :return False
        cpt=0
        if direction == 'H':
            if (x + bateau.taille > self.taille): return False
            for i in range(bateau.taille):
                if (self.grille[y][x+i] == -2): cpt+=1
                if (self.grille[y][x+i] == -1): return False # return False car impossible 
            return not cpt == bateau.taille
        else :
            if (y - bateau.taille <0): return False
            for i in range(bateau.taille):
                if (self.grille[y-i][x] == -2): cpt+=1
                if (self.grille[y-i][x] == -1): return False # return False car impossible 
            return (not cpt == bateau.taille) 

                
    def matrice_possibilite_solo(self, bateau):
        """Crée une matrice représentant les positions possibles d'un bateau.

        Args:
            bateau (Bateau): L'objet bateau à vérifier.

        Returns:
            numpy.ndarray: Matrice des positions possibles pour le bateau.
        """
        resultat = np.zeros((self.taille, self.taille))
        cpt = 0  # Compte les positions où le bateau peut être placé
        # Parcourt chaque case de la grille
        for x in range(self.taille): 
            for y in range(self.taille):
                # Vérifie si le bateau peut être placé horizontalement
                # Vérifie si le bateau peut être entièrement placé sans sortir de la grille
                if self.case_possible(bateau, (x, y), 'H') and (self.peut_etre_placer(bateau,(x,y),'H')):
                        for k in range(bateau.taille+1):
                            if self.grille[y][x + k] == 0: # inutile 
                                resultat[y][x + k] += 1
                                cpt += 1 

                # Vérifie si le bateau peut être placé verticalement
                # Vérifie si le bateau peut être entièrement placé sans sortir de la grille
                if self.case_possible(bateau, (x, y), 'V') and (self.peut_etre_placer(bateau,(x,y),'V')):
                        for k in range(bateau.taille+1):
                            if self.grille[y - k][x] == 0:
                                resultat[y - k][x] += 1
                                cpt += 1  

        # Si aucune position valide n'a été trouvée, éviter la division par 0
        if cpt > 0:
            return resultat /cpt
        else:
            return resultat  # Retourne la matrice sans division si cpt est nul donc la matrice null
    
    def matrice_possible_multi(self):
        """Calcule la matrice des positions possibles pour plusieurs bateaux.

        Returns:
            list: Liste des matrices des positions possibles pour chaque bateau.
        """
        nb_bateau = len(self.liste_bateau)
        matrice =  np.zeros((self.taille,self.taille)) # matrice de 0
        for b in self.liste_bateau: 
            matrice += self.matrice_possibilite_solo(b)
            # check si c'est pas la matrice null dans ce cas la on ne compte pas le bateau dans la liste des bateaux
            if not np.any(matrice != 0): nb_bateau -= 1
        return matrice /nb_bateau
    
    def tous_combler(self,matrice_coups):
        """Vérifie si toutes les cases de la matrice de coups sont couvertes. C'est a dire que tous les cases -2 sont couvertes

        Args:
            matrice_coups (numpy.ndarray): Matrice représentant les coups.

        Returns:
            bool: True si toutes les cases sont couvertes, sinon False.
        """
        for x in range(self.taille):
            for y in range(self.taille):
                if matrice_coups.grille[y][x] == -2 and self.grille[y][x] <= 0 : 
                    return False
        return True 
    
    def place_monte_carlo(self,bateau,matrice_coups):
        """Place un bateau de manière aléatoire en respectant la matrice de coups.

        Args:
            bateau (Bateau): L'objet bateau à placer.
            matrice_coups (numpy.ndarray): Matrice des coups.

        Returns:
            bool: True si le bateau a été placé avec succès, sinon False.
        """
        # genere les coordonner aleatoirement
        x = int(np.random.uniform(0, 10)) 
        y = int(np.random.uniform(0, 10))
        
        if  np.random.uniform(0, 1)>0.5 and matrice_coups.peut_etre_placer(bateau,(x,y),'H') and self.peut_placer(bateau,(x,y),'H'):
                for i in range(bateau.taille):
                    self.grille[y][x+i] = 1 
                return True
        elif matrice_coups.peut_etre_placer(bateau,(x,y),'V') and self.peut_placer(bateau,(x,y),'V'):
                for i in range(bateau.taille):
                    self.grille[y-i][x] = 1
                return True
        else:   
            return False
    
    def monte_carlo_solo(self,liste_bateau,matrice_coups,temps_max):
        """Effectue une recherche Monte Carlo pour placer les bateaux.
           Renvoie None si aucune solution n'est trouvée après temps_max tentatives.
        Args:
            liste_bateau (list): Liste des bateaux à placer.
            matrice_coups (numpy.ndarray): Matrice des coups.
            temps_max (int): Temps maximum en nombres de tours pour la recherche.

        Returns:
            numpy.ndarray: La grille après placement des bateaux.
            
        """
        if not liste_bateau: 
            if self.tous_combler(matrice_coups):
                return self.grille
            else: return None
            
        #choix = int(np.random.uniform(0, len(liste_bateau)))  Autre possibiliter mais moins optimisée
        #bateau=liste_bateau.pop(choix)
        
        bateau = random.choice(liste_bateau)
        liste_bateau.remove(bateau) 
        
        for _ in range(temps_max):
                if self.place_monte_carlo(bateau,matrice_coups): 
                    return self.monte_carlo_solo(liste_bateau,matrice_coups,temps_max)
        return None
        
    
    def monte_carlo_find_matrice(self,matrice_coups,temps_max):
        """Trouve une matrice valide pour le placement des bateaux.
           Renvoie None si aucune solution n'est trouvée après temps_max tentatives.
           Similaire à monte_carlo_solo, mais ici, on gère la liste des bateaux.
        Args:
            matrice_coups (numpy.ndarray): Matrice des coups.
            temps_max (int): Temps maximum en nombres de tours pour la recherche.

        Returns:
            numpy.ndarray: Matrice valide pour le placement des bateaux.
        """
        new_liste = copy.deepcopy(self.liste_bateau)
        new_grille = copy.deepcopy(self)
        sous_temps_max = int(temps_max*0.1) # on prend que 10 % du temps max pour chaque sous matrice pour pas que cela soit trop long
        
        for _ in range(temps_max):
            new_liste = copy.deepcopy(self.liste_bateau)
            new_grille  = copy.deepcopy(self)
            tmp =  new_grille.monte_carlo_solo(new_liste,matrice_coups, sous_temps_max) 
            if tmp is not None: 
                return tmp
        return None    # pour eviter un temps de calcul trop long

    def monte_carlo_multi(self,matrice_coups,n,temps_max):
        """Exécute plusieurs simulations Monte Carlo pour trouver n solutions.
           Si une tentative prend trop de temps à aboutir, on l'ignore, ce qui donne généralement entre 0 et 20 matrices.
           Cependant, dans la pratique, il est rare d'avoir des listes de moins de 20.
           Nous devons procéder ainsi, car parfois l'algorithme met beaucoup trop de temps à trouver une solution,
           mais cela n'affecte pas significativement l'espérance du nombre de coups.
        Args:
            matrice_coups (numpy.ndarray): Matrice des coups.
            n (int): Nombre de simulations. ( Nombre de grilles à chercher )
            temps_max (int): Temps maximum en millisecondes pour chaque simulation.

        Returns:
            numpy.ndarray: Grille après placement des bateaux.
        """

             # check si on le reussi a trouver un matrice en pas trop longtemps
        return [tmp for _ in range(n) if (tmp := self.monte_carlo_find_matrice(matrice_coups, temps_max)) is not None] 
    
    def monte_carlo(self,n,temps_max=2000):
        """Effectue une recherche Monte Carlo pour placer les bateaux et 
           retourne la grille des probabilités associée aux grilles trouvées grâce à la méthode Monte Carlo.

        Args:
            n (int): Nombre de simulations. ( Nombre de grilles à chercher )
            temps_max (int): Temps maximum en millisecondes pour chaque simulation.

        Returns:
            numpy.ndarray: Grille après placement des bateaux.
        """
        matice_start = Grille() # on crée une grille vierge pour pouvoir l'utilise pour ajouter les bateau placer 
        matice_start.liste_bateau =  [bat for bat in self.liste_bateau if bat.est_vivant()]   # on lieu associer les bateaux encore en vie
        liste = matice_start.monte_carlo_multi((self),n,temps_max)  
        if liste == []: return np.zeros((10,10))    # si aucune solution trouver on renvoie la matrice NULL
        return  np.sum(liste, axis=0)/len(liste)    # grille des probabilités
    