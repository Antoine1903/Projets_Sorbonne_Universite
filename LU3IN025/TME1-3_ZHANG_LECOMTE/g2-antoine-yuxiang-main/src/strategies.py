import random
from search.grid2D import *

def strategie_tetue(pos_restaurants, joueur_id, choix_initiaux):
    """Stratégie têtue : le joueur va toujours au même restaurant qu'il a choisi au premier jour."""
    if joueur_id not in choix_initiaux:
        # Si c'est le premier jour, choisir un restaurant au hasard
        choix_initiaux[joueur_id] = random.choice(pos_restaurants)
    return choix_initiaux[joueur_id]

def strategie_stochastique(pos_restaurants, probabilites):
    """Stratégie stochastique : le joueur choisit un restaurant selon une distribution de probabilité."""
    return random.choices(pos_restaurants, weights=probabilites, k=1)[0]

def strategie_greedy(pos_restaurants, nb_players_in_resto, seuil, position_joueur, champ_de_vision_func, distance_vision, temps_restant, joueur_id, preferences, players, coupe_files):
    """
    - Les joueurs ont une liste de restaurants à visiter basée sur la distance (le plus éloigné en priorité).
    - Lorsqu'un joueur entre dans un restaurant, ceux qui le voient parmi les greedy recalculent leur décision.
    - Si le seuil de joueurs dans le restaurant actuel est atteint, le joueur cherche à se rendre dans son prochain restaurant de sa liste.
    - Une fois tous les restaurants essayés, s'ils dépassent tous le seuil, le joueur se dirige vers le restaurant avec le moins de joueurs s'il lui reste suffisamment de temps.
    - S'il n'a pas le temps, chercher celui avec le moins de joueurs qu'il est possible d'atteindre avec le temps qu'il lui reste.
    """
    # Trier les restaurants par distance décroissante par rapport à la position initiale
    restaurants_tries = sorted(pos_restaurants, key=lambda r: distManhattan(position_joueur, r), reverse=True)

    # Filtrer les restaurants accessibles dans le temps restant et respectant le seuil
    restaurants_accessibles = [
        resto for resto in restaurants_tries
        if distManhattan(position_joueur, resto) <= temps_restant and nb_players_in_resto(pos_restaurants.index(resto)) < seuil
    ]

    if not restaurants_accessibles:
        # Si aucun restaurant n'est accessible, rester sur place
        preferences[joueur_id] = [position_joueur]
    else:
        # Trouver le restaurant avec le moins de joueurs parmi ceux visibles
        visible_positions = champ_de_vision_func(position_joueur, distance_vision)
        restaurants_visibles = [resto for resto in restaurants_accessibles if resto in visible_positions]

        if not restaurants_visibles:
            # Si aucun restaurant n'est visible, aller au plus éloigné
            preferences[joueur_id] = [restaurants_tries[0]]
        else:
            # Trouver le restaurant avec le moins de joueurs parmi ceux visibles
            meilleur_resto = min(restaurants_visibles, key=lambda r: nb_players_in_resto(pos_restaurants.index(r)))
            preferences[joueur_id] = [meilleur_resto]

def fictitious_play(pos_restaurants, historique, joueur_id):
    """
    Chaque joueur suppose que ses adversaires jouent selon une distribution fixe de stratégies.
    Il observe les choix passés des autres joueurs et calcule la fréquence de chaque stratégie utilisée.
    Il joue ensuite la meilleure réponse à cette distribution de stratégies estimée.
    """
    # Initialiser un dictionnaire pour compter les visites de chaque restaurant
    restaurant_visits = {r: 0 for r in pos_restaurants}  # Initialisation des comptes de visites

    for other_id, visits in historique.items():
        if other_id != joueur_id:  # Ne prendre en compte que les autres joueurs
            for restaurant, count in visits.items():
                restaurant_visits[restaurant] += count

    # Trouver les restaurants les moins fréquentés
    min_visits = min(restaurant_visits.values())  # Nombre minimal de visites
    least_visited_restaurants = [r for r, v in restaurant_visits.items() if v == min_visits]

    return random.choice(least_visited_restaurants)  # Choisir aléatoirement un des restaurants les moins visités

def regret_matching(pos_restaurants, historique, payoffs, last_choice):
    """
    Chaque joueur ajuste ses choix en fonction du regret des décisions passées.
    Le regret d'une action est la différence entre :
    - le gain qu'on aurait obtenu en jouant une autre action.
    - le gain obtenu en jouant l'action réellement choisie.
    """
    num_actions = len(pos_restaurants)
    
    # Premier tour : choix uniforme
    if sum(historique.values()) == 0:
        return random.choice(pos_restaurants)
    
    # Calculer le nombre de rounds joués
    num_rounds = sum(historique.values())
    
    # Calculer le score total obtenu jusqu'à présent
    score_total = payoffs.get(tuple(last_choice), 0) if last_choice else 0
    
    # Calculer les scores hypothétiques
    scores_hypothetiques = np.zeros(num_actions)
    for s in range(num_actions):
        scores_hypothetiques[s] = payoffs.get(tuple(pos_restaurants[s]), 0) / num_rounds
    
    # Calculer les regrets
    regrets = np.array([scores_hypothetiques[s] - score_total / num_rounds 
                       for s in range(num_actions)])
    
    # Gestion des cas initiaux où tous les regrets sont <= 0
    if np.all(regrets <= 0):
        return random.choice(pos_restaurants)
    
    # Calculer les probabilités proportionnelles aux regrets positifs
    regrets_positifs = np.maximum(regrets, 0)
    probabilites = regrets_positifs / np.sum(regrets_positifs)
    
    # Choisir l'action avec la probabilité calculée
    return pos_restaurants[np.random.choice(num_actions, p=probabilites)]

