# -*-coding:Utf-8 -*

import os
import pickle
import re
from classes.labyrinthe import Labyrinthe

class Partie:

    """Controlleur de partie.

    Il nous permet de controller le robot et de sauvegarder l'état de la partie.

    """

    obstacles = ['O']               # Liste des obstacles
    sortie = 'U'                    # Sortie du labyrinthe

    def __init__(self, nom, labyrinthe):
        self.nom = nom
        self.lab = labyrinthe
        self.en_cours = False
        self.gagnee = False

    @classmethod
    def charger(self, nom_fichier):
        """Chargement de la partie sauvegardée."""
        with open(nom_fichier, "rb") as ficher_sauvegarde:
            unpickler = pickle.Unpickler(ficher_sauvegarde)
            partie = unpickler.load()
        return partie


    def sauvegarder(self, nom_fichier):
        """Sauvegarde la partie en cours."""
        with open(nom_fichier, "wb") as ficher_sauvegarde:
            pickler = pickle.Pickler(ficher_sauvegarde)
            pickler.dump(self)


    def supprimer(self, nom_fichier):
        """Supprime le fichier de sauvegarde """
        if os.path.exists("sauvegarde"):
            os.remove("sauvegarde")


    def deplacer_robot(self, robot, commande):
        """ Déplacement du robot du joueur.

        Modifie les coordonnées du robot après avoir vérifié l'absence
        d'obstacles et renvoie True si tel est le cas. 
        Met fin à la partie si le robot atteint la sortie.
        
        """
        mouvement = 0                   # Nombre de cases parcourues

        # Détection d'une distance éventuelle
        try:
            distance = int(commande[1:])
        except:
            distance = 1

        # Pour chaque unité de mouvement
        while distance != 0:

            # Conversion numérique de la direction saisie
            if commande[0].upper() == 'N':
                direction = (-1, 0)
            elif commande[0].upper() == 'E':
                direction = (0, 1)
            elif commande[0].upper() == 'S':
                direction = (1, 0)
            elif commande[0].upper() == 'O':
                direction = (0, -1)
            else:
                break

            # Calcul de la nouvelle position
            pos = [self.lab.robots[robot][0] + direction[0],
                   self.lab.robots[robot][1] + direction[1]]

            # On verifie que la position ne rencontre pas d'obstacle.
            if self.lab.grille[pos[0]][pos[1]] in Partie.obstacles:
                break

            # Assignation de la nouvelle position
            self.lab.robots[robot] = pos
            distance-=1
            mouvement+=1

            # La sortie a été atteinte.
            if self.lab.grille[pos[0]][pos[1]] == Partie.sortie:
                # Fin du jeu
                self.gagnee = True
                break

        if mouvement == 0:
            return False
        else:
            return True


    def emmurer(self, robot, commande):
        """ Emmurer un autre joueur.
        
        Transforme une porte en mur ou un mur en porte en vérifiant
        que le mur est à proximité du joueur et qu'il ne s'agit pas
        d'un des bords du labyrinthe.
        
        """

        # Conversion numérique de la direction saisie
        if commande[1].upper() == 'N':
            direction = (-1, 0)
        elif commande[1].upper() == 'E':
            direction = (0, 1)
        elif commande[1].upper() == 'S':
            direction = (1, 0)
        elif commande[1].upper() == 'O':
            direction = (0, -1)
        else:
            return False

        # Calcul la position relative à modifier
        pos = [self.lab.robots[robot][0] + direction[0],
               self.lab.robots[robot][1] + direction[1]]

        # S'il ne s'agit pas d'un bord du labyrinthe
        if (pos[0] < len(self.lab.grille ) - 1 and
            pos[1] < len(self.lab.grille[0]) - 1 and 
            pos[0] > 0 and pos[1] > 0):

            if (commande[0].upper() == 'M' and 
                self.lab.grille[pos[0]][pos[1]] == '.'):

                # Il s'agit d'une porte qu'on peut emmurer
                self.lab.grille[pos[0]][pos[1]] = 'O'

            elif (commande[0].upper() == 'P' and 
                  self.lab.grille[pos[0]][pos[1]] == 'O'):

                # Il s'agit d'un mur qu'on peut détruire
                self.lab.grille[pos[0]][pos[1]] = '.'
          
            else:
                return False
        else:
            return False

        return True

