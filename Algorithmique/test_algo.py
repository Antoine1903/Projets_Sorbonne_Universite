import time
import matplotlib.pyplot as plt
import random

TEST_ALGO_I = False  # Pour ne pas tester l'algorithme 1 (tests gourmands)



def lire_entrees(fichier):
    with open(fichier, 'r') as f:
        lignes = f.readlines()

    S = int(lignes[0].strip()) # Première ligne : quantité de confiture
    k = int(lignes[1].strip()) # Deuxième ligne : nombre de types de bocaux
    V = list(map(int, lignes[2:])) # À partir de la troisième ligne, les capacités des bocaux
    
    V.sort() # Trier par ordre croissant
    return S, k, V



def algo_I(S, k, V):
    if S == 0:
        return 0  # Pas besoin de bocal pour 0 confiture
    if k == 0 or S < 0:
        return float('inf')  # Impossible sans bocaux ou si S est négatif

    # Option 1 : Ne pas utiliser le bocal de type k
    option1 = algo_I(S, k - 1, V)

    # Option 2 : Utiliser un bocal de type k
    option2 = algo_I(S - V[k - 1], k, V) + 1

    return min(option1, option2)



def algo_II(S, k, V):
    # Si S est négatif, retourner l'infini pour indiquer que c'est impossible
    if S < 0:
        return float('inf'), []  # Retourner M[S][k] va créer une erreur sinon
    
    # Initialisation du tableau M de dimensions (S+1) x (k+1)
    M = [[0 if s == 0 else float('inf') for _ in range(k + 1)] for s in range(S + 1)]

    # Remplissage du tableau
    for i in range(1, k + 1):  # Parcourir chaque type de bocal
        for s in range(S + 1):  # Parcourir toutes les quantités possibles
            if s < V[i - 1]:  # Si la quantité courante est inférieure à la capacité du bocal
                M[s][i] = M[s][i - 1]  # Ne pas utiliser le bocal de type i
            else:
                # Relation de récurrence : utiliser ou ne pas utiliser le bocal de type i
                M[s][i] = min(M[s][i - 1], M[s - V[i - 1]][i] + 1)

    return M[S][k], M  # Retourner à la fois la solution optimale et la matrice M

def backward(M, S, k, V):
    A = [0] * k
    s = S

    for i in range(k, 0, -1):
        while s > 0 and M[s][i] != M[s][i - 1]:
            A[i - 1] += 1  # Ajouter un bocal de type i
            s -= V[i - 1]  # Décrémenter la quantité restante

    return A if s == 0 else "Impossible"



def algo_III(S, k, V):
    A = [0] * k  # Initialisation du tableau des bocaux
    s = S  # Quantité de confiture restante à répartir

    for i in range(k - 1, -1, -1):  # Parcourir les bocaux de grande à petite capacité
        while s >= V[i]:
            A[i] += 1  # Ajouter un bocal de type i
            s -= V[i]  # Décrémenter la quantité restante

    # Retourner la somme des bocaux ou l'infini si c'est impossible
    return sum(A) if s == 0 else float('inf')



def test_glouton_compatible(k, V):
    if k >= 3:
        for S in range(V[2] + 2, V[k - 2] + V[k - 1]):  # V[2] correspond à V[3] (indexé à 1 dans le pseudo-code)
            for j in range(k):
                if V[j] < S:
                    # Comparer les résultats de l'algorithme glouton
                    if algo_III(S, k, V) > 1 + algo_III(S - V[j], k, V):
                        return False
    return True



