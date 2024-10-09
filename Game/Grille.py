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
        genere_matrice_colision(): Genere un matrice avec colision
        grille_valide (liste): Renvoie true si la grille est valide
        configuration_pour_un_bateau(bateau): denombre le nombre de configuration possible pour un bateau
        trouver_grille_egale(): Cherche si la matrice ne possede pas de colision
        genere_invalide_grille(): Genere un grille invalide c'est a dire avec une colision
        verifie(self,pos,ps): Verifie si le sous-marrin ce situe bien dans la case et si il  est renvoie true avec une probabilité ps
        max_proba(): Renvoie la valeur maximim d'une matrice
        genere_grille_aleatoire(n): Genere un grille aleatoire ou les valeur sont les plus grand son centrer au plus vers le centre et dont la somme des valeur vaut 1
        find_sous_marrin(ps): Cherche un sous-marrin dans une matrice avec detecteur qui a une probabilité de ps de faire un faut negatif et de 1 pour les negatif
    """
    
    def __init__(self,taille=10):
        """
        Initialise une nouvelle grille.

        Args:
            taille (int): La taille de la grille, par défaut 10.
        """
        self.taille = taille
        self.grille = np.zeros((taille, taille)) # matrice de 0 de taille taille 
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
            for i in range(bateau.taille): # check si le bateau peut etre pacer sur la grille
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

    def place_all(self,liste_non_placer = None): # permet de placer tout les bateau de base
        if liste_non_placer == None:
            liste_non_placer = [Bateau(5,1,(-1,-1),self),Bateau(4,2,(-1,-1),self),Bateau(3,3,(-1,-1),self),Bateau(3,4,(-1,-1),self),Bateau(2,5,(-1,-1),self)]
            #liste = porte_avions ,croiseur,contre_torpilleurs,sous_marin,torpilleur 
        
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
    def genere_grille(liste=None):
        """Crée une grille générée aléatoirement avec des bateaux."""
        new = Grille()
        newliste = copy.deepcopy(liste)
        new.place_all(newliste)
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
            return not cpt == bateau.taille                  # check si le bateau est plus grand que la taille de la trace de -2 si elle existe   
        else :
            if (y - bateau.taille <0): return False
            for i in range(bateau.taille):
                if (self.grille[y-i][x] == -2): cpt+=1
                if (self.grille[y-i][x] == -1): return False # return False car impossible 
            return (not cpt == bateau.taille)                # check si le bateau est plus grand que la taille de la trace de -2 si elle existe  

                
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
        matrice =  np.zeros((self.taille,self.taille)) # matrice de 0
        liste_bateau_vivant = [bat for bat in self.liste_bateau if bat.est_vivant()] # liste des bateaux non couler
        nb_bateau = len(liste_bateau_vivant)
        for b in liste_bateau_vivant: 
            matrice += self.matrice_possibilite_solo(b)
            # check si c'est pas la matrice null dans ce cas la on ne compte pas le bateau dans la liste des bateaux
            if not np.any(matrice != 0): nb_bateau -= 1 # si on n'a reussi a placer 0 bateau pour le bateau selectioner
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
        
        # on place un bateau Horizontalement
        if  np.random.uniform(0, 1)>0.5 and matrice_coups.peut_etre_placer(bateau,(x,y),'H') and self.peut_placer(bateau,(x,y),'H'):
                for i in range(bateau.taille):
                    self.grille[y][x+i] = 1 
                return True # on a reussi a le placer 
            
        # on place un bateau veritaclement
        elif matrice_coups.peut_etre_placer(bateau,(x,y),'V') and self.peut_placer(bateau,(x,y),'V'):
                for i in range(bateau.taille):
                    self.grille[y-i][x] = 1
                return True  # on a reussi a le placer 
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
        # cas de base
        if not liste_bateau:                                # si la liste de bateau est vide 
            if self.tous_combler(matrice_coups):            # si tout les cases toucher sont combler 
                return self.grille                              # alors on renvoie la grille
            else: return None                               # sinon matrice non valide on renvoie None
        
        # on choisis un bateau
        bateau = random.choice(liste_bateau)                         
        liste_bateau.remove(bateau) 
        
        for _ in range(temps_max):                                                      # pour eviter les calcule trop long
                if self.place_monte_carlo(bateau,matrice_coups):                        # si on peut placer le bateau on fait un appel reccursif pour placer le prochain bateau 
                    return self.monte_carlo_solo(liste_bateau,matrice_coups,temps_max)
        return None                                                                     # aucun postion trouver en temps_max coup compte comme invalide 

    
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
            new_liste = copy.deepcopy(self.liste_bateau)    # on copy la liste car elle va etre modifier plus tard 
            new_grille  = copy.deepcopy(self)               # de meme la grille va etre modifie
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
    
    def genere_matrice_colision(self):
         """ 
         Renvoie une matrice avec des possibles colisions si il y a une colision alors on met dans les cases qui colision la somme des values des bateaux que l'on multiplie par -1
         """
         for bateau in self.liste_bateau:
            if random.random() >0.5: # On ajoute le bateau de maniere Horizontal et applique donc des condition sur les coorodnées 
                x = int(np.random.uniform(0, 10-bateau.taille)) 
                y = int(np.random.uniform(0, 10))
                for i in range(bateau.taille):
                    if self.grille[y][x+i] == 0: self.grille[y][x+i] = bateau.value # case vierge on ajoute le bateau
                    elif self.grille[y][x+i] >0:                                    # case contenant un bateau premiere colision on adition les deux et on multiplie par -1
                        a=self.grille[y][x+i]
                        self.grille[y][x+i] = (-1)*(a+bateau.value)
                    else:                                                            # case aillant deja eu une colision on a juste a y soustraire la value du nouveau bateau
                        self.grille[y][x+i] -= bateau.value
            else: # On ajoute le bateau de maniere Vertical et applique donc des condition sur les coorodnées
                x = int(np.random.uniform(0, 10)) 
                y = int(np.random.uniform(bateau.taille, 10))
                for i in range(bateau.taille):
                    if self.grille[y-i][x] == 0: self.grille[y-i][x] = bateau.value    # case vierge on ajoute le bateau
                    elif self.grille[y-i][x] >0:                                       # case contenant un bateau premiere colision on adition les deux et on multiplie par -1
                        a=self.grille[y-i][x]
                        self.grille[y-i][x] = (-1)*(a+bateau.value)
                    else:                                                              # case aillant deja eu une colision on a juste a y soustraire la value du nouveau bateau
                        self.grille[y][x+i] -= bateau.value
                        a = self.grille[y-i][x]
                        self.grille[y-i][x] -= bateau.value
                  
    def grille_valide(self)->bool:
        """ 
        Attention doit prendre une matrice genere par genere_matrice_colision!!
        
        Renvoie True si la matrice est valide c'est a dire que tout les elements sans plus grand que 0
        """
        x,y =  np.unravel_index( np.argmin(self.grille) , self.grille.shape) # renvoie les coordonées minimal de la matrice
        return ( self.grille[x][y] >=0)
    
    def configuration_pour_un_bateau(self,bateau) -> int :
        """ Bateau -> int
        Renvoie le nombre de configuration pour un bateau sur une grille de taille 10 x 10
        """
        cpt = 0
        for x in range(10):
            for y in range(10):
                if (self.peut_placer(bateau, (x,y), 'V')): 
                    cpt=cpt+1
                if (self.peut_placer(bateau, (x,y), 'H')):
                    cpt=cpt+1
        return cpt
        
    def trouver_grille_egale(self,liste) -> int :
        """ int[][] * int[] -> int
        Renvoie le nombre de grille générée pour retrouver la même grille que celle passée en paramètre
        """
        grilleGeneree = Grille.genere_grille(liste) # genere une grille aleatoirement en fonction d'une liste de bateau
        cpt = 1
        while not Grille.eq(self.grille, grilleGeneree.grille) :    
            grilleGeneree = Grille.genere_grille(liste)
            cpt += 1
        return cpt
    
    def genere_invalide_grille(self):
        """
        charge une grille invalide dans la Classe 
        """
        while self.grille_valide(): # temps que la grill est valide
            self.genere_matrice_colision()  # genere une matrice avec collision 
               
    def verifie(self,pos,ps)-> bool:
        """
        Vérifie si un capteur détecte correctement un point de la grille (marqué par la valeur 1), avec une probabilité d'exactitude donnée. et renvoie True 
        si le point avec un probabailité ps est present ,sinon False
        
        grid : np.array
            La grille 2D de dimensions NxN contenant des valeurs 0 et 1, où 1 représente un point d'intérêt.
        
        position : tuple[int, int]
            Coordonnées (x, y) sur la grille où le capteur va vérifier la présence du point d'intérêt.
        
        ps : float, optionnel
            La probabilité (entre 0 et 1) que le capteur détecte correctement la présence du point d'intérêt à la position donnée.
            La valeur par défaut est 0.8, ce qui signifie que le capteur détecte correctement dans 80% des cas.
        """
        x, y = pos
        if(self.grille[x][y] == 1):
            affiche = random.random()

            if(affiche < ps):
                return True
        
        return False

    def max_proba(self):
        """
        Renvoie les coordonée du maximun d'une matrice
        """
        return np.unravel_index(np.argmax(self.grille), (self.grille.shape)) 
    
    @staticmethod
    def genere_grille_aleatoire(n):
        """
        Génère une grille de probabilités aléatoires de dimensions N x N, où 
        les valeurs au centre de la grille sont plus probables que celles des bords. 
        La somme des valeurs dans la grille est normalisée à 1.
        """
        g = Grille()
        g.grille = np.random.rand(n,n)  # genere un grille aleatoire

        # Calcule du centre de la grille
        center = (n - 1) // 2

        # Appliquer un facteur de distance pour diminuer les valeurs en s'éloignant du centre
        fact = np.zeros((n, n))  # Correction de l'initialisation du tableau
        for i in range(n):
            for j in range(n):
                distance = np.sqrt((i - center) ** 2 + (j - center) ** 2)
                fact[i][j] = np.exp(-distance)  # Diminuer les valeurs avec la distance

        # Multiplier les valeurs aléatoires par le facteur de distance
        g.grille = fact*g.grille
        grid_sum = np.sum(g.grille)

        # Normaliser la grille pour que la somme soit égale à 1
        if grid_sum > 0:
            g.grille /= grid_sum

        return g
    
    def find_sous_marrin(self,ps = 0.8):
        """
        Implémente l'algorithme du scorpion pour optimiser une grille probabiliste.
        
        L'objectif est de maximiser une grille probabiliste  jusqu'à ce que l'on retrouve le sous-marin, 
        évaluée par la fonction `check`. Cette fonction met à jour les probabilités dans la grille en 
        fonction de la règle d'actualisation et renvoie le nombre d'iteration avant de troiuver le sous-marin.
        
        La Grille doit contenir que un sous-marrin de taille 1 
        
        Parameters
        ----------
        ps : float,
            La probabilité de sélection pour le sous-marin. Il influence la mise à jour des probabilités dans la grille.

        """
        # Nombre d'itérations
        iterations = 1
        grille_aleatoire = Grille.genere_grille_aleatoire(self.taille)
        # Max initiale de la grille
        x, y =  grille_aleatoire.max_proba()

        while not self.verifie((x, y), ps):
            pi_k = self.grille[x][y]
            
            # Mise à jour de la probabilité pour la case sélectionnée
            grille_aleatoire.grille[x][y] = ((1 - ps) * pi_k) / (1 - ps * pi_k)

            # Mise à jour des autres cases
            for i in range(self.taille):
                for j in range(self.taille):
                    if (i, j) != (x, y):
                        grille_aleatoire.grille[i][j] = grille_aleatoire.grille[i][j] / (1 - ps * pi_k)

            # Maximisation après mise à jour
            x, y =grille_aleatoire.max_proba()
            iterations += 1

        return iterations

        