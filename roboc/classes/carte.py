# -*-coding:Utf-8 -*

import os
from classes.labyrinthe import Labyrinthe

class Carte:
    """Objet de transition entre un fichier et un labyrinthe. 
    
    Cet objet nous permet notamment de sélectionner une carte parmis celles 
    disponibles et instancie le labyrinthe correspondant.

    """

    def __init__(self, nom, chaine):
        self.nom = nom
        self.lab = Labyrinthe(chaine)

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

    @staticmethod
    def selectionner():
        """ Affichage du menu de sélection.

        Lance le menu de sélection de carte et renvoie la carte sélectionnée.

        """

        cartes = []

        # On charge les cartes existantes
        for nom_fichier in os.listdir("cartes"):

            if nom_fichier.endswith(".txt"):
                chemin = os.path.join("cartes", nom_fichier)
                nom_carte = nom_fichier[:-3].lower()
                with open(chemin, "r") as fichier:
                    contenu = fichier.read()
                    # Création d'une carte
                    carte = Carte(nom_carte, contenu)
            cartes.append(carte)

        # Affichage des cartes existantes
        print("Labyrinthes existants :")
        for i, carte in enumerate(cartes):
            print("  {} - {}".format(i + 1, carte.nom))

        # Demande de sélection de carte
        num_carte = 0
        while num_carte < 1 or num_carte > len(cartes):
            num_carte = input("\nEntrez un numéro de labyrinthe " 
                              "pour commencer à jouer : ")
            try:
                num_carte = int(num_carte)
            except ValueError:
                print("Vous n'avez pas saisi de nombre.")
                num_carte = 0
                continue
            if num_carte < 1 or num_carte > len(cartes):
                print("La carte selectionnée n'existe pas.")

        return cartes[num_carte - 1]

