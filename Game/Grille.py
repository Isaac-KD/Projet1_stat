import numpy as np 
import matplotlib.pyplot as plt
from Game.Bateau import Bateau
import copy 

class Grille():
    def __init__(self,taille=10):
        self.taille = taille
        self.grille = np.zeros((taille, taille), dtype=int) # matrice de 0 de taille taille et de type int 
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
            for i in range(bateau.taille): # check si le bateau peut etre pacer sur la grille
                if not self.grille[y][x+i] == 0 : return False 
        if direction == 'V':
            for i in range(bateau.taille):
                if not self.grille[y-i][x] == 0: return False
        return True
    
    def case_possible(self,bateau,position, direction):
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
                if not( self.grille[y-i][x] == 0 or self.grille[y][x+i] == -2): return False
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
            
    def place( self, bateau, position, direction): # permet de placer le bateau sur la grille renvoie true si le bateau est placer false sinon
        if self.peut_placer(bateau, position, direction): # check de si c'est possible de placer le bateau
            self.add(bateau,position,direction) # ajoute du  bateau dans la grille 
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
        liste_h=[] # patern horizontat
        liste_v=[]  # patern vertical 
        
        k=0
        while x-k >= 0 and self.grille[y][x-k] == -2 : 
            liste_h.insert(0,(x-k,y))
            k+=1
            
        k=1 
        while x+k <= 9  and self.grille[y][x+k]== -2:
            liste_h.append((x+k,y))
            k+=1
        
        k=0
        while y-k >= 0  and self.grille[y-k][x]== -2:
                liste_v.insert(0,(x,y-k))
                k+=1
         
        k=1
        while y+k <= 9  and self.grille[y+k][x]== -2:
                liste_v.append((x,y+k))   
                k+=1
                
        return liste_h,liste_v
         
    def case_connexes_possible(self,pos): # non utiliser 
        liste_possible =[]
        if x-1>=0 and self.grille.grille[y][x-1]>=0: 
            liste_possible.append((x-1,y))
        if x+1<=9  and self.grille.grille[y][x+1]>=0:
                liste_possible.append((x+1,y)) 
        if y-1>=0  and self.grille.grille[y-1][x]>=0:
                liste_possible.append((x,y-1))
        if y+1<=9  and self.grille.grille[y+1][x]>=0:
                liste_possible.append((x,y+1))   
        return liste_possible
    
    def find_toucher_pos(self,bateau,pos): # cherche a savoir si le bateau peut correspondre , c'est a dire que le bateau correspond au patern de -2 ex si il y a 3 -2 qui ce suive alors seul les bateau de taille plus grand que 3 peuvent correspondre
        x,y = pos
        h,v = self.find_patern(pos)
        pos_possible_h = []
        pos_possible_v =[]
        flag_v = False
        flag_h = False
        if len(h) == len(v) and len(v) == 0: return None,None,None
        if len(h) <= bateau.taille:
            xh,yh = h[0] # x,y en tete de patern horizontal
            xv,yv= v[0] # x,y en tete 
            
            for k in range(bateau.taille - len(h)+1):
                if xh-k>=0 and  self.grille[yh][xh-k] !=-1: # on chech si les k cases a gauche du dernier -2 vu est disponible  et correspond au patern trouver ( la trace de -2)
                    pos_possible_h.append((xh-k,yh))
                    
            for k in range(bateau.taille - len(v)+1):
                if yv-k <=9 and self.grille[yv-k][xv] !=-1: # on chech si les k cases en haut du dernier -2 vu est disponible  et correspond au patern trouver ( la trace de -2)
                    pos_possible_v.append((xv,yv-k))
        
        # on met le flag a True pour que les fonctions qui utilise cette fonction soit au courant que le bateau ne peut pas etre placer ici
        if len(v) == bateau.taille: flag_v = True 
        if len(h) == bateau.taille: flag_h = True
        
        return pos_possible_h, pos_possible_v, (len(h)>len(v) and (len(pos_possible_h) != [])),flag_h,flag_v
    
    def find(self,pos): # cheche si un bateau en fonction d'une position
        x,y = pos
        if self.grille[y][x] <= 0 :
            return None
        else :
            for bat in self.liste_bateau:
                if pos in bat.body: # cheche si la pos est dans les position possible du bateau
                    return bat
        return None
    
    def find_toucher(self): # renvoie une case ou il y a un bateau toucher donc -2
        for x in range(self.taille):
            for y in range(self.taille):
                if self.grille[y][x] ==-2:
                    return (x,y)
        return(-1,-1)   
            
    def toucher(self,pos): # simule la touche d'un bateau 
        x,y = pos
        if self.grille[y][x] > 0 :
            b = self.find(pos)  # cheche le bateau toucher 
            self.grille[y][x]=-2
            b.pdv-=1
            if not b.est_vivant(): # check si le bateau a encore au moins une case non toucher
                for pos_old in b.body: # remplace les cases -2 par -1
                    x,y = pos_old
                    self.grille[y][x] = -1
                print(" Coulerrrrr ")
                
    def matrice_possibilite(self, bateau,):
        # Crée une matrice vide de taille nxn pour stocker les probabilités
        resultat = np.zeros((self.taille, self.taille))
        cpt = 0  # Compte les positions où le bateau peut être placé
        # Parcourt chaque case de la grille
        for x in range(self.taille): 
            for y in range(self.taille):
                # Vérifie si le bateau peut être placé horizontalement
                if self.case_possible(bateau, (x, y), 'H'):
                    # Vérifie si le bateau peut être entièrement placé sans sortir de la grille
                    if x + bateau.taille <= self.taille:
                        for k in range(bateau.taille+1):
                            if self.grille[y][x + k] == 0:
                                resultat[y][x + k] += 1
                                cpt += 1 

                # Vérifie si le bateau peut être placé verticalement
                if self.case_possible(bateau, (x, y), 'V'):
                    # Vérifie si le bateau peut être entièrement placé sans sortir de la grille
                    if y - bateau.taille + 1 >= 0:
                        for k in range(bateau.taille+1):
                            if self.grille[y - k][x] == 0:
                                resultat[y - k][x] += 1
                                cpt += 1  

        # Si aucune position valide n'a été trouvée, éviter la division par 0
        if cpt > 0:
            return resultat /cpt
        else:
            return resultat  # Retourne la matrice sans division si cpt est nul donc la matrice null

    def matrice_possible_toucher(self,bateau,pos): # renvoie la matrice des probabilités pour un bateau donner sur la grille au allant tours d'une case 
        resultat = np.zeros((self.taille,self.taille)) # matrice de 0
        l_possible_h,l_possible_v , h_plus_grand,flag_h,flag_v = self.find_toucher_pos(bateau,pos) # liste de case ou le bateau pourrais etre 
        
        if h_plus_grand  == None: return resultat # si on trouve aucun patern donc aucun -2 sur la grille on renvoie la matrice null
        
        if h_plus_grand:
            for x,y in l_possible_h :
                for k in range(bateau.taille): # place la probabilité de chaque case d'un bateau sur la grille pour tout les position de bateau possible
                    if x+k <=9 and self.grille[y][x+k] >= 0: resultat[y][x+k]+=1 #/(len( l_possible_h))
                    
        else:        
            for x,y in l_possible_v :
                for k in range(bateau.taille): # place la probabilité de chaque case d'un bateau sur la grille pour tout les position de bateau possible
                    if y+k <=9 and self.grille[y+k][x] >= 0: resultat[y+k][x]+=1#(len(l_possible_v))
                         
        return resultat
                      
    def matrice_possible_totaux(self): 
        matrice =  np.zeros((self.taille,self.taille)) # matrice de 0
        for b in self.liste_bateau: matrice+= self.matrice_possibilite(b)
        
        return matrice /len(self.liste_bateau)
    
    def matrice_possible_toucher_all_bis(self,pos):
        matrice = np.zeros((self.taille,self.taille)) # matrice de 0
        nb_bateau=len(self.liste_bateau)
        for bateau in self.liste_bateau:
            tmp = self.matrice_possible_toucher(bateau,pos)
            matrice+= tmp # somme des matrice possible pour un bateau 
            print(tmp)
            if not np.any(matrice != 0): # check si c'est pas la matrice null dans ce cas la on ne compte pas le bateau dans la liste des bateaux
                nb_bateau -= 1
                
        return matrice / nb_bateau # on normalise
    
    def matrice_possible_toucher_all_bis(self):
            pos = self.find_toucher(self)
            if pos == (-1,-1): return self.matrice_possible_totaux() 
            else :  return matrice_possible_toucher_all_bis(pos)
            
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
        
            