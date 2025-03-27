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

def strategie_greedy(pos_restaurants, nb_players_in_resto, seuil, position_joueur, champ_de_vision, temps_restant, joueur_id, nb_players, choix_resto):
    """
    - Les joueurs ont une liste de restaurants à visiter basée sur la distance (le plus éloigné en priorité).
    - Lorsqu'un joueur entre dans un restaurant, ceux qui le voient recalculent leur décision.
    - Si le seuil de joueurs dans le restaurant actuel est atteint, le joueur cherche à se rendre dans son prochain restaurant de sa liste.
    - Une fois tous les restaurants essayés, s'ils dépassent tous le seuil, le joueur se dirige vers le restaurant avec le moins de joueurs, mais s'il n'a pas le temps, chercher celui avec le moins de joueurs qu'il est possible d'atteindre avec le temps qu'il lui reste.
    """

    # Initialiser les préférences pour chaque joueur en fonction de la distance (le plus éloigné en priorité)
    prefs_restaurants = sorted(range(len(pos_restaurants)), key=lambda idx: distManhattan(position_joueur, pos_restaurants[idx]), reverse=True)
    
    print(f"🔹 Joueur {joueur_id+1} - Position actuelle : {position_joueur}")
    print(f"📋 Préférences des restaurants (le plus éloigné en priorité) : {[pos_restaurants[idx] for idx in prefs_restaurants]}")

    print(f"🔍 Joueur {joueur_id+1} explore le champ de vision : {champ_de_vision}")

    # Vérification des restaurants visibles
    for idx in prefs_restaurants:
        resto = pos_restaurants[idx]
        if resto in champ_de_vision:
            nb_players_resto = nb_players_in_resto(idx)
            distance = distManhattan(position_joueur, resto)

            print(f"  🔎 Restaurant visible {resto} → Joueurs : {nb_players_resto}, Distance : {distance}")

            if nb_players_resto < seuil and distance <= temps_restant:
                print(f"✅ Joueur {joueur_id+1} choisit {resto} (Meilleur choix visible)")
                choix_resto[joueur_id] = resto
                return

    # Si aucun restaurant visible ne respecte le critère, choisir celui avec le moins de joueurs accessible
    best_choices = []
    best_score = (float('inf'), float('inf'))  # Moins de joueurs, puis distance min

    for idx in prefs_restaurants:
        resto = pos_restaurants[idx]
        if resto in champ_de_vision:
            nb_players_resto = nb_players_in_resto(idx)
            distance = distManhattan(position_joueur, resto)

            print(f"  📍 Test resto {resto} → Joueurs : {nb_players_resto}, Distance : {distance}")

            if distance <= temps_restant:
                score = (nb_players_resto, distance)  # Moins de joueurs, puis le plus proche
                if score < best_score:
                    best_choices = [(idx, resto)]
                    best_score = score
                elif score == best_score:
                    best_choices.append((idx, resto))

    if best_choices:
        # Choisir le restaurant le plus proche parmi les meilleurs choix
        best_choice = min(best_choices, key=lambda x: distManhattan(position_joueur, x[1]))[1]
        print(f"⚠️ Joueur {joueur_id+1} choisit le restaurant le plus proche parmi les restaurants avec le moins de joueurs accessibles : {best_choice}")
        choix_resto[joueur_id] = best_choice
    else:
        print(f"🚨 Joueur {joueur_id+1} ne peut atteindre aucun restaurant, reste sur place")
        choix_resto[joueur_id] = position_joueur  # Ou autre stratégie de fallback
    return

def fictitious_play(pos_restaurants, historique, joueur_id):
    """
    Jeu fictif : le joueur choisit un restaurant en fonction des probabilités
    calculées à partir de ses expériences passées.
    """
    if joueur_id not in historique:
        # Initialiser l'historique du joueur
        historique[joueur_id] = {r: 0 for r in pos_restaurants}

    # Calculer le total des visites
    total_visits = sum(historique[joueur_id].values())

    if total_visits == 0:
        # Si aucun restaurant n'a été visité, choisir un restaurant au hasard
        return random.choice(pos_restaurants)

    # Calculer les probabilités uniquement pour les restaurants visités
    probabilities = [historique[joueur_id][r] / total_visits for r in pos_restaurants]

    # Sélectionner un restaurant en fonction des probabilités calculées
    return random.choices(pos_restaurants, weights=probabilities, k=1)[0]


