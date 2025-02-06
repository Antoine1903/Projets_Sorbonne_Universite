Yuxiang Zhang & Antoine Lecomte

TME - semaines 1 à 3

Question 2 :
Nous avons différentes possibilités pour optimiser les performances de l'algorithme
de Gale-Shapley en ce qui concerne les structures de données :

nous utilisons plusieurs structures de données qui ont chacune des avantages pour les optimisations que nous cherchons à effectuer.

Structure deque (liste doublement chaînée qui dispose des fonctions d'ajout/suppression en tête/queue appendleft, popleft, append, pop): pour trouver un étudiant libre à chaque itération. Les étudiants sont récupérés dans l'ordre de leur numéro. Complexité constante O(1).

Structure liste de python, de complexité O(1) pour trouver le prochain parcours préféré par l'étudiant.

Structure liste de dictionnaires de Python, où chaque dictionnaire comporte 11 associations (11 étudiants), les clés sont les numéros des étudiants et les valeurs sont leur classement (qui démarre à 0 pour l'étudiant classé en tête). Il y a 9 dictionnaires dans la liste car chaque dictionnaire représente le classement sur un Master.

Structure de heap inversé, on utilise heapq en Python (file de priorité minimale), ce qui donne une complexité en O(1) pour trouver l'étudiant classé en dernière position, car celui-ci est en tête du heapq.

Structures heap inversé + ensemble (set, non ordonné) pour remplacer un étudiant par un autre dans l’affectation courante d’un parcours qui est de complexité O(log k) pour l'ajout et la suppression d'un étudiant. La structure de l'ensemble permet de vérifier directement la présence d'un étudiant en O(1).