import numpy as np 

class Bateau():
    def __init__(self,taille,value,position=(-1,-1),direction='H'):
        self.corp = np.full(taille, value)
        self.value = value
        self.taille = taille
        self.position = position # position de la tete du bateau
        self.direction = direction
    
    def mouve(self,pos):
        self.position = pos
    
    def set_direction(self,direction):
        self.direction = direction