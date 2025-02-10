from collections import deque
import heapq
import random
import time
import matplotlib.pyplot as plt
import numpy as np

def lire_pref_etudiants(fichier):
    with open(fichier, "r") as f:
        lignes = f.readlines()
    
    CE = []
    
    for ligne in lignes[1:]:  # On saute la première ligne (nombre d'étudiants)
        _, _, *preferences = ligne.strip().split()  # On ignore l'ID et le nom
        CE.append(list(map(int, preferences)))  # Conversion en liste d'entiers
    
    return CE


def lire_pref_parcours(fichier):
    with open(fichier, "r") as f:
        lignes = f.readlines()
    
    capacites = list(map(int, lignes[1].strip().split()[1:]))  # On ignore "Cap"
    
    CP = []
    
    for ligne in lignes[2:]:  # On saute les deux premières lignes (NbEtu et Cap)
        _, _, *preferences = ligne.strip().split()  # On ignore l'ID et le nom du parcours
        CP.append(list(map(int, preferences)))  # Conversion en liste d'entiers
    
    return CP, capacites


def gale_shapley_etudiants(CE, CP, capacites):
    n = len(CE)  # Nombre d'étudiants
    m = len(CP)  # Nombre de parcours

    # Étape 1 : Prétraitement optimisé

    # 1. File des étudiants libres
    etudiants_libres = deque(range(n))  # O(n) en espace, O(1) pour ajout/retrait

    # 2. Suivi des propositions des étudiants
    prochain_parcours = [0] * n  # O(n) en espace, O(1) pour accès et incrément

    # 3. Classement des étudiants pour chaque parcours
    # Espace : O(m * n) car chaque parcours classe tous les étudiants
    classement_parcours = [{etudiant: rang for rang, etudiant in enumerate(CP[j])} for j in range(m)]  # O(m * n) en temps et espace

    # 4. Affectations sous forme de heaps pour un accès rapide à l'étudiant le moins préféré
    affectations = {j: [] for j in range(m)}  # O(m) en espace pour les heaps
    set_affectations = {j: set() for j in range(m)}  # O(m) en espace pour la vérification rapide de présence

    # 5. Capacité restante
    capacite_restante = capacites[:]  # O(m) en espace

    # Algorithme optimisé
    while etudiants_libres:  # Chaque étudiant propose au plus à tous les parcours, donc au total O(n * m)
        i = etudiants_libres.popleft()  # O(1)

        while prochain_parcours[i] < m:  # Chaque étudiant fait au plus m propositions
            j = CE[i][prochain_parcours[i]]  # O(1) pour accéder au parcours préféré suivant
            prochain_parcours[i] += 1  # O(1)

            # Si le parcours a de la place
            if capacite_restante[j] > 0:
                heapq.heappush(affectations[j], (-classement_parcours[j][i], i))  # O(log k), k = nombre d'affectés dans le parcours
                set_affectations[j].add(i)  # O(1)
                capacite_restante[j] -= 1  # O(1)
                break  # Étudiant affecté, on passe au suivant

            # Si le parcours est plein, vérifier si l'étudiant est mieux classé
            moins_prefere_rang, moins_prefere = max(affectations[j])  # O(1) car heap inversé, max est en tête
            if classement_parcours[j][i] < -moins_prefere_rang:
                # Remplacement
                affectations[j].remove((moins_prefere_rang, moins_prefere))  # O(log k) pour la suppression dans le heap
                heapq.heapify(affectations[j])  # O(k) pour rétablir la propriété de heap après suppression

                heapq.heappush(affectations[j], (-classement_parcours[j][i], i))  # O(log k) pour ajouter le nouvel étudiant
                set_affectations[j].remove(moins_prefere)  # O(1)
                set_affectations[j].add(i)  # O(1)

                etudiants_libres.append(moins_prefere)  # O(1), l'étudiant remplacé redevient libre
                break  # Étudiant affecté, on passe au suivant

    # Transformation du résultat pour une lecture facile
    # O(m * k) où k est le nombre d'étudiants affectés par parcours
    result = {j: [etudiant for _, etudiant in affectations[j]] for j in range(m)}  
    return result


