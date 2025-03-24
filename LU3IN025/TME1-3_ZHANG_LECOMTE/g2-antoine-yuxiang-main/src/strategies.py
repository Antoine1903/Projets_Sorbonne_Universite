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

def strategie_greedy(pos_restaurants, nb_players_in_resto, seuil, position_joueur, champ_de_vision, temps_restant, joueur_id, nb_players):
    """
    Stratégie greedy :
    - Les joueurs ont une liste de préférences de restaurants.
    - Lorsqu'un joueur entre dans un restaurant, ceux qui le voient recalculent leur décision.
    - Si le seuil est atteint, le joueur cherche un autre restaurant de sa liste.
    - Si tous les restaurants visibles dépassent son seuil, il va au plus proche avec le moins de joueurs.
    - Si le temps manque pour changer, il reste dans le restaurant atteint.
    """
    # Initialiser les préférences pour chaque joueur
    prefs_restaurants = [pos_restaurants.copy() for _ in range(nb_players)]
    for prefs in prefs_restaurants:
        random.shuffle(prefs)

    if joueur_id >= len(prefs_restaurants):
        # Initialiser les préférences si elles ne sont pas définies
        prefs_restaurants.append(pos_restaurants.copy())
        random.shuffle(prefs_restaurants[joueur_id])

    preferences = prefs_restaurants[joueur_id]

    for resto in preferences:
        if resto in pos_restaurants:
            nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
            distance = distManhattan(position_joueur, resto)

            # Vérification du seuil et du temps restant
            if nb_joueurs < seuil and distance <= temps_restant:
                return resto

    # Si tous les restaurants préférés dépassent le seuil :
    # Trouver le restaurant visible le plus proche avec le moins de joueurs
    best_choice = None
    best_score = (float('inf'), float('inf'))  # Utiliser un tuple pour le score

    for resto in champ_de_vision:
        if resto in pos_restaurants:
            nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
            distance = distManhattan(position_joueur, resto)

            print(f"Joueur {joueur_id} : Restaurant visible {resto} - Joueurs = {nb_joueurs}, Distance = {distance}")

            # Vérifier que le joueur a assez de temps pour y aller
            if distance > temps_restant:
                continue

            score = (nb_joueurs, distance)  # Priorité à moins de joueurs, puis distance

            if score < best_score:
                best_score = score
                best_choice = resto

    # Si aucun bon choix trouvé (peu probable), choisir au hasard parmi les accessibles en temps_restant
    possibles = [r for r in champ_de_vision if abs(position_joueur[0] - r[0]) + abs(position_joueur[1] - r[1]) <= temps_restant]
    return best_choice if best_choice else (random.choice(possibles) if possibles else random.choice(pos_restaurants))