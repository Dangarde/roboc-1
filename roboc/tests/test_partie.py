# -*-coding:Utf-8 -*

import unittest
from classes.partie import Partie
from classes.labyrinthe import Labyrinthe

class PartieTest(unittest.TestCase):

    """ Test cases utilisés pour tester les fonctions du module partie """

    def setUp(self):
        """ Initialisation des tests.

        Nous lisons une des cartes pour initialiser le labyrinthe de test.
        Puis nous nous en servons pour effectuer les tests sur l'objet partie.

        """

        with open('tests/carte_test.txt', 'r') as fichier_carte:
            self.carte = fichier_carte.read()

        # Initialisation de la partie et du labyrinthe
        self.lab = Labyrinthe(self.carte)
        self.partie = Partie("test", self.lab)

        # Création du robot 0 à la position [1, 1]
        self.lab.robots.append([1, 1])


    def test_lab_contenu(self):
        """ Test la conversion de la carte """

        # La grille du labyrinthe correspond au contenu du fichier
        self.assertEqual(str(self.lab), self.carte)


    def test_deplacement(self):
        """ Test le déplacement du robot """

        # Renvoie du robot 0 à la position [1, 1]
        self.lab.robots[0] = [1, 1]

        # Déplacement vers le sud
        self.partie.deplacer_robot(0, "s3")

        # Le robot doit se trouver en position [4, 1]        
        self.assertEqual(self.lab.robots[0], [4, 1])


    def test_emmurer(self):
        """ Test la modification d'un mur """

        # Renvoie du robot 0 à la position [1, 1]
        self.lab.robots[0] = [1, 1]

        # Création d'une porte à l'est
        self.partie.emmurer(0, "pe")

        # La position [1][2] doit être une porte
        self.assertEqual(self.lab.grille[1][2], '.')


    def test_deplacement_fail(self):
        """ Test l'impossibilité de déplacement du robot (contre un mur) """

        # Renvoie du robot 0 à la position [1, 1]
        self.lab.robots[0] = [1, 1]

        # Déplacement vers le nord
        self.partie.deplacer_robot(0, "n3")

        # Le robot doit ne doit pas avoir bougé        
        self.assertEqual(self.lab.robots[0], [1, 1])


    def test_emmurer_fail(self):
        """ Test l'impossibilité de modification d'un mur (bordure lab) """

        # Renvoie du robot 0 à la position [1, 1]
        self.lab.robots[0] = [1, 1]

        # Vérification du contenu de la position à modifier
        self.assertEqual(self.lab.grille[0][1], 'O')

        # Création d'une porte au nord
        self.partie.emmurer(0, "pn")

        # La position [0][1] ne doit pas avoir changé
        self.assertEqual(self.lab.grille[0][1], 'O')


if __name__ == '__main__':
    unittest.main()