def gale_shapley_parcours(CE, CP, capacites):
    n = len(CE)  # Nombre d'étudiants, O(1)
    m = len(CP)  # Nombre de parcours, O(1)

    # 1. File des étudiants libres
    etudiants_libres = deque(range(n))  # O(n) en espace, O(1) pour ajout/retrait

    # 2. Capacités restantes des parcours
    capacite_restante = capacites[:]  # O(m) en espace

    # 3. Dictionnaire pour suivre l'affectation des étudiants
    etudiant_affecte = {}  # O(n) en espace pour stocker l'affectation des étudiants

    # 4. Classement des étudiants pour chaque parcours
    # O(m * n) en espace et en temps pour construire ce classement
    classement_parcours = [{etudiant: rang for rang, etudiant in enumerate(CP[j])} for j in range(m)]  # O(m * n) en temps et espace

    # 5. Heaps pour gérer les étudiants affectés dans chaque parcours
    affectations = {j: [] for j in range(m)}  # O(m) en espace pour les heaps

    # 6. Processus de Gale-Shapley pour l'affectation
    while etudiants_libres:  # Chaque étudiant propose au plus à tous les parcours, donc au total O(n * m)
        i = etudiants_libres.popleft()  # O(1)

        while True:
            # L'étudiant propose au parcours préféré qu'il n'a pas encore proposé
            parcours = CE[i][0]  # O(1) pour accéder au parcours préféré suivant
            CE[i].pop(0)  # O(m) pour supprimer le parcours de la liste des préférences de l'étudiant
            
            # Si le parcours a de la place
            if capacite_restante[parcours] > 0:
                # Affecter l'étudiant au parcours
                affectations[parcours].append(i)  # O(1) pour ajouter l'étudiant dans la liste du parcours
                capacite_restante[parcours] -= 1  # O(1) pour décrémenter la capacité
                etudiant_affecte[i] = parcours  # O(1) pour l'affectation
                break  # Étudiant affecté, on passe au suivant

            # Si le parcours est plein, vérifier si l'étudiant est mieux classé que le plus bas dans la pile
            worst_student = min(affectations[parcours], key=lambda student: classement_parcours[parcours][student])  # O(k) où k est le nombre d'étudiants affectés
            if classement_parcours[parcours][i] < classement_parcours[parcours][worst_student]:
                # Remplacer le pire étudiant par l'étudiant i
                affectations[parcours].remove(worst_student)  # O(k) pour la suppression
                capacite_restante[parcours] += 1  # O(1) pour libérer une place
                affectations[parcours].append(i)  # O(1) pour ajouter l'étudiant
                capacite_restante[parcours] -= 1  # O(1) pour réduire la capacité
                etudiant_affecte[i] = parcours  # O(1) pour l'affectation

                # L'étudiant expulsé devient libre et peut proposer à d'autres parcours
                etudiants_libres.append(worst_student)  # O(1)
                break  # Étudiant affecté, on passe au suivant

    # 7. Résultats finaux
    result = {j: affectations[j] for j in range(m) if affectations[j]}  # O(m * k) où k est le nombre d'étudiants affectés par parcours
    return result

# Q6
def trouver_paires_instables(CE, CP, affectation):
    """
    Trouve les paires instables dans l'affectation donnée.
    
    Une paire est instable si l'étudiant et le parcours préfèrent être ensemble
    plutôt qu'avec leur affectation actuelle.
    
    :param CE: Matrice des préférences des étudiants
    :param CP: Matrice des préférences des parcours
    :param affectation: Dictionnaire d'affectation des étudiants aux parcours
    :return: Liste des paires instables sous forme de tuples (étudiant, parcours)
    """
    paires_instables = []

    # Parcours chaque parcours pour examiner les étudiants affectés
    for parcours, etudiants in affectation.items():
        # Les étudiants actuellement affectés à ce parcours
        for etudiant in etudiants:
            # Vérifier si cette affectation est stable
            # 1. L'étudiant préfère un autre parcours à celui auquel il est affecté
            for i in range(len(CP[parcours])):
                etudiant_prefere = CP[parcours][i]  # Parcours préféré par l'étudiant
                
                # Vérifiez que l'étudiant n'est pas déjà affecté à ce parcours
                if etudiant_prefere != etudiant:
                    if parcours in CE[etudiant]:  # Vérifier que le parcours est dans les préférences de l'étudiant
                        if (CE[etudiant].index(parcours) < CE[etudiant].index(etudiant_prefere)) and (CP[parcours].index(etudiant) < CP[parcours].index(etudiant_prefere)):
                            paires_instables.append((etudiant, parcours))  # Ajouter la paire instable

    return paires_instables

def afficher_paires_instables(paires_instables):
    """
    Affiche les paires instables, ou un message si aucune paire instable n'est trouvée.
    
    :param paires_instables: Liste des paires instables sous forme de tuples (étudiant, parcours)
    """
    if paires_instables:
        print("Paires instables trouvées :")
        for etudiant, parcours in paires_instables:
            print(f"Étudiant {etudiant} préfère le parcours {parcours}.")
    else:
        print("Aucune paire instable trouvée. L'affectation est stable.")


# Partie 2: Evolution du temps de calcul
# Q7
def generer_pref_etudiants(n):
    """
    Génère une matrice de préférences des étudiants pour 9 parcours.
    Chaque étudiant a un ordre de préférence aléatoire pour les 9 parcours.
    
    :param n: Nombre d'étudiants
    :return: Matrice CE (liste de listes)
    """
    nb_parcours = 9
    CE = [random.sample(range(nb_parcours), nb_parcours) for _ in range(n)]
    return CE


def generer_pref_parcours(n):
    """
    Génère une matrice de préférences des 9 parcours pour les étudiants.
    Chaque parcours a un ordre de préférence aléatoire pour les n étudiants.
    
    :param n: Nombre d'étudiants
    :return: Matrice CP (liste de listes)
    """
    nb_parcours = 9
    CP = [random.sample(range(n), n) for _ in range(nb_parcours)]
    return CP


