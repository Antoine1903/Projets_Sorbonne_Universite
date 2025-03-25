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
    """- Les joueurs ont une liste de préférences de restaurants basée sur la distance.
    - Lorsqu'un joueur entre dans un restaurant, ceux qui le voient recalculent leur décision.
    - Si le seuil de joueurs dans le restaurant actuel est atteint, le joueur cherche un autre restaurant visible dans son champ de vision.
    - Si tous les restaurants visibles dépassent le seuil, le joueur se dirige vers le restaurant le plus proche avec le moins de joueurs.
    - Si le temps restant est insuffisant pour changer de restaurant, le joueur reste dans le restaurant atteint.
    """

    # Initialiser les préférences pour chaque joueur en fonction de la distance
    prefs_restaurants = sorted(pos_restaurants, key=lambda resto: distManhattan(position_joueur, resto))

    print(f"🔹 Joueur {joueur_id} - Position actuelle : {position_joueur}")
    print(f"📋 Préférences des restaurants : {prefs_restaurants}")

    print(f"🔍 Joueur {joueur_id} explore le champ de vision : {champ_de_vision}")

    for resto in prefs_restaurants:
        if resto in champ_de_vision:
            nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
            distance = distManhattan(position_joueur, resto)

            print(f"  🔎 Restaurant visible {resto} → Joueurs : {nb_joueurs}, Distance : {distance}")

            # Vérification du seuil et du temps restant
            if nb_joueurs < seuil and distance <= temps_restant:
                print(f"✅ Joueur {joueur_id} choisit {resto} (Meilleur choix visible)")
                return resto


    # Trouver le restaurant le plus proche (le joueur ne voit pas les restaurants)
    best_choice = None
    best_score = (float('inf'), float('inf'))  # Priorité : (nb_joueurs, distance)

    # Parcourir les préférences
    for resto in prefs_restaurants:
        nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
        distance = distManhattan(position_joueur, resto)

        print(f"  📍 Test resto {resto} → Joueurs : {nb_joueurs}, Distance : {distance}")

        # Vérification du temps restant
        if distance <= temps_restant:
            print(f"✅ Joueur {joueur_id} choisit {resto} (Seuil OK, Temps OK)")
            return resto
        else:
            print(f"    ⏳ {resto} est trop loin ! (Distance : {distance}, Temps restant : {temps_restant})")
            continue

        score = (nb_joueurs, distance)  # Priorité : moins de joueurs, puis distance
        if score < best_score:
            best_score = score
            best_choice = resto

    # Si aucun bon choix trouvé, choisir au hasard parmi les accessibles en temps restant
    possibles = [r for r in prefs_restaurants if distManhattan(position_joueur, r) <= temps_restant]
    final_choice = possibles[0] if possibles else random.choice(pos_restaurants)

    print(f"⚠️ Joueur {joueur_id} n'a pas trouvé de choix optimal, prend au hasard : {final_choice}")
    return final_choice

def fictitious_play(pos_restaurants, historique, joueur_id):
    """
    Fictitious Play: 玩家基于过去的经验选择概率最高的餐厅。
    :param pos_restaurants: 所有餐厅位置
    :param historique: 记录每个餐厅的访问情况 {joueur_id: {restaurant: visit_count}}
    :param joueur_id: 当前玩家
    """
    if joueur_id not in historique:
        historique[joueur_id] = {r: 1 for r in pos_restaurants}  # 初始化每个餐厅访问次数至少为 1（避免除 0）

    total = sum(historique[joueur_id].values())
    probabilities = [historique[joueur_id][r] / total for r in pos_restaurants]
    return random.choices(pos_restaurants, weights=probabilities, k=1)[0]

def regret_matching(pos_restaurants, historique, joueur_id, payoffs):
    """
    Regret-Matching: 计算遗憾值，并调整策略以最大化收益。
    :param pos_restaurants: 餐厅位置
    :param historique: 记录玩家去过的餐厅 {joueur_id: {restaurant: visit_count}}
    :param joueur_id: 当前玩家
    :param payoffs: 记录每个餐厅的历史收益 {joueur_id: {restaurant: total_score}}
    """
    if joueur_id not in historique:
        historique[joueur_id] = {r: 1 for r in pos_restaurants}
        payoffs[joueur_id] = {r: 0 for r in pos_restaurants}

    # 计算平均收益
    total_visits = sum(historique[joueur_id].values())
    avg_payoff = {r: payoffs[joueur_id][r] / (historique[joueur_id][r] + 1e-5) for r in pos_restaurants}  # 避免除零

    # 计算遗憾值 (regret)
    max_payoff = max(avg_payoff.values())
    regret = {r: max_payoff - avg_payoff[r] for r in pos_restaurants}

    # 计算新选择概率
    total_regret = sum(max(0, regret[r]) for r in pos_restaurants)
    if total_regret > 0:
        probabilities = [max(0, regret[r]) / total_regret for r in pos_restaurants]
    else:
        probabilities = [1 / len(pos_restaurants)] * len(pos_restaurants)  # 如果没有遗憾值，则均匀随机选择

    return random.choices(pos_restaurants, weights=probabilities, k=1)[0]

