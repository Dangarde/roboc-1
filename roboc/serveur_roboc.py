#!/usr/bin/python3
# -*-coding:Utf-8 -*

from random import choice
from classes.serveur import Serveur
from classes.partie import Partie
from classes.carte import Carte

print("==== Serveur Roboc ====")
partie = None
serveur = Serveur()


# Sélection de la carte
if not partie or partie.gagnee:
    carte = Carte.selectionner()
    partie = Partie(carte.nom, carte.lab)
    print("Création d'une nouvelle partie : {0}\n".format(partie.nom))
    print(partie.lab)

# Lancement du serveur roboc et attente des connexions client
serveur.demarrer()
if serveur.attendre_connexions():
    partie.en_cours = True


# Boucle principale
while partie.en_cours:

    # Calcule la position de chaque robot
    for client in serveur.clients_connectes:
        robot = choice(partie.lab.cases_libres())
        partie.lab.robots.append(list(robot))

    # Affichage de la carte sélectionnée
    serveur.envoyer_cartes(partie.lab)
    print(partie.lab)

    # Début de partie
    nb_joueurs = len(serveur.clients_connectes)
    joueur_index = -1
    rejouer = False             # Permettre de rejouer en cas de mauvais coup

    while not partie.gagnee:

        # Passe au joueur suivant et lui demande de jouer
        if not rejouer:
            joueur_index = (joueur_index + 1) % nb_joueurs
            joueur = serveur.clients_connectes[joueur_index]

        serveur.envoyer_msg(joueur, "TURN")
        print("En attente du joueur {}...".format(joueur_index + 1))

        # Notification d'attente pour les autres joueurs
        for i, client in enumerate(serveur.clients_connectes):
            if i != joueur_index:
                serveur.envoyer_msg(client, "WAIT")

        # Attend la réponse du joueur
        commande = joueur.recv(serveur.MSG_LG).decode().rstrip()
        print("Commande reçue {}...".format(commande))
        rejouer = False

        # Exécute la commande
        if commande.upper() == 'Q':
            serveur.envoyer_msg_tous("Joueur {} quitte la partie.".format(joueur_index + 1))
            partie.en_cours = False
            break
        elif commande.upper().startswith('M') or commande.upper().startswith('P'):
            if not partie.emmurer(joueur_index, commande):
                serveur.envoyer_msg(joueur,
                    "Erreur: vous ne pouvez pas effectuer cette action.")
                rejouer = True
        else:
            if not partie.deplacer_robot(joueur_index, commande):
                serveur.envoyer_msg(joueur,
                    "Erreur: vous ne pouvez pas vous déplacer dans cette direction.")
                rejouer = True

        # Affichage de la carte mise à jour
        serveur.envoyer_cartes(partie.lab)

    # La partie a été gagnée
    if partie.gagnee:
        partie.en_cours = False
        serveur.envoyer_msg_tous("Joueur {} gagne la partie!".format(joueur_index + 1))

# Arrêt du serveur
serveur.arreter()