# Fonctions pour affichage
def afficher_matrice(titre, matrice, prefixe_ligne=""):
    print(titre)
    for i, ligne in enumerate(matrice):
        print(f"{prefixe_ligne}{i}: {ligne}")
    print("\n")


def afficher_affectations_etudiants(titre, affectations):
    """ Affiche les affectations sous un format clair. """
    print(f"\n{titre}:")
    for parcours, etudiants in affectations.items():
        print(f"  Etudiants {etudiants}: {parcours}")


def afficher_affectations_parcours(titre, affectations):
    """ Affiche les affectations sous un format clair. """
    print(f"\n{titre}:")
    for parcours, etudiants in affectations.items():
        print(f"  Parcours {parcours}: {', '.join(map(str, etudiants))}")


def generer_capacites(n, nb_parcours=9):
    """
    Génère une liste de capacités équilibrées pour les parcours.
    La somme des capacités est égale à n.
    Le reste est réparti aléatoirement entre les parcours.
    """
    base_capacite = n // nb_parcours
    capacites = [base_capacite] * nb_parcours
    reste = n % nb_parcours

    # Sélectionner aléatoirement des indices pour distribuer le reste
    indices_aleatoires = random.sample(range(nb_parcours), reste)
    for i in indices_aleatoires:
        capacites[i] += 1

    return capacites


# Mesure du temps d'exécution des deux algorithmes
def mesurer_temps_gale_shapley(n, nb_tests=15):
    """
    Mesure le temps moyen d'exécution des algorithmes de Gale-Shapley côté étudiants et parcours pour une valeur donnée de n.
    """
    temps_etudiants = []
    temps_parcours = []

    for _ in range(nb_tests):
        CE = generer_pref_etudiants(n)
        CP = generer_pref_parcours(n)
        capacites = generer_capacites(n)

        # Mesurer le temps pour l'algorithme côté étudiants
        debut_etudiants = time.time()
        gale_shapley_etudiants(CE, CP, capacites)
        fin_etudiants = time.time()
        temps_etudiants.append(fin_etudiants - debut_etudiants)

        # Mesurer le temps pour l'algorithme côté parcours
        debut_parcours = time.time()
        gale_shapley_parcours(CE, CP, capacites)
        fin_parcours = time.time()
        temps_parcours.append(fin_parcours - debut_parcours)

    return np.mean(temps_etudiants), np.mean(temps_parcours)


# Q8
def tracer_courbes():
    """Générer les temps d'exécution pour différentes valeurs de n"""
    valeurs_n = range(200, 2001, 200)
    temps_moyens_etudiants = []
    temps_moyens_parcours = []

    for n in valeurs_n:
        temps_etudiants, temps_parcours = mesurer_temps_gale_shapley(n)
        temps_moyens_etudiants.append(temps_etudiants)
        temps_moyens_parcours.append(temps_parcours)

    # Tracer la courbe
    plt.figure(figsize=(10, 6))
    plt.plot(valeurs_n, temps_moyens_etudiants, label='Gale-Shapley (Étudiants)', color='b', marker='o')
    plt.plot(valeurs_n, temps_moyens_parcours, label='Gale-Shapley (Parcours)', color='g', marker='o')
    plt.xlabel('Nombre d\'étudiants (n)')
    plt.ylabel('Temps moyen d\'exécution (secondes)')
    plt.title('Temps d\'exécution des algorithmes de Gale-Shapley')
    plt.legend()
    plt.grid(True)
    plt.show()


# Exemple d'utilisation dans le contexte du programme
def main():
    # Lecture des préférences
    CE = lire_pref_etudiants("PrefEtu.txt")
    CP, capacites = lire_pref_parcours("PrefSpe.txt")

    # Exécution des algorithmes
    affectations_etudiants = gale_shapley_etudiants(CE, CP, capacites)
    affectations_parcours = gale_shapley_parcours(CE, CP, capacites)

    # Vérification de la stabilité de l'affectation
    print("\nVérification de la stabilité de l'affectation (étudiants):")
    afficher_paires_instables(trouver_paires_instables(CE, CP, affectations_etudiants))
    
    print("\nVérification de la stabilité de l'affectation (parcours):")
    afficher_paires_instables(trouver_paires_instables(CE, CP, affectations_parcours))

    # Affichage des résultats finaux
    afficher_affectations_etudiants("Affectations finales (Côté étudiants)", affectations_etudiants)
    afficher_affectations_parcours("Affectations finales (Côté parcours)", affectations_parcours)
    print('\n')

    # Q7
    n = 11
    CE = generer_pref_etudiants(n)
    CP = generer_pref_parcours(n)

    # Affichage des matrices générées
    afficher_matrice("Matrice CE (Préférences des étudiants) :", CE, "Etudiant ")
    afficher_matrice("Matrice CP (Préférences des parcours) :", CP, "Parcours ")


# Programme principal
main()

# Exécuter le tracé
tracer_courbes()
