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

def strategie_greedy(pos_restaurants, nb_players_in_resto, seuil, current_pos, visited_restaurants, iterations, i):
    """Stratégie greedy : le joueur se dirige vers un restaurant aléatoire et vérifie l'occupation à chaque étape."""
    # Choisir un restaurant aléatoire initialement
    target_resto = random.choice(pos_restaurants)

    # Vérifier l'occupation du restaurant actuel
    if current_pos in pos_restaurants:
        r = pos_restaurants.index(current_pos)
        if nb_players_in_resto(r) - 1 < seuil:
            return current_pos  # Rester dans le restaurant actuel

    # Si le restaurant actuel est trop occupé ou si le joueur n'est pas dans un restaurant, aller vers le restaurant cible
    if len(visited_restaurants) == len(pos_restaurants) or (iterations - i) <= len(pos_restaurants):
        # Augmenter le seuil si tous les restaurants ont été visités ou s'il n'y a plus assez de temps
        seuil += 1
        visited_restaurants.clear()

    # Marquer le restaurant comme visité
    visited_restaurants.add(target_resto)

    return target_resto
