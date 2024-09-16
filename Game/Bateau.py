import numpy as np 

class Bateau():
    def __init__(self,taille,value,position=(-1,-1),direction='H'):
        self.corp = np.full(taille, value) # jsp 
        self.value = value # valeur indiquer dans le pdf
        self.taille = taille 
        self.position = position # position de la tete du bateau
        self.direction = direction # 'H' ou 'V'
        self.body = [] # permet de visualiser le bateau et les cases touche peut etre remplacer par un int qui serait ca barre de vie 
        self.pdv = taille # le nombre de fois que l'on peut le toucher 
        
    def set_direction(self,direction): 
        self.direction = direction
    
    def est_vivant(self): 
        """
        Renvoie si le bateau est encore en vie donc a été toucher moins de taille fois
        """
        return self.pdv>0
        
        