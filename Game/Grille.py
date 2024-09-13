import numpy as np 
import matplotlib.pyplot as plt
from Game.Bateau import Bateau

class Grille():
    def __init__(self,taille=10):
        self.grille = np.zeros((taille, taille), dtype=int)
        self.dico_bateau = {}
        self.liste_bateau=[]
        
    def affiche(self):
        plt.imshow(self.grille, cmap='viridis') 
        plt.show()
    
    def eq(grilleA,grilleB):
        return np.array_equal(grilleA,grilleB)
    
    def peut_placer(self, bateau, position, direction):
        x,y = position
        if x<0 or x>9 :return False
        if y<0 or y>9 :return False
        if direction == 'H' and bateau.taille+x >9: return False
        if direction == 'V' and y-bateau.taille <0 : return False
        if direction == 'H':
            for i in range(bateau.taille):
                if not self.grille[y][x+i] == 0: return False
        if direction == 'V':
            for i in range(bateau.taille):
                if not self.grille[y-i][x] == 0: return False
        return True
    
    def add(self, bateau, position,direction): # Il n'y a pas de check sur le fait que le batau sort du tableau
        x,y = position 
        if direction == 'V':
            for i in range(bateau.taille):
                self.grille[y-i][x]= bateau.value
                bateau.body[i] = (x,y-i)
        else :
            for i in range(bateau.taille):
                self.grille[y][x+i]= bateau.value
                bateau.body[i] = (x+i,y)
                
    def ajoute_dico(self,bateau):
        clee = bateau.value
        if clee in self.dico_bateau:
            self.dico_bateau[clee].append(bateau)
        else:
            self.dico_bateau[clee] = [bateau]
            
    def place( self, bateau, position, direction):
        if self.peut_placer(bateau, position, direction):
            self.add(bateau,position,direction)
            self.ajoute_dico(bateau)
            self.liste_bateau.append(bateau)
            bateau.position = position
            return True
        else: 
            return False 

    def place_alea(self, bateau):
        x = int(np.random.uniform(0, 10))
        y = int(np.random.uniform(0, 10))
        destiniation = np.random.uniform(0, 2)
        if  np.random.uniform(0, 1)>0.5: res = self.place(bateau,(x,y),'H')
        else: res = self.place(bateau,(x,y),'V')
        return res
    
    def place_all(self,liste=):
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
        placed = True
        
        while liste_non_placer:
            if placed :
                x = liste_non_placer.pop()
            placed = self.place_alea(x)  
    
    def find(self,pos):
        x,y = pos
        if self.grille[y][x] <= 0 :
            return None
        else :
            for bat in self.liste_bateau:
                if pos in self.body:
                    return bat
        return None
    
    def toucher(self,pos):
        x,y = pos
        if self.grille[y][x] > 0 :
            self.grille[y][x]=-1
            b = find(self,pos)
            b.pdv-=1
            if not b.est_vivant():
                print(" Coulerrrrr ")
                
        
    def genere_grille():
        new = Grille()
        new.place_all()
        return new