def test():
    # Lire les entrées du fichier
    S, k, V = lire_entrees('data.txt')
    
    print(f"Quantité totale de confiture (S): {S} dg")
    print(f"Nombre de types de bocaux (k): {k}")
    print(f"Capacités des bocaux (V): {V}")
    
    # Test de l'algorithme récursif (algo_I)
    print("\nRésultat de l'algorithme récursif (AlgoI):")
    resultat_recursif = algo_I(S, k, V)
    print(resultat_recursif)
    
    # Test de l'algorithme dynamique (algo_II)
    print("\nRésultat de l'algorithme dynamique (AlgoII):")
    resultat_dynamique, M = algo_II(S, k, V)  # Récupérer la matrice M
    print(resultat_dynamique)
    
    # Test de l'algorithme glouton (algo_III)
    print("\nRésultat de l'algorithme glouton (AlgoIII):")
    resultat_glouton = algo_III(S, k, V)  # Récupérer le nombre de bocaux
    print(resultat_glouton)
    
    # Vérification de la compatibilité glouton
    compatible = test_glouton_compatible(k, V)
    if compatible:
        print("V glouton-compatible ? Oui")
    else:
        print("V glouton-compatible ? Non")
    
    # Afficher les bocaux utilisés
    A = [0] * k  
    s = S  
    for i in range(k - 1, -1, -1):  
        while s >= V[i]:
            A[i] += 1  
            s -= V[i]  
    if s == 0:
        print(f"Tableau des bocaux utilisés:\n{A}")
    else:
        print(f"Tableau des bocaux utilisés:\nImpossible")

    # Affichage de l'algorithme backward pour reconstituer la solution
    print("\nRésultat de l'algorithme backward (Retourner les bocaux utilisés):")
    resultat_backward = backward(M, S, k, V)  # Passez M à backward
    print(resultat_backward)



def mesurer_temps_execution(algorithme, *args):
    start_time = time.time()
    resultat = algorithme(*args)
    end_time = time.time()
    return resultat, end_time - start_time



def test_et_generer_graphiques():
    # Données pour les graphiques
    resultats_S = {d: {"S_values": [], "temps_algo_i_S": [], "temps_algo_ii_S": [], "temps_algo_iii_S": []} for d in [2, 3, 4]}
    resultats_k = {d: {"k_values": [], "temps_algo_i_k": [], "temps_algo_ii_k": [], "temps_algo_iii_k": []} for d in [2, 3, 4]}

    for d in [2, 3, 4]:  # Variation des systèmes Expo
        print(f"Tests pour d = {d}")

        # Préparer les capacités Expo
        max_k = 30  # Valeur maximale de k
        capacites = [d**i for i in range(max_k)]

        # Étude du temps en fonction de S
        k_fixed = 5  # Fixer \( k \) pour cette étude
        for S in range(0, 1000001, 200000):
            print(f"Test pour d={d}, S={S}, k={k_fixed}")

            if TEST_ALGO_I:  # Vérifier si l'algorithme 1 doit être testé
                _, exec_time_i = mesurer_temps_execution(algo_I, S, k_fixed, capacites[:k_fixed])
                if exec_time_i > 60:
                    print(f"Algo I a dépassé 60s pour d={d}, S={S}, k={k_fixed}")
                    break
            else:
                exec_time_i = None

            _, exec_time_ii = mesurer_temps_execution(algo_II, S, k_fixed, capacites[:k_fixed])
            _, exec_time_iii = mesurer_temps_execution(algo_III, S, k_fixed, capacites[:k_fixed])

            resultats_S[d]["S_values"].append(S)
            resultats_S[d]["temps_algo_i_S"].append(exec_time_i if TEST_ALGO_I else float("nan"))
            resultats_S[d]["temps_algo_ii_S"].append(exec_time_ii)
            resultats_S[d]["temps_algo_iii_S"].append(exec_time_iii)

        # Étude du temps en fonction de k
        S_fixed = 500000  # Fixer \( S \) pour cette étude
        for k in [1, 5, 10, 15, 20, 25, 30]:
            print(f"Test pour d={d}, S={S_fixed}, k={k}")

            if TEST_ALGO_I:
                _, exec_time_i = mesurer_temps_execution(algo_I, S_fixed, k, capacites[:k])
                if exec_time_i > 60:
                    print(f"Algo I a dépassé 60s pour d={d}, S={S_fixed}, k={k}")
                    break
            else:
                exec_time_i = None

            _, exec_time_ii = mesurer_temps_execution(algo_II, S_fixed, k, capacites[:k])
            _, exec_time_iii = mesurer_temps_execution(algo_III, S_fixed, k, capacites[:k])

            resultats_k[d]["k_values"].append(k)
            resultats_k[d]["temps_algo_i_k"].append(exec_time_i if TEST_ALGO_I else float("nan"))
            resultats_k[d]["temps_algo_ii_k"].append(exec_time_ii)
            resultats_k[d]["temps_algo_iii_k"].append(exec_time_iii)

    # Génération des graphiques
    for d in [2, 3, 4]:
        # Graphique pour \( S \)
        plt.figure(figsize=(10, 6))
        if TEST_ALGO_I:
            plt.plot(resultats_S[d]["S_values"], resultats_S[d]["temps_algo_i_S"], label="Algo I (Récursif)", color='g')
        plt.plot(resultats_S[d]["S_values"], resultats_S[d]["temps_algo_ii_S"], label="Algo II (Dynamique)", color='b')
        plt.plot(resultats_S[d]["S_values"], resultats_S[d]["temps_algo_iii_S"], label="Algo III (Glouton)", color='r')
        plt.xlabel("Quantité de confiture (S)")
        plt.ylabel("Temps d'exécution (secondes)")
        plt.title(f"Temps d'exécution en fonction de S (k={k_fixed}, d={d})")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"temps_vs_S_d{d}.png")
        plt.show()

        # Graphique pour \( k \)
        plt.figure(figsize=(10, 6))
        if TEST_ALGO_I:
            plt.plot(resultats_k[d]["k_values"], resultats_k[d]["temps_algo_i_k"], label="Algo I (Récursif)", color='g')
        plt.plot(resultats_k[d]["k_values"], resultats_k[d]["temps_algo_ii_k"], label="Algo II (Dynamique)", color='b')
        plt.plot(resultats_k[d]["k_values"], resultats_k[d]["temps_algo_iii_k"], label="Algo III (Glouton)", color='r')
        plt.xlabel("Nombre de types de bocaux (k)")
        plt.ylabel("Temps d'exécution (secondes)")
        plt.title(f"Temps d'exécution en fonction de k (S={S_fixed}, d={d})")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"temps_vs_k_d{d}.png")
        plt.show()



