import os
from collections import deque
import heapq

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


def gale_shapley_optimise(CE, CP, capacites):
    n = len(CE)
    m = len(CP)

    # Étape 1 : Prétraitement optimisé

    # 1. File des étudiants libres
    etudiants_libres = deque(range(n))  # O(1) pour ajout/retrait
    
    # 2. Suivi des propositions des étudiants
    prochain_parcours = [0] * n  # O(1) pour accès et incrément

    # 3. Classement des étudiants pour chaque parcours
    classement_parcours = [{etudiant: rang for rang, etudiant in enumerate(CP[j])} for j in range(m)]

    # 4. Affectations sous forme de heaps pour un accès rapide à l'étudiant le moins préféré
    affectations = {j: [] for j in range(m)}  # Chaque parcours a un heap
    set_affectations = {j: set() for j in range(m)}  # Vérification rapide de la présence

    # 5. Capacité restante
    capacite_restante = capacites[:]

    # Algorithme optimisé
    while etudiants_libres:
        i = etudiants_libres.popleft()  # O(1)

        while prochain_parcours[i] < m:
            j = CE[i][prochain_parcours[i]]  # O(1)
            prochain_parcours[i] += 1

            # Si le parcours a de la place
            if capacite_restante[j] > 0:
                heapq.heappush(affectations[j], (-classement_parcours[j][i], i))  # O(log k)
                set_affectations[j].add(i)
                capacite_restante[j] -= 1
                break

            # Si le parcours est plein, vérifier si l'étudiant est mieux classé
            moins_prefere_rang, moins_prefere = max(affectations[j])  # O(1) car heap inversé
            if classement_parcours[j][i] < -moins_prefere_rang:
                # Remplacement
                affectations[j].remove((moins_prefere_rang, moins_prefere))  # O(log k)
                heapq.heapify(affectations[j])  # Maintenir la propriété du heap

                heapq.heappush(affectations[j], (-classement_parcours[j][i], i))  # O(log k)
                set_affectations[j].remove(moins_prefere)
                set_affectations[j].add(i)

                etudiants_libres.append(moins_prefere)  # O(1)
                break

    # Transformation du résultat pour une lecture facile
    result = {j: [etudiant for _, etudiant in affectations[j]] for j in range(m)}
    return result



CE = lire_pref_etudiants("PrefEtu.txt")
CP, capacites = lire_pref_parcours("PrefSpe.txt")

# Affichage des matrices CE et CP pour vérifier leur contenu
print("\nMatrice CE (préférences des étudiants) :")
for i, row in enumerate(CE):
    print(f"{i}: {row}")

print("\nMatrice CP (préférences des parcours) :")
for i, row in enumerate(CP):
    print(f"{i}: {row}")

# Exécution de l'algorithme
affectations = gale_shapley_optimise(CE, CP, capacites)

# Affichage du résultat
print("\nAffectations finales :")
for parcours, etudiants in affectations.items():
    print(f"Parcours {parcours}: {etudiants}")
