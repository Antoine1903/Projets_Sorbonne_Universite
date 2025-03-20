import random

def strategie_tetue(pos_restaurants, joueur_id, choix_initiaux):
    """Stratégie têtue : le joueur va toujours au même restaurant qu'il a choisi au premier jour."""
    if joueur_id not in choix_initiaux:
        # Si c'est le premier jour, choisir un restaurant au hasard
        choix_initiaux[joueur_id] = random.choice(pos_restaurants)
    return choix_initiaux[joueur_id]

def strategie_stochastique(pos_restaurants, probabilites):
    """Stratégie stochastique : le joueur choisit un restaurant selon une distribution de probabilité."""
    return random.choices(pos_restaurants, weights=probabilites, k=1)[0]

def strategie_greedy(pos_restaurants, nb_players_in_resto, seuil, position_joueur, visited_restaurants, iterations, joueur_id, champ_de_vision):
    scores_restos = []
    for r in range(len(pos_restaurants)):
        pos = pos_restaurants[r]
        if pos in visited_restaurants:
            continue
        if pos in champ_de_vision:
            joueurs_present = nb_players_in_resto(r)
            if joueurs_present < seuil:
                scores_restos.append((joueurs_present, pos))
    if scores_restos:
        return min(scores_restos)[1]
    return random.choice(pos_restaurants)