def strategie_greedy_complex(pos_restaurants, nb_players_in_resto, seuil, position_joueur, champ_de_vision, temps_restant, joueur_id, nb_players, choix_resto):
    """
    Stratégie greedy complexe :
    - Les joueurs ont une liste de préférences de restaurants basée sur la distance.
    - Lorsqu'un joueur entre dans un restaurant, ceux qui le voient recalculent leur décision.
    - Si le seuil de joueurs dans le restaurant actuel est atteint, le joueur cherche un autre restaurant visible dans son champ de vision.
    - Si tous les restaurants visibles dépassent le seuil, le joueur se dirige vers le restaurant le plus proche avec le moins de joueurs.
    - Si le temps restant est insuffisant pour changer de restaurant, le joueur reste dans le restaurant atteint.

    Différences avec la stratégie greedy :
    - **Réévaluation dynamique** : Contrairement à la stratégie greedy de base, cette version permet aux joueurs de réévaluer leur choix en cours de jeu.
    - **Champ de vision** : Les joueurs prennent en compte les restaurants visibles pour ajuster leur décision.
    - **Flexibilité** : Les joueurs peuvent changer de restaurant même après avoir fait un choix initial, s'ils trouvent une meilleure option.
    - **Gestion du temps restant** : La stratégie vérifie constamment le temps restant pour atteindre les restaurants potentiels, permettant des ajustements en temps réel.
    """

    # Initialiser les préférences pour chaque joueur en fonction de la distance
    prefs_restaurants = sorted(pos_restaurants, key=lambda resto: distManhattan(position_joueur, resto))

    print(f"🔹 Joueur {joueur_id} - Position actuelle : {position_joueur}")
    print(f"📋 Préférences des restaurants : {prefs_restaurants}")

    print(f"🔍 Joueur {joueur_id} explore le champ de vision : {champ_de_vision}")

    # Vérifier si le joueur est déjà dans un restaurant
    if position_joueur in pos_restaurants:
        current_resto_index = pos_restaurants.index(position_joueur)
        current_nb_joueurs = nb_players_in_resto(current_resto_index)

        # Si le restaurant actuel dépasse le seuil, envisager de changer
        if current_nb_joueurs >= seuil:
            print(f"⚠️ Joueur {joueur_id} réévalue sa décision car le restaurant actuel a trop de joueurs.")
            for resto in prefs_restaurants:
                if resto in champ_de_vision and resto != position_joueur:
                    nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
                    distance = distManhattan(position_joueur, resto)

                    print(f"  🔎 Restaurant visible {resto} → Joueurs : {nb_joueurs}, Distance : {distance}")

                    # Vérification du seuil et du temps restant
                    if nb_joueurs < seuil and distance <= temps_restant:
                        print(f"✅ Joueur {joueur_id} change pour {resto} (Meilleur choix visible)")
                        choix_resto[joueur_id] = resto
                        return

    # Si le joueur n'est pas dans un restaurant ou s'il n'y a pas de meilleure option visible, trouver le meilleur choix
    best_choice = None
    best_score = (float('inf'), float('inf'))  # Priorité : (nb_joueurs, distance)

    for resto in prefs_restaurants:
        nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
        distance = distManhattan(position_joueur, resto)

        print(f"  📍 Test resto {resto} → Joueurs : {nb_joueurs}, Distance : {distance}")

        # Vérification du temps restant
        if distance <= temps_restant:
            score = (nb_joueurs, distance)  # Priorité : moins de joueurs, puis distance
            if score < best_score:
                best_score = score
                best_choice = resto
        else:
            print(f"    ⏳ {resto} est trop loin ! (Distance : {distance}, Temps restant : {temps_restant})")

    # Si un meilleur choix est trouvé, le prendre
    if best_choice:
        print(f"✅ Joueur {joueur_id} choisit {best_choice} (Meilleur choix global)")
        choix_resto[joueur_id] = best_choice
        return

    # Si aucun bon choix trouvé, choisir au hasard parmi les accessibles en temps restant
    possibles = [r for r in prefs_restaurants if distManhattan(position_joueur, r) <= temps_restant]
    final_choice = possibles[0] if possibles else random.choice(pos_restaurants)

    print(f"⚠️ Joueur {joueur_id} n'a pas trouvé de choix optimal, prend au hasard : {final_choice}")
    choix_resto[joueur_id] = final_choice
