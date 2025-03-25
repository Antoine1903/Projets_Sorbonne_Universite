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
import matplotlib.pyplot as plt

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

def main(nb_jours):
    iterations = 40  # nb de pas max par episode
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print("Iterations: ")
    print(iterations)

    init('restaurant-map')

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
    # Rapport de ce qui est trouvé sur la carte
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

    def champ_de_vision(position_joueur, distance_vision, players, coupe_files):
        """
        :param position_joueur: position actuelle du joueur
        :param distance_vision: distance de vision du joueur
        :param players: liste des joueurs
        :param coupe_files: liste des coupe-files
        :return: liste des positions visibles par le joueur (joueurs et coupe-files)
        """
        visible_positions = []
        for player in players:
            if player.get_rowcol() != position_joueur:
                if np.linalg.norm(np.array(position_joueur) - np.array(player.get_rowcol())) <= distance_vision:
                    visible_positions.append(player.get_rowcol())
        for cf in coupe_files:
            if np.linalg.norm(np.array(position_joueur) - np.array(cf.get_rowcol())) <= distance_vision:
                visible_positions.append(cf.get_rowcol())
        return visible_positions

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
    strategy_names = []  # 新增：记录策略名称
    choix_initiaux = {}  
    visited_restaurants = [set() for _ in range(nb_players)]  
    distance_vision = 5
    temps_restant = [iterations] * nb_players  
    seuils = [float('inf')] * nb_players  
    historique = {}  
    payoffs = {}  

    for i in range(nb_players):
        print(f"Choisissez la stratégie pour le joueur {i+1}:")
        print("1. Stratégie têtue")
        print("2. Stratégie stochastique")
        print("3. Stratégie greedy")
        print("4. Fictitious Play")
        print("5. Regret Matching")
        choice = int(input("Entrez le numéro de la stratégie : "))

        if choice == 1:
            strategies.append(lambda p=i: strategie_tetue(pos_restaurants, p, choix_initiaux))
            strategy_names.append("Têtue")  # 记录策略名称
        elif choice == 2:
            probabilites = [1/nb_restos] * nb_restos  
            strategies.append(lambda p=probabilites: strategie_stochastique(pos_restaurants, p))
            strategy_names.append("Stochastique")
        elif choice == 3:
            seuil = int(input(f"Entrez le seuil pour greedy (joueur {i+1}) : "))
            seuils[i] = seuil  
            strategies.append(lambda p=i: strategie_greedy(
                pos_restaurants,
                nb_players_in_resto,
                seuils[p],
                players[p].get_rowcol(),
                champ_de_vision(players[p].get_rowcol(), distance_vision, players, coupe_files),
                temps_restant[p], 
                p,
                nb_players  
            ))
            strategy_names.append("Greedy")
        elif choice == 4:
            strategies.append(lambda p=i: fictitious_play(pos_restaurants, historique, p))
            strategy_names.append("Fictitious Play")
        elif choice == 5:
            strategies.append(lambda p=i: regret_matching(pos_restaurants, historique, p, payoffs))
            strategy_names.append("Regret Matching")
        else:
            print("Stratégie aléatoire par défaut.")
            strategies.append(lambda: random.choice(pos_restaurants))
            strategy_names.append("Aléatoire")

    # -------------------------------
    # Boucle principale sur les jours
    # -------------------------------

    total_scores = [0] * nb_players
    initial_coupe_files = [o for o in game.layers["ramassable"]]  # Sauvegarder les objets "coupe-file" initiaux
    for day in range(nb_jours):
        print(f"\nJour {day+1}:")
        # Réinitialiser le temps restant pour chaque joueur
        temps_restant = [iterations] * nb_players

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
            prob = ProblemeGrid2D(players[p].get_rowcol(), choix_resto[p], g, 'manhattan')
            path.append(probleme.astar(prob, verbose=False))

        # Réinitialiser les coupe-files ramassés
        player_coupe_file = [False] * nb_players

        # Boucle principale de déplacements
        for i in range(iterations):
            print(f"\n--- ITERATION {i+1}/{iterations} ---")

            for j in range(nb_players):
                if i < len(path[j]):
                    (row, col) = path[j][i]
                    players[j].set_rowcol(row, col)

                    # Affichage des informations du joueur
                    print(f"Joueur {j} | Position: ({row}, {col}) | Temps restant: {temps_restant[j]} | Destination: {choix_resto[j]}")

                    # Vérification du temps restant
                    if temps_restant[j] <= 0:
                        print(f"⚠️ ALERTE: Le temps du joueur {j} est écoulé !")

                    # Vérifier si le joueur est arrivé à un restaurant
                    if (row, col) in pos_restaurants:
                        r = pos_restaurants.index((row, col))
                        print(f"🍽️ Joueur {j} est arrivé au restaurant {r}")

                        # Vérifier que le joueur utilise la stratégie_greedy et que le seuil est dépassé
                        if strategies[j].__name__ == "strategie_greedy" and seuils[j] is not None:
                            if nb_players_in_resto(r) >= seuils[j]:
                                print(f"⚠️ Trop de joueurs dans le restaurant {r}. Recherche d'un autre restaurant...")

                                # Choisir un autre restaurant
                                new_target = strategie_greedy(
                                    pos_restaurants,
                                    nb_players_in_resto,
                                    seuils[j],
                                    players[j].get_rowcol(),
                                    champ_de_vision(players[j].get_rowcol(), distance_vision, players, coupe_files),
                                    temps_restant[j],
                                    j,
                                    nb_players
                                )

                                if new_target and new_target != choix_resto[j]:  # Si un nouveau choix est fait
                                    print(f"🔄 Joueur {j} change de restaurant: {choix_resto[j]} ➝ {new_target}")
                                    choix_resto[j] = new_target
                                    prob = ProblemeGrid2D(players[j].get_rowcol(), choix_resto[j], g, 'manhattan')
                                    path[j] = probleme.astar(prob, verbose=False)  # Recalcule le chemin

                                # Déplacer le joueur sur le chemin mis à jour
                                if i < len(path[j]):
                                    (row, col) = path[j][i]
                                    players[j].set_rowcol(row, col)

                # Vérifier si le joueur ramasse un "Coupe-file"
                for cf in coupe_files:
                    if (row, col) == cf.get_rowcol() and not player_coupe_file[j]:
                        player_coupe_file[j] = True
                        game.layers["ramassable"].remove(cf)
                        coupe_files.remove(cf)
                        print(f"🎟️ Joueur {j} a ramassé un Coupe-file!")
                        break

            # Mettre à jour le temps restant pour chaque joueur
            for j in range(nb_players):
                temps_restant[j] -= 1
                if temps_restant[j] < 0:
                    print(f"⏳ Joueur {j} n'a plus de temps restant !")

            game.mainiteration()
            print("-" * 40)  # Séparation entre les itérations

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

        # Mettre à jour l'historique et les gains pour les stratégies Fictitious Play et Regret Matching
        for p in range(nb_players):
            historique.setdefault(p, {}).setdefault(choix_resto[p], 0)
            historique[p][choix_resto[p]] += 1

            payoffs.setdefault(p, {}).setdefault(choix_resto[p], 0)
            payoffs[p][choix_resto[p]] += scores[p]

    print("Scores totaux après 5 jours :", total_scores)
    # 生成比较图表（修改后的统计逻辑）
    strategy_total = {}  # 记录策略总分
    strategy_count = {}  # 记录使用人数
    
    # 遍历所有玩家统计数据
    for p in range(nb_players):
        strategy = strategy_names[p]
        if strategy not in strategy_total:
            strategy_total[strategy] = 0
            strategy_count[strategy] = 0
        strategy_total[strategy] += total_scores[p]
        strategy_count[strategy] += 1
    
    # 计算平均分数（处理除零错误）
    average_scores = {}
    for strategy in strategy_total:
        if strategy_count[strategy] > 0:
            average_scores[strategy] = strategy_total[strategy] / strategy_count[strategy]
        else:
            average_scores[strategy] = 0
    
    # 准备可视化数据
    labels = []
    values = []
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    color_idx = 0
    
    # 按策略名称排序保证颜色一致性
    for strategy in sorted(average_scores.keys()):
        labels.append(f"{strategy}\n(n={strategy_count[strategy]})")  # 显示使用人数
        values.append(average_scores[strategy])
        color_idx += 1
    
    # 创建图表
    plt.figure(figsize=(12, 7))
    bars = plt.bar(labels, values, color=colors[:len(labels)])
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom')
    
    # 图表装饰
    plt.xlabel('Stratégies (avec nombre de joueurs)')
    plt.ylabel('Score Moyen par Joueur')
    plt.title(f'Performance Comparative des Stratégies sur {nb_jours} Jours (Moyenne par Joueur)')
    plt.xticks(rotation=15)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # 保存并显示
    plt.savefig('strategy_comparison.png', dpi=300)
    plt.show()
    pygame.quit()

if __name__ == '__main__':
    main(nb_jours=50)