def generer_systeme_capacites(k, pmax):
    """
    Génère un système de capacités avec k types de bocaux.
    Toujours inclut 1 et trie les capacités par ordre croissant.
    """
    if k == 1:
        return [1]  # Si un seul type, on retourne juste 1
    capacites = [1] + random.sample(range(2, pmax + 1), k - 1)
    capacites.sort()
    return capacites



def tester_glouton_ecart(k, pmax, n_tests):
    """
    Teste la compatibilité glouton et calcule les écarts relatifs pour n_tests.
    """
    resultats = {
        "glouton_compatibles": 0,
        "non_glouton_compatibles": 0,
        "ecarts_relatifs": []
    }

    for _ in range(n_tests):
        # Génération aléatoire d'un système de capacités
        V = generer_systeme_capacites(k, pmax)
        S = random.randint(1, sum(V))  # Générer une quantité aléatoire

        # Tester la compatibilité glouton
        compatible = test_glouton_compatible(k, V)
        if compatible:
            resultats["glouton_compatibles"] += 1
        else:
            resultats["non_glouton_compatibles"] += 1
            # Calculer l'écart relatif pour un système non compatible
            opt, _ = algo_II(S, k, V)
            glouton = algo_III(S, k, V)
            if opt != float('inf') and glouton != float('inf'):
                ecart_relatif = (glouton - opt) / opt
                resultats["ecarts_relatifs"].append(ecart_relatif)

    return resultats