def strategie_greedy_complex(pos_restaurants, nb_players_in_resto, seuil, position_joueur, champ_de_vision_func, distance_vision, temps_restant, joueur_id, preferences, historique_choix_joueurs, players, coupe_files):
    """
    Stratégie greedy complexe qui vérifie si le joueur est déjà dans un restaurant
    et envisage de changer si le seuil est dépassé ou si les autres joueurs se sont arrêtés.
    """
    # Vérifier si le joueur est déjà dans un restaurant
    current_resto_idx = None
    for idx, resto in enumerate(pos_restaurants):
        if position_joueur == resto:
            current_resto_idx = idx
            break

    # Si le joueur est dans un restaurant et que le seuil est dépassé, envisager de changer
    if current_resto_idx is not None:
        nb_joueurs_current = nb_players_in_resto(current_resto_idx)
        if nb_joueurs_current >= seuil:
            # Le joueur doit envisager de changer de restaurant
            preferences[joueur_id] = []  # Réinitialiser les préférences
        else:
            # Vérifier si les autres joueurs se sont arrêtés
            joueurs_arretes = 0
            for other_id, choix in historique_choix_joueurs.items():
                if other_id != joueur_id and choix == position_joueur:
                    joueurs_arretes += 1

            if joueurs_arretes >= 2:
                # Si au moins deux autres joueurs se sont arrêtés, réévaluer les options
                preferences[joueur_id] = []  # Réinitialiser les préférences
            else:
                # Le joueur reste dans le restaurant actuel
                preferences[joueur_id] = [position_joueur]
                return

    # Trier les restaurants par distance décroissante par rapport à la position initiale
    restaurants_tries = sorted(pos_restaurants, key=lambda r: distManhattan(position_joueur, r), reverse=True)

    # Filtrer les restaurants accessibles dans le temps restant et respectant le seuil
    restaurants_accessibles = [
        resto for resto in restaurants_tries
        if distManhattan(position_joueur, resto) <= temps_restant and nb_players_in_resto(pos_restaurants.index(resto)) < seuil
    ]

    if not restaurants_accessibles:
        # Si aucun restaurant n'est accessible, rester sur place
        preferences[joueur_id] = [position_joueur]
    else:
        # Trouver le restaurant avec le moins de joueurs parmi ceux visibles
        visible_positions = champ_de_vision_func(position_joueur, distance_vision)
        restaurants_visibles = [resto for resto in restaurants_accessibles if resto in visible_positions]

        if not restaurants_visibles:
            # Si aucun restaurant n'est visible, aller au plus éloigné
            preferences[joueur_id] = [restaurants_tries[0]]
        else:
            # Trouver le restaurant avec le moins de joueurs parmi ceux visibles
            meilleur_resto = min(restaurants_visibles, key=lambda r: nb_players_in_resto(pos_restaurants.index(r)))
            preferences[joueur_id] = [meilleur_resto]

def strategie_imitation(pos_restaurants, historique_scores, historique_choix):
    """
    Stratégie d'imitation : le joueur examine le score total de tous les joueurs, 
    puis imite le choix de restaurant du joueur ayant le score le plus élevé.
    S'il y a plusieurs joueurs avec le score maximal, il en choisit un au hasard.
    """

    if not historique_scores:
        # S'il n'y a pas encore d'historique, choisir un restaurant au hasard
        return random.choice(pos_restaurants)

    # Trouver le score maximal parmi les joueurs
    max_score = max(historique_scores.values())
    meilleurs_joueurs = [j for j, score in historique_scores.items() if score == max_score]

    # Sélectionner au hasard l'un des joueurs ayant le score maximal
    joueur_a_mimer = random.choice(meilleurs_joueurs)

    # Retourner le dernier restaurant choisi par ce joueur, ou un restaurant au hasard s'il n'y a pas d'historique
    return historique_choix.get(joueur_a_mimer, random.choice(pos_restaurants))

def strategie_sequence_fixe(pos_restaurants, joueur_id, jour_actuel):
    """
    Stratégie de rotation en séquence fixe :
    - Chaque joueur suit une séquence décalée basée sur son identifiant.
    - Parcourt les restaurants dans l'ordre.
    - Une fois arrivé au dernier restaurant, recommence depuis le premier.
    """
    # Trier les restaurants pour assurer un ordre cohérent
    pos_restaurants_sorted = sorted(pos_restaurants)
    
    # Calculer le restaurant à visiter en fonction du jour et de l'identifiant du joueur
    index_resto = (jour_actuel + joueur_id) % len(pos_restaurants_sorted)
    resto_choisi = pos_restaurants_sorted[index_resto]
    
    return resto_choisi
