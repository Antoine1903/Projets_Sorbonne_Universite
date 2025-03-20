# -*- coding: utf-8 -*-

# Zhang Yuxiang & Lecomte Antoine

from __future__ import absolute_import, print_function, unicode_literals

import random
import numpy as np
import sys
from itertools import chain

import pygame

from pySpriteWorld.gameclass import Game, check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme

from strategies import *

# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player, game
    name = _boardname if _boardname is not None else 'restaurant-map2'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player

def champ_vision(position, taille_vision, nb_lignes, nb_cols):
    x, y = position
    vision = []
    for i in range(-taille_vision, taille_vision + 1):
        for j in range(-taille_vision, taille_vision + 1):
            new_x, new_y = x + i, y + j
            if 0 <= new_x < nb_lignes and 0 <= new_y < nb_cols:
                vision.append((new_x, new_y))
    return vision

def main(nb_jours):
    iterations = 40  # nb de pas max par episode
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print("Iterations: ")
    print(iterations)

    init()

    # -------------------------------
    # Initialisation
    # -------------------------------

    nb_lignes = game.spriteBuilder.rowsize
    nb_cols = game.spriteBuilder.colsize
    assert nb_lignes == nb_cols  # a priori on souhaite un plateau carre
    lMin = 2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les objets)
    lMax = nb_lignes - 2
    cMin = 2
    cMax = nb_cols - 2

    players = [o for o in game.layers['joueur']]
    nb_players = len(players)

    pos_restaurants = [(3, 4), (3, 7), (3, 10), (3, 13), (3, 16)]  # 5 restaurants positionnes
    nb_restos = len(pos_restaurants)
    capacity = [1] * nb_restos

    coupe_files = [o for o in game.layers["ramassable"]]  # a utiliser dans le cas de la variante coupe-file
    nb_coupe_files = len(coupe_files)

    # -------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets ou de joueurs
    # -------------------------------

    def item_states(items):
        # donne la liste des coordonnees des items
        return [o.get_rowcol() for o in items]

    def player_states(players):
        # donne la liste des coordonnees des joueurs
        return [p.get_rowcol() for p in players]

    # -------------------------------
    # Rapport de ce qui est trouve sut la carte
    # -------------------------------
    print("lecture carte")
    print("-------------------------------------------")
    print('joueurs:', nb_players)
    print("restaurants:", nb_restos)
    print("lignes:", nb_lignes)
    print("colonnes:", nb_cols)
    print("coup_files:", nb_coupe_files)
    print("-------------------------------------------")

    # -------------------------------
    # Carte demo
    # 8 joueurs
    # 5 restos
    # -------------------------------

    # -------------------------------

    # -------------------------------
    # Fonctions definissant les positions legales et placement aléatoire
    # -------------------------------

    def legal_position(pos):
        row, col = pos
        # une position legale est dans la carte et pas sur un objet deja pose ni sur un joueur ni sur un resto
        return ((pos not in item_states(coupe_files)) and (pos not in player_states(players)) and (
                    pos not in pos_restaurants) and row > lMin and row < lMax - 1 and col >= cMin and col < cMax)

    def draw_random_location():
        # tire au hasard un couple de positions permettant de placer un item
        while True:
            random_loc = (random.randint(lMin, lMax), random.randint(cMin, cMax))
            if legal_position(random_loc):
                return random_loc

    def players_in_resto(r):
        """
        :param r: id of the resto
        :return: id of players in resto
        """
        are_here = []
        pos = pos_restaurants[r]
        for i in range(0, nb_players):
            if players[i].get_rowcol() == pos:
                are_here.append(i)
        return are_here

    def nb_players_in_resto(r):
        """
        :param r: id of resto
        :return: int number of players currently here
        """
        return len(players_in_resto(r))

    # -------------------------------
    # On place tous les coupe_files du bord au hasard
    # -------------------------------

    for o in coupe_files:
        (x1, y1) = draw_random_location()
        o.set_rowcol(x1, y1)
        game.mainiteration()

    # -------------------------------
    # On place tous les joueurs au hasard sur la ligne du bas
    # -------------------------------

    y_init = [3, 5, 7, 9, 11, 13, 15, 17]
    x_init = 18
    random.shuffle(y_init)
    for i in range(0, nb_players):
        players[i].set_rowcol(x_init, y_init[i])
        game.mainiteration()

    # -------------------------------
    # Menu de sélection des stratégies
    # -------------------------------

    strategies = []
    choix_initiaux = {}  # Dictionnaire pour stocker les choix initiaux des joueurs
    visited_restaurants = [set() for _ in range(nb_players)]  # Liste des restaurants visités par chaque joueur
    seuils = []  # Seuil individuel pour chaque joueur
    for i in range(nb_players):
        print(f"Choisissez la stratégie pour le joueur {i+1}:")
        print("1. Stratégie têtue")
        print("2. Stratégie stochastique")
        print("3. Stratégie greedy")
        choice = int(input("Entrez le numéro de la stratégie : "))
        if choice == 1:
            strategies.append(lambda p=i: strategie_tetue(pos_restaurants, p, choix_initiaux))
        elif choice == 2:
            probabilites = [1/nb_restos] * nb_restos  # Distribution uniforme par défaut
            strategies.append(lambda p=probabilites: strategie_stochastique(pos_restaurants, p))
        elif choice == 3:
            seuil = int(input(f"Entrez le seuil d'occupation pour la stratégie greedy (joueur {i+1}) : "))
            seuils.append(seuil)
            strategies.append(lambda p=i: strategie_greedy(pos_restaurants, nb_players_in_resto, seuils[p], players[p].get_rowcol(), visited_restaurants[p], iterations, i))
        else:
            print("Choix invalide. Stratégie aléatoire par défaut.")
            strategies.append(lambda: random.choice(pos_restaurants))

    # -------------------------------
    # Boucle principale sur les jours
    # -------------------------------

    total_scores = [0] * nb_players
    initial_coupe_files = [o for o in game.layers["ramassable"]]  # Sauvegarder les objets "coupe-file" initiaux
    for day in range(nb_jours):
        print(f"\nJour {day+1}:")

        # Réinitialiser les positions des joueurs et des coupe-files
        coupe_files = initial_coupe_files.copy()
        for o in coupe_files:
            (x1, y1) = draw_random_location()
            o.set_rowcol(x1, y1)
            game.layers["ramassable"].add(o)
            game.mainiteration()

        random.shuffle(y_init)
        for i in range(nb_players):
            players[i].set_rowcol(x_init, y_init[i])
            game.mainiteration()

        # Réinitialiser les choix de restaurants et les chemins
        choix_resto = [strategy() for strategy in strategies]
        path = []
        g = np.ones((nb_lignes, nb_cols), dtype=bool)
        for i in range(nb_lignes):
            g[0][i] = False
            g[1][i] = False
            g[nb_lignes - 1][i] = False
            g[nb_lignes - 2][i] = False
            g[i][0] = False
            g[i][1] = False
            g[i][nb_lignes - 1] = False
            g[i][nb_lignes - 2] = False

        for p in range(nb_players):
            pos_player = (x_init, y_init[p])
            prob = ProblemeGrid2D(pos_player, choix_resto[p], g, 'manhattan')
            path.append(probleme.astar(prob, verbose=False))

        # Réinitialiser les coupe-files ramassés
        player_coupe_file = [False] * nb_players

        # Boucle principale de déplacements
        for i in range(iterations):
            for j in range(nb_players):
                if i < len(path[j]):
                    (row, col) = path[j][i]
                    players[j].set_rowcol(row, col)

                    # Vérifier si le joueur est arrivé à un restaurant
                    if (row, col) in pos_restaurants:
                        r = pos_restaurants.index((row, col))
                        if nb_players_in_resto(r) - 1 >= seuils[j]:
                            # Choisir un autre restaurant aléatoire
                            new_target = strategie_greedy(pos_restaurants, nb_players_in_resto, seuils[j], players[j].get_rowcol(), visited_restaurants[j], iterations, i)
                            pos_player = (row, col)
                            prob = ProblemeGrid2D(pos_player, new_target, g, 'manhattan')
                            path[j] = probleme.astar(prob, verbose=False)

                for cf in coupe_files:
                    if (row, col) == cf.get_rowcol() and not player_coupe_file[j]:
                        player_coupe_file[j] = True
                        game.layers["ramassable"].remove(cf)
                        coupe_files.remove(cf)
                        print(f"Joueur {j} a ramassé le Coupe-file!")
                        break

            game.mainiteration()

        # Calcul des scores quotidiens
        attendance = [0] * nb_restos
        for r in range(nb_restos):
            attendance[r] = nb_players_in_resto(r)

        scores = [0] * nb_players
        for r in range(nb_restos):
            players_here = players_in_resto(r)
            with_coupe_file = [p for p in players_here if player_coupe_file[p]]
            without_coupe_file = [p for p in players_here if not player_coupe_file[p]]
            random.shuffle(with_coupe_file)
            random.shuffle(without_coupe_file)
            served_players = with_coupe_file[:capacity[r]]
            remaining_slots = max(0, capacity[r] - len(served_players))
            served_players += without_coupe_file[:remaining_slots]
            for p in served_players:
                scores[p] += 1

        print("Scores quotidiens :", scores)
        for p in range(nb_players):
            total_scores[p] += scores[p]

    print("Scores totaux après 5 jours :", total_scores)
    pygame.quit()

if __name__ == '__main__':
    main(nb_jours=5)