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
    Stratégie greedy avec tests :
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

    print(f"🟢 Joueur {joueur_id} - Position actuelle : {position_joueur}")
    print(f"🔹 Préférences des restaurants : {preferences}")

    # Parcourir les préférences
    for resto in preferences:
        if resto in pos_restaurants:
            nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
            distance = distManhattan(position_joueur, resto)

            print(f"  📍 Test resto {resto} → Joueurs : {nb_joueurs}, Distance : {distance}")

            # Vérification du seuil et du temps restant
            if nb_joueurs < seuil and distance <= temps_restant:
                print(f"✅ Joueur {joueur_id} choisit {resto} (Seuil OK, Temps OK)")
                return resto

    # Si tous les restaurants préférés dépassent le seuil :
    # Trouver le restaurant visible le plus proche avec le moins de joueurs
    best_choice = None
    best_score = (float('inf'), float('inf'))  # Priorité : (nb_joueurs, distance)

    print(f"🔍 Joueur {joueur_id} explore le champ de vision : {champ_de_vision}")

    for resto in champ_de_vision:
        if resto in pos_restaurants:
            nb_joueurs = nb_players_in_resto(pos_restaurants.index(resto))
            distance = distManhattan(position_joueur, resto)

            print(f"  🔎 Restaurant visible {resto} → Joueurs : {nb_joueurs}, Distance : {distance}")

            # Vérifier que le joueur a assez de temps pour y aller
            if distance > temps_restant:
                print(f"    ⏳ {resto} est trop loin ! (Distance : {distance}, Temps restant : {temps_restant})")
                continue

            score = (nb_joueurs, distance)  # Priorité : moins de joueurs, puis distance
            if score < best_score:
                best_score = score
                best_choice = resto

    if best_choice:
        print(f"✅ Joueur {joueur_id} choisit {best_choice} (Meilleur choix visible)")
        return best_choice

    # Si aucun bon choix trouvé, choisir au hasard parmi les accessibles en temps restant
    possibles = [r for r in champ_de_vision if distManhattan(position_joueur, r) <= temps_restant]
    final_choice = random.choice(possibles) if possibles else random.choice(pos_restaurants)

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

def strategie_imitation(pos_restaurants, historique_scores, historique_choix):
    """
    战略模仿：玩家查看所有玩家的得分总和，然后模仿得分最高的玩家的餐厅选择。
    如果有多个得分最高的玩家，则随机选择其中之一进行模仿。

    :param pos_restaurants: 所有餐厅位置
    :param historique_scores: 记录每个玩家的历史得分 {joueur_id: total_score}
    :param historique_choix: 记录每个玩家的历史餐厅选择 {joueur_id: dernier_choix}
    :param joueur_id: 当前玩家ID
    :return: 选择的餐厅
    """

    if not historique_scores:
        # 如果没有历史数据，则随机选择一个餐厅
        return random.choice(pos_restaurants)

    # 找到得分最高的玩家
    max_score = max(historique_scores.values())
    meilleurs_joueurs = [j for j, score in historique_scores.items() if score == max_score]

    # 随机选择一个得分最高的玩家进行模仿
    joueur_a_mimer = random.choice(meilleurs_joueurs)

    # 返回该玩家上次选择的餐厅，如果有的话
    return historique_choix.get(joueur_a_mimer, random.choice(pos_restaurants))

# In the strategies.py file:

def strategie_sequence_fixe(pos_restaurants, historique_sequence, joueur_id, jour_actuel=None):
    """
    Fixed sequence rotation strategy:
    - Each player has their own sequence offset based on their ID
    - Cycles through restaurants in order
    - After last restaurant, starts again from first
    
    :param pos_restaurants: List of all restaurant positions (sorted)
    :param historique_sequence: Dictionary to track state (unused here)
    :param joueur_id: Current player ID (used for sequence offset)
    :param jour_actuel: Current day (0-based)
    :return: Restaurant to visit on current day
    """
    if jour_actuel is None:
        jour_actuel = 0  # Default to first day if not specified
    
    # Ensure restaurant list is sorted for consistent ordering
    pos_restaurants_sorted = sorted(pos_restaurants)
    
    # Calculate which restaurant to visit based on day number and player ID
    # This ensures each player has their own sequence offset
    index_resto = (jour_actuel + joueur_id) % len(pos_restaurants_sorted)
    resto_choisi = pos_restaurants_sorted[index_resto]
    
    print(f"📅 Joueur {joueur_id} Jour {jour_actuel+1}: "
          f"Resto {index_resto+1}/{len(pos_restaurants_sorted)} → {resto_choisi}")
    
    return resto_choisi
