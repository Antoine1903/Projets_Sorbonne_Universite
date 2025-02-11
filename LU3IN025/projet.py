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

    etudiants_libres = deque(range(n))  # File des étudiants libres
    prochain_parcours = [0] * n  # Indice du prochain parcours que chaque étudiant va proposer
    classement_parcours = [{etudiant: rang for rang, etudiant in enumerate(CP[j])} for j in range(m)]  # Classement des étudiants pour chaque parcours
    affectations = {j: [] for j in range(m)}  # Affectations des parcours
    capacite_restante = capacites[:]  # Capacités restantes pour chaque parcours

    while etudiants_libres:
        i = etudiants_libres.popleft()  # Récupérer un étudiant libre

        while prochain_parcours[i] < m:
            j = CE[i][prochain_parcours[i]]  # Le prochain parcours à proposer
            prochain_parcours[i] += 1

            # Si le parcours a de la capacité, on l'ajoute directement
            if capacite_restante[j] > 0:
                heapq.heappush(affectations[j], (-classement_parcours[j][i], i))  # Ajouter l'étudiant avec son rang inversé
                capacite_restante[j] -= 1  # Réduire la capacité restante
                break
            else:
                # Si le parcours est plein, on vérifie l'étudiant le moins préféré
                # Récupérer l'étudiant le moins préféré (le premier dans le heap)
                moins_prefere_rang, moins_prefere = affectations[j][0]
                
                # Si l'étudiant i est plus préféré que l'étudiant moins préféré, on remplace
                if classement_parcours[j][i] < -moins_prefere_rang:
                    heapq.heappop(affectations[j])  # Enlever l'étudiant le moins préféré
                    etudiants_libres.append(moins_prefere)  # Remettre l'étudiant moins préféré dans la file des libres
                    # Ajouter le nouvel étudiant dans le parcours
                    heapq.heappush(affectations[j], (-classement_parcours[j][i], i))
                    break

    # Formatage des résultats : on trie les étudiants affectés à chaque parcours
    result = {j: [etudiant for _, etudiant in sorted(affectations[j])] for j in range(m)}
    return result


def gale_shapley_parcours(CE, CP, capacites):
    n = len(CE)  # Nombre d'étudiants
    m = len(CP)  # Nombre de parcours

    parcours_libres = deque(range(m))  # Tous les parcours sont initialement libres
    capacite_restante = capacites[:]  # Capacités restantes
    etudiant_affecte = [-1] * n  # Affectation actuelle des étudiants
    classement_etudiants = [{parcours: rang for rang, parcours in enumerate(CE[i])} for i in range(n)]  # Classement des parcours pour chaque étudiant
    affectations = {j: [] for j in range(m)}  # Étudiants affectés dans chaque parcours

    while parcours_libres:
        parcours = parcours_libres.popleft()  # Prendre un parcours libre

        while capacite_restante[parcours] > 0 and CP[parcours]:
            etudiant = CP[parcours].pop(0)  # Étudiant préféré suivant

            if etudiant_affecte[etudiant] == -1:  # Étudiant libre, pas encore affecté
                etudiant_affecte[etudiant] = parcours
                affectations[parcours].append(etudiant)
                capacite_restante[parcours] -= 1
            else:  # L'étudiant est déjà affecté ailleurs
                ancien_parcours = etudiant_affecte[etudiant]

                # Vérifier si ce parcours est mieux classé pour l'étudiant
                if classement_etudiants[etudiant][parcours] < classement_etudiants[etudiant][ancien_parcours]:
                    affectations[ancien_parcours].remove(etudiant)
                    capacite_restante[ancien_parcours] += 1
                    affectations[parcours].append(etudiant)
                    capacite_restante[parcours] -= 1
                    etudiant_affecte[etudiant] = parcours

                    if capacite_restante[ancien_parcours] > 0:
                        parcours_libres.append(ancien_parcours)

        if capacite_restante[parcours] > 0:
            parcours_libres.append(parcours)

    return affectations


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
            for autre_parcours in CE[etudiant]:
                if autre_parcours != parcours:
                    # Vérifier que l'autre parcours préfère cet étudiant à certains de ses étudiants actuels
                    for etudiant_autre_parcours in affectation.get(autre_parcours, []):
                        if etudiant in CP[autre_parcours] and etudiant_autre_parcours in CP[autre_parcours]:
                            if (CE[etudiant].index(autre_parcours) < CE[etudiant].index(parcours)) and \
                            (CP[autre_parcours].index(etudiant) < CP[autre_parcours].index(etudiant_autre_parcours)):
                                paires_instables.append((etudiant, autre_parcours))  # Ajouter la paire instable


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