def regret_matching(pos_restaurants, historique, joueur_id, payoffs):
    """
    Stratégie d'appariement au regret : calcule les regrets et ajuste la stratégie 
    pour maximiser les gains futurs.
    """
    if joueur_id not in historique:
        historique[joueur_id] = {r: 1 for r in pos_restaurants}
        payoffs[joueur_id] = {r: 0 for r in pos_restaurants}

    # Calcul du gain moyen par restaurant
    total_visits = sum(historique[joueur_id].values())
    avg_payoff = {r: payoffs[joueur_id][r] / (historique[joueur_id][r] + 1e-5) for r in pos_restaurants}  # Évite la division par zéro

    # Calcul des regrets (écart entre le meilleur gain et les autres)
    max_payoff = max(avg_payoff.values())
    regret = {r: max_payoff - avg_payoff[r] for r in pos_restaurants}

    # Calcul des probabilités de sélection basées sur le regret
    total_regret = sum(max(0, regret[r]) for r in pos_restaurants)
    if total_regret > 0:
        probabilities = [max(0, regret[r]) / total_regret for r in pos_restaurants]
    else:
        # Si aucun regret, choisir un restaurant de manière uniforme aléatoire
        probabilities = [1 / len(pos_restaurants)] * len(pos_restaurants)

    # Sélectionner un restaurant en fonction des probabilités ajustées par le regret
    return random.choices(pos_restaurants, weights=probabilities, k=1)[0]

