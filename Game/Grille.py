import numpy as np 
import matplotlib.pyplot as plt
from Game.Bateau import Bateau

class Grille():
    def __init__(self,taille=10):
        self.taille = taille
        self.grille = np.zeros((taille, taille), dtype=int) # matrice de 0 de taille taille et de type int 
        self.dico_bateau = {} # dico de bateau pour non utiliser
        self.liste_bateau=[] # liste des bateau dans la grille
        
    def affiche(self): 
        plt.imshow(self.grille, cmap='viridis') 
        plt.show()
    
    def eq(grilleA,grilleB):
        return np.array_equal(grilleA,grilleB) 
    
    def peut_placer(self, bateau, position, direction):
        x,y = position
        if x<0 or x>9 :return False
        if y<0 or y>9 :return False
        if direction == 'H' and bateau.taille+x >9: return False # check si le bateau est hors de la grille
        if direction == 'V' and y-bateau.taille <0 : return False
        if direction == 'H':
            for i in range(bateau.taille): # check si le bateau peut etre pacer su rla grille
                if not self.grille[y][x+i] == 0: return False 
        if direction == 'V':
            for i in range(bateau.taille):
                if not self.grille[y-i][x] == 0: return False
        return True
    
    def add(self, bateau, position,direction): # Il n'y a pas de check sur le fait que le batau sort du tableau, la fonction ajoute le bateau sur la grille
        x,y = position 
        if direction == 'V':
            for i in range(bateau.taille):
                self.grille[y-i][x]= bateau.value
                bateau.body.append((x,y-i))
        else :
            for i in range(bateau.taille):
                self.grille[y][x+i]= bateau.value
                bateau.body.append((x+i,y))
                
    def ajoute_dico(self,bateau): # non utliser 
        clee = bateau.value
        if clee in self.dico_bateau:
            self.dico_bateau[clee].append(bateau)
        else:
            self.dico_bateau[clee] = [bateau]
            
    def place( self, bateau, position, direction): # permet de placer le bateau sur la grille renvoie true si le bateau est placer false sinon
        if self.peut_placer(bateau, position, direction): # check de si c'est possible de placer le bateau
            self.add(bateau,position,direction) # ajoute du  bateau dans la grille 
            self.ajoute_dico(bateau)
            self.liste_bateau.append(bateau) # ajoute du  bateau dans la liste
            bateau.position = position
            return True
        else: 
            return False 

    def place_alea(self, bateau): # meme fonctionement que place
        # genere les coordonner aleatoirement
        x = int(np.random.uniform(0, 10)) 
        y = int(np.random.uniform(0, 10))
        destiniation = np.random.uniform(0, 2)
        if  np.random.uniform(0, 1)>0.5: res = self.place(bateau,(x,y),'H')
        else: res = self.place(bateau,(x,y),'V') # meme fonctionnement 
        return res
    
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
        placed = True
        
        while liste_non_placer:
            if placed :
                x = liste_non_placer.pop()
            placed = self.place_alea(x)  
    
    def find(self,pos): # cheche si un bateau en fonction d'une position
        x,y = pos
        if self.grille[y][x] <= 0 :
            return None
        else :
            for bat in self.liste_bateau:
                if pos in bat.body: # cheche si la pos est dans les position possible du bateau
                    return bat
        return None
    
    def toucher(self,pos): # simule la touche d'un bateau 
        x,y = pos
        if self.grille[y][x] > 0 :
            b = self.find(pos)  # cheche le bateau toucher 
            self.grille[y][x]=-1
            b.pdv-=1
            if not b.est_vivant(): # check si le bateau a encore au moins un case non toucher
                print(" Coulerrrrr ")
           
    def genere_grille(): # creer une grille genere aleatoirement 
        new = Grille()
        new.place_all()
        return new

    def grille_test(): # permet de genere une grille pour les tests
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
        
            