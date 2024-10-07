import unittest
from Game.Bateau import Bateau

class TestBateau(unittest.TestCase):

    def setUp(self):
        """Crée une instance de Bateau pour les tests."""
        self.bateau = Bateau(taille=3, value=10)

    def test_initialisation(self):
        """Teste l'initialisation de la classe Bateau."""
        self.assertEqual(self.bateau.taille, 3)
        self.assertEqual(self.bateau.value, 10)
        self.assertEqual(self.bateau.position, (-1, -1))
        self.assertEqual(self.bateau.direction, 'H')
        self.assertEqual(self.bateau.pdv, 3)
        self.assertEqual(self.bateau.body, [])

    def test_set_direction(self):
        """Teste la méthode set_direction."""
        self.bateau.set_direction('V')
        self.assertEqual(self.bateau.direction, 'V')
        
        self.bateau.set_direction('H')
        self.assertEqual(self.bateau.direction, 'H')

    def test_est_vivant(self):
        """Teste la méthode est_vivant."""
        self.assertTrue(self.bateau.est_vivant())
        
        # Simule un touché
        self.bateau.pdv -= 1
        self.assertTrue(self.bateau.est_vivant())
        
        # Simule un autre touché
        self.bateau.pdv -= 2
        self.assertFalse(self.bateau.est_vivant())

if __name__ == '__main__':
    unittest.main()
