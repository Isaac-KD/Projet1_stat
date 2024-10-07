import unittest
from Game.Grille import Grille
from Game.Bataille import Bataille

class TestBataille(unittest.TestCase):

    def setUp(self):
        """
        Prépare un environnement de test pour chaque méthode de test.
        Initialise une instance de la classe Bataille et configure une grille.
        """
        self.bataille = Bataille()

    def test_initialisation(self):
        """
        Teste l'initialisation de la classe Bataille.
        Vérifie que la grille et la matrice de coups sont correctement initialisées.
        """
        self.assertIsInstance(self.bataille.grille, Grille)
        self.assertIsInstance(self.bataille.matrice_coup, Grille)
        self.assertEqual(len(self.bataille.grille.liste_bateau), len(self.bataille.matrice_coup.liste_bateau))

    def test_joue_touché(self):
        """
        Teste le comportement de la méthode joue lorsque le coup touche un bateau.
        """
        # Supposez que la position (0, 0) touche un bateau.
        position = (0, 0)
        self.bataille.grille.grille[0][0] = 0  # Simule le vide
        self.bataille.matrice_coup.grille[0][0] = 0  # Simule un coup non joué
        result = self.bataille.joue(position)
        self.assertFalse(result)
        self.assertEqual(self.bataille.matrice_coup.grille[0][0], -1)  # Marqué comme manquer

    def test_joue_manqué(self):
        """
        Teste le comportement de la méthode joue lorsque le coup ne touche pas un bateau.
        """
        position = (0, 0)
        self.bataille.grille.grille[0][0] = 0  # Simule pas de bateau à cette position

        result = self.bataille.joue(position)
        self.assertFalse(result)
        self.assertEqual(self.bataille.matrice_coup.grille[0][0], -1)  # Marqué comme manqué

    def test_victoire(self):
        """
        Teste la méthode victoire pour vérifier si tous les bateaux ont été coulés.
        """
        # Ajoute un bateau vivant
        for bat in self.bataille.grille.liste_bateau:
            bat.pdv= 0
        # Vérifie que la victoire est atteinte
        self.assertTrue(self.bataille.victoire())

    def test_reset(self):
        """
        Teste la méthode reset pour vérifier qu'une nouvelle grille est générée.
        """
        initial_grille = self.bataille.grille
        self.bataille.reset()
        self.assertIsNot(initial_grille, self.bataille.grille)  # Doit être une nouvelle instance

    def test_case_conexe_possible(self):
        """
        Teste la méthode case_conexe_possible pour vérifier les cases adjacentes jouables.
        """
        position = (1, 1)
        self.bataille.grille.grille[1][1] = 0  # Position de référence
        self.bataille.matrice_coup.grille[1][1] = 0  # Marquer comme non jouée
        
        result = self.bataille.case_conexe_possible(position)
        expected = [(0, 1), (1, 0), (2, 1),(1,2)]  # Cases possibles

        self.assertCountEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
