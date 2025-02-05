import os
from collections import deque

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



def gale_shapley_hopitaux(CE, CP, capacites):
    n = len(CE)  # Nombre d'étudiants
    m = len(CP)  # Nombre de parcours

    # Étape 1 : Prétraitement pour accélérer les opérations

    # 1. File des étudiants libres
    etudiants_libres = deque(range(n))

    # 2. Suivi des propositions des étudiants
    prochain_parcours = [0] * n  # Index du prochain parcours à qui proposer

    # 3. Dictionnaire pour retrouver rapidement le rang d’un étudiant dans un parcours
    classement_parcours = [{etudiant: rang for rang, etudiant in enumerate(CP[j])} for j in range(m)]

    # 4. Liste des étudiants actuellement affectés à chaque parcours
    affectations = {j: [] for j in range(m)}

    # 5. Capacité restante pour chaque parcours
    capacite_restante = capacites[:]

    # Étape 2 : Algorithme de Gale-Shapley

    while etudiants_libres:
        i = etudiants_libres.popleft()  # Étudiant libre
        while prochain_parcours[i] < m:
            j = CE[i][prochain_parcours[i]]  # Parcours préféré suivant
            prochain_parcours[i] += 1  # Passer au suivant pour la prochaine itération

            # 1. Si le parcours a de la place, on affecte directement
            if capacite_restante[j] > 0:
                affectations[j].append(i)
                capacite_restante[j] -= 1
                break

            # 2. Si le parcours est plein, vérifier si i est mieux classé qu’un étudiant actuel
            moins_prefere = max(affectations[j], key=lambda x: classement_parcours[j][x])
            if classement_parcours[j][i] < classement_parcours[j][moins_prefere]:
                affectations[j].remove(moins_prefere)
                affectations[j].append(i)
                etudiants_libres.append(moins_prefere)  # L'ancien étudiant devient libre
                break

    return affectations


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
affectations = gale_shapley_hopitaux(CE, CP, capacites)

# Affichage du résultat
print("\nAffectations finales :")
for parcours, etudiants in affectations.items():
    print(f"Parcours {parcours}: {etudiants}")