def analyser_resultats(resultats):
    """
    Affiche les résultats de l'analyse des systèmes de capacités,
    en différenciant les cas en fonction du type de résultat (avec ou sans pire_ecart).
    """
    total = resultats["glouton_compatibles"] + resultats["non_glouton_compatibles"]
    freq_glouton = resultats["glouton_compatibles"] / total * 100
    freq_non_glouton = resultats["non_glouton_compatibles"] / total * 100

    print(f"Compatibilité glouton : {freq_glouton:.2f}%")
    print(f"Non compatibilité glouton : {freq_non_glouton:.2f}%")

    if resultats["ecarts_relatifs"]:
        ecart_moyen = sum(resultats["ecarts_relatifs"]) / len(resultats["ecarts_relatifs"])
        print(f"Écart relatif moyen : {ecart_moyen:.4f}")
        
        if "pire_ecart" in resultats:  # Cas de tester_glouton_ecart_f
            ecart_max = resultats["pire_ecart"]
            print(f"Écart relatif maximal : {ecart_max:.4f}")
        else:  # Cas de tester_glouton_ecart
            ecart_max = max(resultats["ecarts_relatifs"])
            print(f"Écart relatif maximal : {ecart_max:.4f}")
    else:
        print("Aucun écart relatif calculé (aucun système non glouton-compatible testé avec succès).")



def tester_glouton_ecart_f(k, pmax, f, n_tests):
    """
    Teste la compatibilité glouton et calcule les écarts relatifs pour n_tests,
    en évaluant toutes les valeurs S entre pmax et f*pmax pour les systèmes non glouton-compatibles.
    """
    resultats = {
        "glouton_compatibles": 0,
        "non_glouton_compatibles": 0,
        "ecarts_relatifs": [],
        "pire_ecart": -float('inf'),
    }

    for _ in range(n_tests):
        # Génération aléatoire d'un système de capacités
        V = generer_systeme_capacites(k, pmax)
        
        # Tester la compatibilité glouton
        compatible = test_glouton_compatible(k, V)
        if compatible:
            resultats["glouton_compatibles"] += 1
        else:
            resultats["non_glouton_compatibles"] += 1
            # Tester sur toutes les valeurs de S entre pmax et f*pmax
            pire_ecart = -float('inf')
            for S in range(pmax, f * pmax + 1):
                opt, _ = algo_II(S, k, V)  # Solution optimale
                glouton = algo_III(S, k, V)  # Solution gloutonne
                if opt != float('inf') and glouton != float('inf'):
                    ecart_relatif = (glouton - opt) / opt  # Calcul de l'écart relatif
                    resultats["ecarts_relatifs"].append(ecart_relatif)
                    pire_ecart = max(pire_ecart, ecart_relatif)
            
            # Enregistrer le pire écart
            resultats["pire_ecart"] = max(resultats["pire_ecart"], pire_ecart)

    return resultats



def statistiques_glouton(k, pmax, f, n_tests):
    """
    Regroupe les tests de compatibilité glouton et analyse les résultats pour les deux approches :
    - Test classique avec une seule valeur de S aléatoire
    - Test avec un intervalle étendu de S (tester_glouton_ecart_f)
    
    Arguments :
    - k : nombre de types de bocaux
    - pmax : capacité maximale des bocaux
    - f : facteur multiplicatif pour étendre l'intervalle de S
    - n_tests : nombre de tests aléatoires à effectuer
    """
    # Tester les systèmes de capacités avec une seule valeur S aléatoire
    print("=== Résultats pour tester_glouton_ecart ===")
    resultats = tester_glouton_ecart(k, pmax, n_tests)
    analyser_resultats(resultats)

    # Tester les systèmes de capacités avec un intervalle étendu de S
    print("\n=== Résultats pour tester_glouton_ecart_f ===")
    resultats_f = tester_glouton_ecart_f(k, pmax, f, n_tests)
    analyser_resultats(resultats_f)



# Pour tester soi-même des valeurs avec le fichier data.txt
#test()


# Appeler la fonction de test pour générer les données
#test_et_generer_graphiques() # ATTENTION : régler TEST_ALGO_I avant de lancer le programme


# Pour tester des proportions d'algorithmes glouton-compatibles
#statistiques_glouton(10, 100, 3, 100)