def strategie_greedy_complex(pos_restaurants, nb_players_in_resto, seuil, position_joueur, champ_de_vision, temps_restant, joueur_id, nb_players, choix_resto):
    """
    Stratégie greedy complexe :
    - Les joueurs ont une liste de restaurants à visiter basée sur la distance (le plus éloigné en priorité).
    - Lorsqu'un joueur entre dans un restaurant, ceux qui le voient recalculent leur décision.
    - Si le seuil de joueurs dans le restaurant actuel est atteint, le joueur cherche à se rendre dans son prochain restaurant de sa liste.

    Différences avec la stratégie greedy :
    - **Réévaluation dynamique** : Contrairement à la stratégie greedy de base, cette version permet aux joueurs de réévaluer leur choix en cours de jeu.
    - **Champ de vision** : Les joueurs prennent en compte les restaurants visibles pour ajuster leur décision.
    - **Flexibilité** : Les joueurs peuvent changer de restaurant même après avoir fait un choix initial, s'ils trouvent une meilleure option.
    - **Gestion du temps restant** : La stratégie vérifie constamment le temps restant pour atteindre les restaurants potentiels, permettant des ajustements en temps réel.
    """

    # Initialiser les préférences pour chaque joueur en fonction de la distance (le plus éloigné en priorité)
    prefs_restaurants = sorted(range(len(pos_restaurants)), key=lambda idx: distManhattan(position_joueur, pos_restaurants[idx]), reverse=True)
    choix_resto[joueur_id] = prefs_restaurants[0]

    print(f"🔹 Joueur {joueur_id+1} - Position actuelle : {position_joueur}")
    print(f"📋 Préférences des restaurants : {prefs_restaurants}")

    print(f"🔍 Joueur {joueur_id+1} explore le champ de vision : {champ_de_vision}")

    # Vérifier si le joueur est déjà dans un restaurant
    if position_joueur in pos_restaurants:
        current_resto_index = pos_restaurants.index(position_joueur)
        current_nb_joueurs = nb_players_in_resto(current_resto_index)

        # Si le restaurant actuel dépasse le seuil, envisager de changer
        if current_nb_joueurs >= seuil:
            print(f"⚠️ Joueur {joueur_id+1} réévalue sa décision car le restaurant actuel a trop de joueurs.")
            for resto in prefs_restaurants:
                if resto in champ_de_vision and resto != position_joueur:
                    nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
                    distance = distManhattan(position_joueur, resto)

                    print(f"  🔎 Restaurant visible {resto} → Joueurs : {nb_joueurs}, Distance : {distance}")

                    # Vérification du seuil et du temps restant
                    if nb_joueurs < seuil and distance <= temps_restant:
                        print(f"✅ Joueur {joueur_id+1} change pour {resto} (Meilleur choix visible)")
                        choix_resto[joueur_id] = resto
                        return

    # Si le joueur n'est pas dans un restaurant poursuivre comme la stratégie greedy
    for idx in prefs_restaurants:
        resto = pos_restaurants[idx]
        if resto in champ_de_vision:
            nb_players_resto = nb_players_in_resto(idx)
            distance = distManhattan(position_joueur, resto)

            print(f"  🔎 Restaurant visible {resto} → Joueurs : {nb_players_resto}, Distance : {distance}")

            if nb_players_resto < seuil and distance <= temps_restant:
                print(f"✅ Joueur {joueur_id+1} choisit {resto} (Meilleur choix visible)")
                choix_resto[joueur_id] = resto
                return

    # Si aucun restaurant visible ne respecte le critère, choisir celui avec le moins de joueurs accessible
    best_choices = []
    best_score = (float('inf'), float('inf'))  # Moins de joueurs, puis distance min

    for idx in prefs_restaurants:
        resto = pos_restaurants[idx]
        if resto in champ_de_vision:
            nb_players_resto = nb_players_in_resto(idx)
            distance = distManhattan(position_joueur, resto)

            print(f"  📍 Test resto {resto} → Joueurs : {nb_players_resto}, Distance : {distance}")

            if distance <= temps_restant:
                score = (nb_players_resto, distance)  # Moins de joueurs, puis le plus proche
                if score < best_score:
                    best_choices = [(idx, resto)]
                    best_score = score
                elif score == best_score:
                    best_choices.append((idx, resto))

    if best_choices:
        # Choisir le restaurant le plus proche parmi les meilleurs choix
        best_choice = min(best_choices, key=lambda x: distManhattan(position_joueur, x[1]))[1]
        print(f"⚠️ Joueur {joueur_id+1} choisit le restaurant le plus proche parmi les restaurants avec le moins de joueurs accessibles : {best_choice}")
        choix_resto[joueur_id] = best_choice
    else:
        print(f"🚨 Joueur {joueur_id+1} ne peut atteindre aucun restaurant, reste sur place")
        choix_resto[joueur_id] = position_joueur  # Ou autre stratégie de fallback
    return

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

def strategie_sequence_fixe(pos_restaurants, historique_sequence, joueur_id, jour_actuel=None):
    """
    Stratégie de rotation en séquence fixe :
    - Chaque joueur suit une séquence décalée basée sur son identifiant.
    - Parcourt les restaurants dans l'ordre.
    - Une fois arrivé au dernier restaurant, recommence depuis le premier.
    """
    if jour_actuel is None:
        jour_actuel = 0  # Par défaut, premier jour s'il n'est pas précisé

    # Trier les restaurants pour assurer un ordre cohérent
    pos_restaurants_sorted = sorted(pos_restaurants)

    # Calculer le restaurant à visiter en fonction du jour et de l'identifiant du joueur
    # Chaque joueur a un décalage propre dans la séquence
    index_resto = (jour_actuel + joueur_id) % len(pos_restaurants_sorted)
    resto_choisi = pos_restaurants_sorted[index_resto]

    print(f"📅 Joueur {joueur_id+1} Jour {jour_actuel+1} : "
          f"Resto {index_resto+1}/{len(pos_restaurants_sorted)} → {resto_choisi}")

    return resto_choisi
