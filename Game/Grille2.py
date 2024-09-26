import numpy as np 
import matplotlib.pyplot as plt
from Game.Bateau import Bateau
import copy 

class Grille():
    def __init__(self,taille=10):
        self.taille = taille
        self.grille = np.zeros((taille, taille), dtype=int) # matrice de 0 de taille taille et de type int 
        self.dico_bateau = {} # dico de bateau pour non utiliser
        self.liste_bateau=[] # liste des bateau dans la grille
        
    def affiche(self): 
        plt.imshow(self.grille, cmap='viridis', vmin=self.grille.min(), vmax=self.grille.max())
        plt.show()

    
    def eq(grilleA,grilleB):
        return np.array_equal(grilleA,grilleB) 
    
    def pos_possible(self,pos):
        x,y = position
        if x<0 or x>9 :return False
        if y<0 or y>9 :return False
        return True
    
    def peut_placer(self, bateau, position, direction):
        x,y = position
        if x<0 or x>9 :return False
        if y<0 or y>9 :return False
        if direction == 'H' and bateau.taille+x >9: return False # check si le bateau est hors de la grille
        if direction == 'V' and y-bateau.taille <0 : return False
        if direction == 'H':
            for i in range(bateau.taille): # check si le bateau peut etre pacer su rla grille
                if not self.grille[x+i][y] == 0: return False 
        if direction == 'V':
            for i in range(bateau.taille):
                if not self.grille[x][y-i] == 0: return False
        return True
    
    def add(self, bateau, position,direction): # Il n'y a pas de check sur le fait que le batau sort du tableau, la fonction ajoute le bateau sur la grille
        x,y = position 
        if direction == 'V':
            for i in range(bateau.taille):
                self.grille[x][y-i]= bateau.value
                bateau.body.append((x,y-i))
        else :
            for i in range(bateau.taille):
                self.grille[x+i][y]= bateau.value
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
            
    def find_patern(self,pos):
        x,y= pos
        liste_h=[pos] # patern horizontat
        liste_v=[pos]  # patern vertical 
        k=1
        
        while x-k>=0 and self.grille[x-k][y] == -2 : 
            liste_h.insert(0,(x-k,y))
            k+=1
            
        k=1
        while x+k<=9  and self.grille[x+k][y]== -2:
                liste_h.append((x+k,y))
                k+=1
        
        k=1    
        while y-k>=0  and self.grille[x][y-k]== -2:
                liste_v.append((x,y-k))
                k+=1
         
        k=1      
        while y+k<=9  and self.grille[x][y+k]== -2:
                liste_v.insert(0,(x,y+k))   
                k+=1
                
        return liste_h,liste_v
         
    def case_connexes_possible(self,pos): # non utiliser 
        liste_possible =[]
        if x-1>=0 and self.grille.grille[x-1][y]>=0: 
            liste_possible.append((x-1,y))
        if x+1<=9  and self.grille.grille[x+1][y]>=0:
                liste_possible.append((x+1,y)) 
        if y-1>=0  and self.grille.grille[x][y-1]>=0:
                liste_possible.append((x,y-1))
        if y+1<=9  and self.grille.grille[x][y+1]>=0:
                liste_possible.append((x,y+1))   
        return liste_possible
    
    def find_toucher_pos(self,bateau,pos): # cherche a savoir si le bateau peut correspondre , c'est a dire que le bateau correspond au patern de -2 ex si il y a 3 -2 qui ce suive alors seul les bateau de taille plusgrand que 3 peuvent correspondre
        x,y = pos
        h,v = self.find_patern(pos)
        pos_possible_h = []
        pos_possible_v =[]
 
        if len(h)<bateau.taille:
            xht,yht = h[0] # x,y en tete de patern horizontal
            xvd,yvd = v[0] # x,y en queue
            
            for k in range(bateau.taille - len(h)):
                if xht-k>=0 and  self.grille[xht-k][yht] >=0: # on chech si les k cases a gauche du dernier -2 vu est disponible  et correspond au patern trouver ( la trace de -2)
                    pos_possible_h.append((xht-k,yht))
                    
            for k in range(bateau.taille - len(v)):
                if yvd+k <=9 and self.grille[xvd][yvd+k] >=0: # on chech si les k cases en haut du dernier -2 vu est disponible  et correspond au patern trouver ( la trace de -2)
                    pos_possible_v.append((xvd,yvd+k))
                  
        return pos_possible_h, pos_possible_v, len(h)>len(v)
    
    def find(self,pos): # cheche si un bateau en fonction d'une position
        x,y = pos
        if self.grille[x][y] <= 0 :
            return None
        else :
            for bat in self.liste_bateau:
                if pos in bat.body: # cheche si la pos est dans les position possible du bateau
                    return bat
        return None
    
    def find_toucher(self): # renvoie une case ou il y a un bateau toucher donc -2
        for x in range(self.taille):
            for y in range(self.taille):
                if self.grille[x][y] ==-2:
                    return (x,y)
        return(-1,-1)   
            
    def toucher(self,pos): # simule la touche d'un bateau 
        x,y = pos
        if self.grille[x][y] > 0 :
            b = self.find(pos)  # cheche le bateau toucher 
            self.grille[x][y]=-2
            b.pdv-=1
            if not b.est_vivant(): # check si le bateau a encore au moins une case non toucher
                for pos_old in b.body: # remplace les cases -2 par -1
                    x,y = pos_old
                    self.grille[x][y] = -1
                print(" Coulerrrrr ")
                
    def matrice_possibilite(self,bateau): # renvoie une grille avec les probabilités que chaque case contient le bateau en question
        resultat = np.zeros((self.taille,self.taille))
        cpt=0
        for x in range(self.taille): 
            for y in range(self.taille):
                if self.peut_placer(bateau,(x,y),'H'):
                    for k in range(bateau.taille):
                        resultat[x+k][y]+=1
                    cpt+=1
                if self.peut_placer(bateau,(x,y),'V'):
                    for k in range(bateau.taille):                 
                        resultat[x][y-k]+=1
                    cpt+=1  
        return resultat / cpt   
       
    def matrice_possible_toucher(self,bateau,pos):
        resultat = np.zeros((self.taille,self.taille)) # matrice de 0
        l_possible_h,l_possible_v , h_plus_grand = self.find_toucher_pos(bateau,pos) # liste de case ou le bateau pourrais etre 
        if h_plus_grand:
            for x,y in l_possible_h :
                for k in range(bateau.taille):
                    if y+k <=9 and self.grille[x][y+k] >= 0: resultat[x][y+k]+=1 /(len( l_possible_h))
        else:   
            print("liste = ",l_possible_v)             
            for x,y in l_possible_v :
                for k in range(bateau.taille):
                    if x+k <=9 and self.grille[x+k][y] >= 0: resultat[x+k][y]+=1/(len(l_possible_v))
        print(bateau.taille,resultat)     #################################################################             
        return resultat
                      
    def matrice_possible_totaux(self,pos):
        l = copy.deepcopy(self.liste_bateau)
        premier_bateau = l.pop()
        matrice = self.matrice_possibilite(premier_bateau)
        for b in l: matrice+= self.matrice_possibilite(b)
        return matrice / len(self.liste_bateau)
    
    def matrice_possible_toucher_all(self,pos):
        print(self.liste_bateau) ##############################################################
        matrice = np.zeros((self.taille,self.taille)) # matrice de 0
        nb_bateau=len(self.liste_bateau)
        for bateau in self.liste_bateau:
            matrice+= self.matrice_possible_toucher(bateau,pos)
            if not np.any(matrice != 0):
                print("b =", bateau.taille)################################
                nb_bateau-=1
                
        return matrice/nb_bateau
            
                
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
        