import unittest
import numpy as np
from Game.Bateau import Bateau
from Game.Grille import Grille

class TestGrille(unittest.TestCase):
    """Suite de tests pour la classe Grille."""

    def setUp(self):
        """Initialisation avant chaque test."""
        self.grille = Grille(taille=10)
        self.bateau1 = Bateau(taille=5, value=1, position=(-1, -1), direction='H')
        self.bateau2 = Bateau(taille=4, value=2, position=(-1, -1), direction='H')
        self.bateau3 = Bateau(taille=3, value=3, position=(-1, -1), direction='H')
        self.bateau4 = Bateau(taille=3, value=4, position=(-1, -1), direction='H')
        self.bateau5 = Bateau(taille=2, value=5, position=(-1, -1), direction='H')

    def test_initialisation_grille(self):
        """Test l'initialisation de la grille."""
        expected_grille = np.zeros((10, 10), dtype=int)
        self.assertTrue(np.array_equal(self.grille.grille, expected_grille), "La grille initialisée n'est pas correcte.")
        self.assertEqual(self.grille.taille, 10, "La taille de la grille est incorrecte.")
        self.assertEqual(len(self.grille.liste_bateau), 0, "La liste des bateaux devrait être vide à l'initialisation.")

    def test_ajout_bateau(self):
        """Test l'ajout d'un bateau sur la grille."""
        self.grille.add(self.bateau1, (0, 0), 'H')
        
        # Vérifie les positions après ajout du bateau
        expected_grille = np.zeros((10, 10), dtype=int)
        expected_grille[0, 0:5] = 1
        self.assertTrue(np.array_equal(self.grille.grille, expected_grille), "Le bateau n'a pas été ajouté correctement.")

    def test_peut_placer_bateau_valide(self):
        """Test la fonction 'peut_placer' pour un placement valide."""
        self.assertTrue(self.grille.peut_placer(self.bateau1, (0, 0), 'H'), "Le bateau devrait pouvoir être placé horizontalement.")
        self.assertTrue(self.grille.peut_placer(self.bateau1, (9, 9), 'V'), "Le bateau devrait pouvoir être placé verticalement.")

    def test_peut_placer_bateau_invalide_hors_grille(self):
        """Test la fonction 'peut_placer' pour un placement invalide (hors grille)."""
        self.assertFalse(self.grille.peut_placer(self.bateau1, (6, 0), 'H'), "Le bateau ne devrait pas pouvoir être placé horizontalement hors de la grille.")
        self.assertFalse(self.grille.peut_placer(self.bateau1, (0, 4), 'V'), "Le bateau ne devrait pas pouvoir être placé verticalement hors de la grille.")

    def test_peut_placer_bateau_chevauchement(self):
        """Test la fonction 'peut_placer' pour un chevauchement de bateaux."""
        self.grille.add(self.bateau1, (0, 0), 'H')
        self.assertFalse(self.grille.peut_placer(self.bateau2, (0, 0), 'V'), "Le bateau ne devrait pas pouvoir chevaucher un autre bateau.")
        self.assertFalse(self.grille.peut_placer(self.bateau2, (2, 0), 'V'), "Le bateau ne devrait pas pouvoir chevaucher un autre bateau.")

    def test_place_bateau_succes(self):
        """Test le placement d'un bateau sur la grille."""
        resultat = self.grille.place(self.bateau1, (0, 0), 'H')
        self.assertTrue(resultat, "Le bateau devrait être placé avec succès.")
        self.assertIn(self.bateau1, self.grille.liste_bateau, "Le bateau n'a pas été ajouté à la liste des bateaux.")
        self.assertEqual(self.bateau1.position, (0, 0), "La position du bateau n'a pas été mise à jour.")
        expected_grille = np.zeros((10, 10), dtype=int)
        expected_grille[0, 0:5] = 1
        self.assertTrue(np.array_equal(self.grille.grille, expected_grille), "Le bateau n'a pas été placé correctement dans la grille.")

    def test_place_bateau_echec(self):
        """Test le placement d'un bateau échouant à cause de contraintes."""
        self.grille.add(self.bateau1, (0, 0), 'H')
        resultat = self.grille.place(self.bateau2, (0, 0), 'V')  # Chevauchement
        self.assertFalse(resultat, "Le bateau ne devrait pas être placé en raison du chevauchement.")
        self.assertNotIn(self.bateau2, self.grille.liste_bateau, "Le bateau ne devrait pas être ajouté à la liste des bateaux.")

    def test_place_all(self):
        """Test le placement automatique de tous les bateaux."""
        self.grille.place_all()
        self.assertEqual(len(self.grille.liste_bateau), 5, "Tous les bateaux devraient être placés.")
        # Vérifier que chaque bateau est correctement placé et dans la grille
        for bateau in self.grille.liste_bateau:
            self.assertTrue(bateau.position != (-1, -1), "Le bateau devrait avoir une position valide.")
            # Vérifier que les cases de la grille sont correctement marquées
            for (x, y) in bateau.body:
                self.assertEqual(self.grille.grille[y][x], bateau.value, "La grille ne marque pas correctement les positions du bateau.")

    def test_place_alea(self):
        """Test le placement aléatoire d'un bateau."""
        resultat = False 
        while not resultat:
            resultat = self.grille.place_alea(self.bateau1)
        #while not resultat:
             #self.grille.place_alea(self.bateau1)
        self.assertTrue(resultat, "Le bateau devrait être placé avec succès de manière aléatoire.")
        self.assertIn(self.bateau1, self.grille.liste_bateau, "Le bateau n'a pas été ajouté à la liste des bateaux.")
        # Vérifier que le bateau est dans les limites de la grille
        for (x, y) in self.bateau1.body:
            self.assertGreaterEqual(x, 0)
            self.assertLess(x, self.grille.taille)
            self.assertGreaterEqual(y, 0)
            self.assertLess(y, self.grille.taille)

    def test_case_possible(self):
        """Test la fonction 'case_possible'."""
        # Position vide
        self.assertTrue(self.grille.case_possible(self.bateau1, (0, 0), 'H'), "La case devrait être possible pour le placement.")
        # Position avec chevauchement
        self.grille.add(self.bateau1, (0, 0), 'H')
        self.assertFalse(self.grille.case_possible(self.bateau2, (0, 0), 'V'), "La case ne devrait pas être possible en raison du chevauchement.")
        # Position touchée (-2)
        self.grille.grille[5, 5] = -2
        self.assertTrue(self.grille.case_possible(self.bateau3, (5, 5), 'H'), "La case devrait être possible même si elle est touchée (-2).")

    def test_find_bateau(self):
        """Test la fonction 'find'."""
        self.grille.place(self.bateau1, (0, 0), 'H')
        bat = self.grille.find((0, 0))
        self.assertEqual(bat, self.bateau1, "La fonction 'find' n'a pas trouvé le bon bateau.")
        bat = self.grille.find((9, 9))
        self.assertIsNone(bat, "La fonction 'find' devrait retourner None pour une position sans bateau.")

    def test_eq_grilles(self):
        """Test la méthode statique 'eq' pour vérifier l'égalité de deux grilles."""
        grille1 = Grille(taille=10)
        grille2 = Grille(taille=10)
        self.assertTrue(Grille.eq(grille1.grille, grille2.grille), "Deux grilles vides devraient être égales.")
        self.grille.add(self.bateau1, (0, 0), 'H')
        grille1.add(self.bateau1, (0, 0), 'H')
        self.assertTrue(Grille.eq(grille1.grille, self.grille.grille), "Les grilles devraient être égales après avoir ajouté le même bateau.")
        self.grille.add(self.bateau2, (2, 2), 'V')
        self.assertFalse(Grille.eq(grille1.grille, self.grille.grille), "Les grilles ne devraient pas être égales après avoir ajouté un bateau différent.")

    def test_grille_test(self):
        """Test la génération d'une grille de test avec des bateaux prédéfinis."""
        g = Grille.grille_test()
        # Vérifie que les bateaux sont placés aux positions prédéfinies
        self.assertIsNotNone(g.find((0, 9)), "Un bateau aurait dû être trouvé à la position (0, 9).")
        self.assertIsNotNone(g.find((1, 9)), "Un bateau aurait dû être trouvé à la position (1, 9).")
        self.assertIsNotNone(g.find((2, 9)), "Un bateau aurait dû être trouvé à la position (2, 9).")
        self.assertIsNotNone(g.find((3, 9)), "Un bateau aurait dû être trouvé à la position (3, 9).")
        self.assertIsNotNone(g.find((3, 6)), "Un bateau aurait dû être trouvé à la position (3, 6).")
        self.assertIsNone(g.find((9, 0)), "Il ne devrait pas y avoir de bateau à la position (9, 0).")

    def test_peut_etre_placer(self):
        """Test la fonction 'peut_etre_placer'."""
        # Placement valide
        self.assertTrue(self.grille.peut_etre_placer(self.bateau1, (0, 0), 'H'), "Le bateau devrait pouvoir être placé.")
        # Placement entièrement sur des cases -2
        self.grille.grille[0, 0:5] = -2
        self.assertFalse(self.grille.peut_etre_placer(self.bateau1, (0, 0), 'H'), "Le bateau ne devrait pas être placé uniquement sur des cases -2.")
        # Placement mixte
        self.grille.grille[0, 0:3] = -2
        self.grille.grille[0, 3:5] = 0
        self.assertTrue(self.grille.peut_etre_placer(self.bateau1, (0, 0), 'H'), "Le bateau devrait pouvoir être placé sur des cases mixtes.")

    def test_matrice_possibilite_solo(self):
        """Test la création de la matrice de possibilités pour un seul bateau."""
        self.grille.add(self.bateau1, (0, 0), 'H')
        matrice = self.grille.matrice_possibilite_solo(self.bateau2)
        # Vérifie que la matrice contient des valeurs non nulles
        self.assertTrue(np.any(matrice > 0), "La matrice de possibilités devrait contenir des valeurs non nulles.")
        # Vérifie que la somme des probabilités est 1
        self.assertAlmostEqual(np.sum(matrice), 1.0, places=5, msg="La somme des probabilités devrait être égale à 1.")

    def test_matrice_possible_multi(self):
        """Test la création de la matrice de possibilités pour plusieurs bateaux."""
        self.grille.place(self.bateau1, (0, 0), 'H')
        self.grille.add(self.bateau2, (2, 2), 'V')
        matrice_coups = Grille()
        matrice_coups.liste_bateau = [self.bateau1, self.bateau2, self.bateau3, self.bateau4,self.bateau5]
        matrice = matrice_coups.matrice_possible_multi()
        # Vérifie que la matrice contient des valeurs non nulles
        self.assertTrue(np.any(matrice > 0), "La matrice de possibilités multi devrait contenir des valeurs non nulles.")
        # Vérifie que la somme des probabilités est égale au nombre de bateaux
        self.assertAlmostEqual(np.sum(matrice), len(self.grille.liste_bateau), places=5, msg="La somme des probabilités devrait être égale au nombre de bateaux.")

    def test_tous_combler(self):
        """Test la fonction 'tous_combler'."""
        matrice_coups = Grille(taille=10)
        # Ajout de cases touchées (-2)
        matrice_coups.grille[0, 0] = -2
        matrice_coups.grille[1, 1] = -2
        # Grille sans couverture
        self.assertFalse(self.grille.tous_combler(matrice_coups), "Toutes les cases ne sont pas couvertes.")
        # Couvrir les cases touchées
        self.grille.add(self.bateau1, (0, 0), 'H')
        self.grille.add(self.bateau2, (1, 1), 'H')
        self.assertTrue(self.grille.tous_combler(matrice_coups), "Toutes les cases devraient être couvertes.")

    def test_monte_carlo_solo(self):
        """Test la fonction 'monte_carlo_solo'."""
        matrice_coups = Grille(taille=10)
        matrice_coups.grille[0, 0] = -2
        liste_bateaux = [self.bateau1, self.bateau2]
        grille_resultat = self.grille.monte_carlo_solo(liste_bateaux, matrice_coups, temps_max=100)
        if grille_resultat is not None:
            self.assertTrue(isinstance(grille_resultat, np.ndarray), "Le résultat devrait être une matrice numpy.")
            self.assertTrue(np.any(grille_resultat > 0), "La grille résultante devrait contenir des bateaux.")
        else:
            self.assertIsNone(grille_resultat, "Le résultat devrait être None si aucun placement n'est trouvé.")

    def test_monte_carlo_find_matrice(self):
        """Test la fonction 'monte_carlo_find_matrice'."""
        matrice_coups = Grille(taille=10)
        liste_bateaux = [self.bateau1, self.bateau2]
        matrice_coups.grille[0, 0] = -2
        resultat = self.grille.monte_carlo_find_matrice(matrice_coups, temps_max=100)
        if resultat is not None:
            self.assertTrue(isinstance(resultat, np.ndarray), "Le résultat devrait être une matrice numpy.")
            self.assertTrue(np.any(resultat > 0), "La matrice résultante devrait contenir des bateaux.")
        else:
            self.assertIsNone(resultat, "Le résultat devrait être None si aucune matrice valide n'est trouvée.")

    def test_monte_carlo_multi(self):
        """Test la fonction 'monte_carlo_multi'."""
        matrice_coups = Grille(taille=10)
        liste_bateaux = [self.bateau1, self.bateau2]
        matrice_coups.grille[0, 0] = -2
        listes_resultats = self.grille.monte_carlo_multi(matrice_coups, n=5, temps_max=100)
        self.assertIsInstance(listes_resultats, list, "Le résultat devrait être une liste de grilles.")
        for matrice in listes_resultats:
            self.assertTrue(isinstance(matrice, np.ndarray), "Chaque élément de la liste devrait être une matrice numpy.")
            self.assertTrue(np.any(matrice > 0), "Chaque matrice résultante devrait contenir des bateaux.")

    def test_monte_carlo(self):
        """Test la fonction 'monte_carlo'."""
        self.grille.place_all()
        probabilite_grille = self.grille.monte_carlo(n=100, temps_max=1000)
        self.assertTrue(isinstance(probabilite_grille, np.ndarray), "Le résultat devrait être une matrice numpy.")
        self.assertEqual(probabilite_grille.shape, (10, 10), "La matrice de probabilités devrait avoir la bonne forme.")
        self.assertTrue(np.all(probabilite_grille >= 0), "Les probabilités devraient être positives.")
        self.assertTrue(np.all(probabilite_grille <= 1), "Les probabilités ne devraient pas dépasser 1.")

    def test_genere_grille(self):
        """Test la méthode statique 'genere_grille'."""
        g = Grille.genere_grille()
        self.assertIsInstance(g, Grille, "Le résultat devrait être une instance de Grille.")
        self.assertTrue(len(g.liste_bateau) > 0, "La grille générée devrait contenir des bateaux.")
        for bateau in g.liste_bateau:
            for (x, y) in bateau.body:
                self.assertEqual(g.grille[y][x], bateau.value, "Les bateaux devraient être correctement placés dans la grille.")

    def test_peut_etre_placer_without_chevauchement(self):
        """Test 'peut_etre_placer' sans chevauchement."""
        # Placement valide
        self.assertTrue(self.grille.peut_etre_placer(self.bateau1, (5, 5), 'V'), "Le bateau devrait pouvoir être placé sans chevauchement.")
        # Placement invalide à cause d'un autre bateau
        self.bateau1.value =-1 # simule 5  essaye rater
        self.grille.add(self.bateau1, (5, 5), 'V')
        self.assertFalse(self.grille.peut_etre_placer(self.bateau2, (5, 5), 'H'), "Le bateau ne devrait pas pouvoir être placé en chevauchement.")
        self.assertTrue(self.grille.peut_etre_placer(self.bateau2, (0, 0), 'H'), "Le bateau devrait pouvoir être placé sans chevauchement.")

    #def test_affiche(self): # fonctionne retirer les # si veut etre utiliser 
        """Test la méthode 'affiche'."""
        # Cette méthode affiche la grille avec matplotlib. Nous allons simplement appeler la méthode pour vérifier qu'elle ne lève pas d'erreurs.
        #try:
        #    self.grille.affiche()
       # except Exception as e:
         #   self.fail(f"La méthode 'affiche' a levé une exception : {e}")

if __name__ == '__main__':
    unittest.main()
