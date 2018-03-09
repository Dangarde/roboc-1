# -*-coding:Utf-8 -*

class Labyrinthe:

    """ Classe représentant un labyrinthe.

    Elle se compose du schema de la
    sous forme de liste de listes (grille) et des coordonnées du
    robot.

    """

    def __init__(self, carte):
        """ Constructeur du labyrinthe.
        
        Nous construisons une grille vierge de toute position à partir de la
        chaine passée en paramètre.

        """

        self.grille = list()
        self.robots = list()

        # Construction de la carte
        for i, ligne in enumerate(carte.split("\n")):
            line = []
            for j, case in enumerate(ligne):
                line.append(case)
            if line:
                self.grille.append(line)


    def __repr__(self):
        """ Représentation du labyrinthe avec des informations de taille """

        carte = str()
        for i, ligne in enumerate(self.grille):
            for j, case in enumerate(ligne):
                carte += case
            carte += "\n"

        return "{}Hauteur:{}, Largeur:{}\n".format(
                carte, len(self.grille), len(self.grille[0]))

    def __str__(self):
        """ Représentation générique de la grille du labyrinthe """

        carte = str()
        for i, ligne in enumerate(self.grille):
            for j, case in enumerate(ligne):
                carte += case
            carte += "\n"

        return "{}".format(carte)


    def carte_individuelle(self, robot):
        """ Représentation personnalisée du labyrinthe.

        Renvoie une représentation du labyrinthe avec un robot principal (X)
        accompagné des autres robots (x).

        """

        carte = str()
        for i, ligne in enumerate(self.grille):
            for j, case in enumerate(ligne):
                if [i, j] == self.robots[robot]:
                    carte += "X"
                elif [i, j] in self.robots:
                    carte += "x"
                else:
                    carte += case
            carte += "\n"

        return "\n{}".format(carte)


    def cases_libres(self):
        """ Renvoie la liste des cases libres du labyrinthe

        Cette méthode est utilisée pour déterminer les positions
        initiales des robots
        
        """

        cases = []
        for i, ligne in enumerate(self.grille):
            for j, case in enumerate(ligne):
                if case == ' ':
                    cases.append((i,j))

        return cases
