class Bateau:
    """
    Classe représentant un bateau. Sert a facilité les operation sur la taille des bateau choisis etc.
    
    Attributs:
    ----------
    taille : int
        La taille du bateau, c'est-à-dire le nombre de cases qu'il occupe.
    value : int
        La valeur du bateau, utilisée pour le scoring ou d'autres logiques de jeu.
    position : tuple, optionnel
        La position de la tête du bateau sur la grille (x, y). Par défaut, (-1, -1).
    direction : str, optionnel
        La direction du bateau, 'H' pour horizontal et 'V' pour vertical. Par défaut, 'H'.
    body : list
        Liste pour représenter le bateau et les cases touchées. Initialement vide.
    pdv : int
        Points de vie du bateau, qui représente le nombre de fois que le bateau peut être touché. 
        Il est initialisé à la taille du bateau.
    
    Méthodes:
    ---------
    set_direction(direction):
        Définit la direction du bateau.
    
    est_vivant():
        Renvoie True si le bateau est encore en vie (non touché le nombre de fois correspondant à sa taille), sinon False.
    """
    
    def __init__(self, taille, value, position=(-1, -1), direction='H'):
        self.value = value  # valeur indiquée dans le PDF
        self.taille = taille
        self.position = position  # position de la tête du bateau
        self.direction = direction  # 'H' ou 'V'
        self.body = []  # permet de visualiser le bateau et les cases touchées
        self.pdv = taille  # le nombre de fois que l'on peut le toucher

    def set_direction(self, direction):
        """Définit la direction du bateau."""
        self.direction = direction

    def est_vivant(self):
        """
        Renvoie si le bateau est encore en vie, donc a été touché moins de taille fois.
        
        Returns:
            bool: True si le bateau est vivant, sinon False.
        """
        return self.pdv > 0

        