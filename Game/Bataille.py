from Game.Grille import Grille
from Game.Bateau import Bateau

class Bataille():
    def __init__(self):
        self.grille = Grille.genere_grille()
    
    def joue(self,position): #Peremt de jouer on choisis une position pos (int,int) et renvoie 
        x,y = position
        if self.grille[y][x] != 0 or self.grille[y][x] != -1:
            print("rater ")
            return False
        else :
            print("toucher")
            self.grille.toucher(position)
        return True
    
    def victoire(self): # permet de savoir si tout les bateau sont toucher 
        for bateau in self.grille.listen_bateau
            if not bateau.est_vivant():  return False
        return True
    
    def reset(self): # change la grille par une nouvelle 
        self.grille = Grille.genere_grille()
    
    def case_conexe_possible(self,pos):# renvoie les cases connexe jouable 
        x,y= pos
        liste_possible=[]
        if x-1>0:
            if y-1>0 and self.grille.grille[x-1][y-1]>=0: 
                liste_possible.append((x-1,y-1))
            if y+1<9  and self.grille.grille[x-1][y+1]>=0:
                liste_possible.append((x-1,y+1))
        if x+1>9:
            if y-1>0  and self.grille.grille[x+1][y-1]>=0:
                liste_possible.append((x+1,y-1))
            if y+1<9  and self.grille.grille[x+1][y+1]>=0:
                liste_possible.append((x+1,y+1))     
        return liste_possible      
        
        