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

def strategie_greedy(pos_restaurants, nb_players_in_resto, seuil, position_joueur, champ_de_vision, temps_restant, joueur_id, nb_players, choix_resto, preferences):
    """
    - Les joueurs ont une liste de restaurants à visiter basée sur la distance (le plus éloigné en priorité).
    - Lorsqu'un joueur entre dans un restaurant, ceux qui le voient parmi les greedy recalculent leur décision.
    - Si le seuil de joueurs dans le restaurant actuel est atteint, le joueur cherche à se rendre dans son prochain restaurant de sa liste.
    - Une fois tous les restaurants essayés, s'ils dépassent tous le seuil, le joueur se dirige vers le restaurant avec le moins de joueurs s'il lui reste suffisamment de temps.
    - S'il n'a pas le temps, chercher celui avec le moins de joueurs qu'il est possible d'atteindre avec le temps qu'il lui reste.
    """
    # Trier les restaurants par distance (le plus éloigné en premier)
    restaurants_tries = sorted(pos_restaurants, key=lambda r: distManhattan(position_joueur, r), reverse=True)

    # Initialiser le tableau de préférences
    preferences[joueur_id] = []

    # Vérifier chaque restaurant dans l'ordre
    for resto in restaurants_tries:
        # Vérifier si le restaurant est visible
        if resto in champ_de_vision:
            # Obtenir l'index du restaurant
            resto_idx = pos_restaurants.index(resto)
            # Obtenir le nombre de joueurs dans ce restaurant
            nb_joueurs = nb_players_in_resto(resto_idx)
            # Calculer la distance
            distance = distManhattan(position_joueur, resto)

            # Si le restaurant n'est pas plein et accessible dans le temps restant
            if nb_joueurs < seuil and distance <= temps_restant:
                preferences[joueur_id].append(resto)

    # Si aucun restaurant disponible n'a été trouvé, ajouter les restaurants accessibles
    if not preferences[joueur_id]:
        for resto in restaurants_tries:
            resto_idx = pos_restaurants.index(resto)
            distance = distManhattan(position_joueur, resto)
            if distance <= temps_restant:
                preferences[joueur_id].append(resto)

    # Si aucun restaurant n'est accessible, rester sur place
    if not preferences[joueur_id]:
        preferences[joueur_id].append(position_joueur)

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

def regret_matching(pos_restaurants, historique, joueur_id, payoffs, last_choice):
    """
    Chaque joueur ajuste ses choix en fonction du regret des décisions passées.
    Le regret d'une action est la différence entre :
    - le gain qu'on aurait obtenu en jouant une autre action.
    - le gain obtenu en jouant l'action réellement choisie.
    """
    num_actions = len(pos_restaurants)
    action_indices = list(range(num_actions))

    # Calculer le nombre de rounds joués
    num_rounds = sum(historique.values())

    # Calculer le score total obtenu jusqu'à la période t
    score_total = 0
    if last_choice is not None and tuple(last_choice) in payoffs:
        score_total = payoffs[tuple(last_choice)]

    # Calculer le score hypothétique pour chaque stratégie s
    scores_hypothetiques = np.zeros(num_actions)
    for s in range(num_actions):
        if tuple(pos_restaurants[s]) in payoffs:
            scores_hypothetiques[s] = payoffs[tuple(pos_restaurants[s])]

    # Calculer le regret pour chaque stratégie s
    regrets = np.array([scores_hypothetiques[s] - score_total for s in range(num_actions)])

    # Calculer la somme des regrets positifs
    somme_regrets_positifs = sum(max(0, regret) for regret in regrets)

    if somme_regrets_positifs == 0:
        # Si tous les regrets sont négatifs ou nuls, choisir uniformément au hasard
        probabilites = np.ones(num_actions) / num_actions
    else:
        # Calculer les probabilités proportionnelles aux regrets positifs
        probabilites = np.array([max(0, regret) / somme_regrets_positifs for regret in regrets])

    # Choisir l'action avec la probabilité calculée
    chosen_index = np.random.choice(action_indices, p=probabilites)
    next_action = pos_restaurants[chosen_index]

    return next_action

def strategie_greedy_complex(pos_restaurants, nb_players_in_resto, seuil, position_joueur, champ_de_vision, temps_restant, joueur_id, nb_players, choix_resto, preferences, historique_choix_joueurs):
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
            print(f"Joueur {joueur_id} envisage de changer de restaurant car le seuil est dépassé.")
            preferences[joueur_id] = []  # Réinitialiser les préférences
        else:
            # Vérifier si les autres joueurs se sont arrêtés
            joueurs_arretes = 0
            for other_id, choix in historique_choix_joueurs.items():
                if other_id != joueur_id and choix == position_joueur:
                    joueurs_arretes += 1

            if joueurs_arretes >= 2:
                # Si au moins deux autres joueurs se sont arrêtés, réévaluer les options
                print(f"Joueur {joueur_id} réévalue ses options car d'autres joueurs se sont arrêtés.")
                preferences[joueur_id] = []  # Réinitialiser les préférences
            else:
                # Le joueur reste dans le restaurant actuel
                preferences[joueur_id] = [position_joueur]
                return

    # Trier les restaurants par distance (le plus éloigné en premier)
    restaurants_tries = sorted(pos_restaurants, key=lambda r: distManhattan(position_joueur, r), reverse=True)

    # Initialiser le tableau de préférences
    preferences[joueur_id] = []

    # Vérifier chaque restaurant dans l'ordre
    for resto in restaurants_tries:
        # Vérifier si le restaurant est visible
        if resto in champ_de_vision:
            # Obtenir l'index du restaurant
            resto_idx = pos_restaurants.index(resto)
            # Obtenir le nombre de joueurs dans ce restaurant
            nb_joueurs = nb_players_in_resto(resto_idx)
            # Calculer la distance
            distance = distManhattan(position_joueur, resto)

            # Si le restaurant n'est pas plein et accessible dans le temps restant
            if nb_joueurs < seuil and distance <= temps_restant:
                preferences[joueur_id].append(resto)

    # Si aucun restaurant disponible n'a été trouvé, ajouter les restaurants accessibles
    if not preferences[joueur_id]:
        for resto in restaurants_tries:
            resto_idx = pos_restaurants.index(resto)
            distance = distManhattan(position_joueur, resto)
            if distance <= temps_restant:
                preferences[joueur_id].append(resto)

    # Si aucun restaurant n'est accessible, rester sur place
    if not preferences[joueur_id]:
        preferences[joueur_id].append(position_joueur)

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