def generate_lp_file_k(n, preferences, capacities, k, filename="problem.lp"):
    """
    Génère un fichier .lp correspondant au PLNE assurant qu'un étudiant obtient un de ses k premiers choix.
    
    :param n: Nombre d'étudiants
    :param preferences: Dictionnaire des préférences des étudiants (clé: étudiant, valeur: liste de parcours classés)
    :param capacities: Liste des capacités des parcours
    :param k: Nombre maximum de choix considérés pour chaque étudiant
    :param filename: Nom du fichier LP généré
    """
    with open(filename, "w") as f:
        f.write("\* PLNE - Affectation avec contrainte sur k premiers choix *\n")
        f.write("Minimize\n")
        f.write(" obj: 0\n")  # Pas d'objectif, on cherche la faisabilité
        f.write("Subject To\n")
        
        # Contraintes d'affectation unique pour chaque étudiant
        for i in range(n):
            f.write(f" c_assign_{i}: " + " + ".join([f"x_{i}_{j}" for j in preferences[i][:k]]) + " = 1\n")
        
        # Contraintes de capacité des parcours
        num_parcours = len(capacities)
        for j in range(num_parcours):
            f.write(f" c_capacity_{j}: " + " + ".join([f"x_{i}_{j}" for i in range(n) if j in preferences[i][:k]]) + f" <= {capacities[j]}\n")
        
        # Déclaration des variables binaires
        f.write("Binary\n")
        for i in range(n):
            for j in preferences[i][:k]:
                f.write(f" x_{i}_{j}\n")
        
        f.write("End\n")

def main():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Charger les préférences et exécuter Gale-Shapley (Donnee deviens de Fichers PrefEtu.txt et PrefSpe.txt)")
        print("2. Générer des préférences aléatoires et afficher les matrices et tracer le graphe")
        print("3. Générer un fichier LP pour l'affectation (n = 3,Donnee deviens de Fichers PrefEtu.txt et PrefSpe.txt)")
        print("4. Quitter")
        
        choix = input("Votre choix : ")

        if choix == "1":
            # Charger les préférences depuis les fichiers
            CE = lire_pref_etudiants("PrefEtu.txt")
            CP, capacites = lire_pref_parcours("PrefSpe.txt")

            # Exécuter les algorithmes Gale-Shapley
            affectations_etudiants = gale_shapley_etudiants(CE, CP, capacites)
            affectations_parcours = gale_shapley_parcours(CE, CP, capacites)

            # Vérifier la stabilité
            print("\nVérification de la stabilité de l'affectation (étudiants):")
            afficher_paires_instables(trouver_paires_instables(CE, CP, affectations_etudiants))
            
            print("\nVérification de la stabilité de l'affectation (parcours):")
            afficher_paires_instables(trouver_paires_instables(CE, CP, affectations_parcours))

            # Afficher les résultats finaux
            afficher_affectations_etudiants("Affectations finales (Côté étudiants)", affectations_etudiants)
            afficher_affectations_parcours("Affectations finales (Côté parcours)", affectations_parcours)
        
        elif choix == "2":
            # Générer des préférences aléatoires
            n = int(input("Entrez le nombre d'étudiants : "))
            CE = generer_pref_etudiants(n)
            CP = generer_pref_parcours(n)

            # Afficher les matrices générées
            afficher_matrice("Matrice CE (Préférences des étudiants) :", CE, "Etudiant ")
            afficher_matrice("Matrice CP (Préférences des parcours) :", CP, "Parcours ")

            tracer_courbes()
        
        elif choix == "3":
            # Générer un fichier LP pour l'affectation
            n = 11
            preferences = lire_pref_etudiants("PrefEtu.txt")
            _, capacities = lire_pref_parcours("PrefSpe.txt")
            k = int(input("Entrez la valeur de k : "))
            generate_lp_file_k(n, preferences, capacities, k, "affectation_k.lp")
            print("Fichier LP généré : affectation_k.lp")
        
        elif choix == "4":
            print("Au revoir !")
            break
        
        else:
            print("Choix invalide, veuillez réessayer.")

main()
