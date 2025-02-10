Yuxiang Zhang & Antoine Lecomte & Warsame Ismail

TME - semaines 1 à 3


Question 2 :

Nous avons différentes possibilités pour optimiser les performances de l'algorithme
de Gale-Shapley en ce qui concerne les structures de données :

Nous utilisons plusieurs structures de données qui ont chacune des avantages pour les
optimisations que nous cherchons à effectuer.

Structure deque (liste doublement chaînée qui dispose des fonctions d'ajout/suppression
en tête/queue appendleft, popleft, append, pop): pour trouver un étudiant libre à
chaque itération. Les étudiants sont récupérés dans l'ordre de leur numéro. Complexité
constante O(1).

Structure liste de python, de complexité O(1) pour trouver le prochain parcours préféré
par l'étudiant.

Structure liste de dictionnaires de Python, où chaque dictionnaire comporte 11
associations (11 étudiants), les clés sont les numéros des étudiants et les valeurs
sont leur classement (qui démarre à 0 pour l'étudiant classé en tête). Il y a 9
dictionnaires dans la liste car chaque dictionnaire représente le classement sur un
Master.

Structure de heap inversé, on utilise heapq en Python (file de priorité minimale),
ce qui donne une complexité en O(1) pour trouver l'étudiant classé en dernière position
car celui-ci est en tête du heapq.

Structures heap inversé + ensemble (set, non ordonné) pour remplacer un étudiant par
un autre dans l’affectation courante d’un parcours qui est de complexité O(log k) pour
l'ajout et la suppression d'un étudiant. La structure de l'ensemble permet de vérifier
directement la présence d'un étudiant en O(1).


Question 3 :

Complexité temporelle globale :

Initialisation des files, tableaux et dictionnaires : O(m * n) pour le classement des étudiants.
Chaque étudiant fait au plus m propositions : O(n * m).
Chaque insertion ou suppression dans un heap a un coût O(log k), où k est la capacité maximale d'un parcours (= le nombre d'étudiants qu'il peut accepter).
Dans le pire des cas (tous les parcours sont pleins et nécessitent des réaffectations), la complexité est O(n * m * log k).

Complexité spatiale globale :

Classements des parcours : O(m * n), car chaque parcours classe tous les étudiants.
Affectations des étudiants : O(m * k), où k est la capacité maximale par parcours.
File des étudiants libres : O(n) et les suivis de propositions.


En résumé :

Complexité temporelle : O(n * m * log k).
Complexité spatiale : O(m * n + m * k + n), cela donne O(m * (n+k) + n), la complexité se simplifie en O(m * (n + k)), sauf si m est très petit, n serait significatif et cela donnerait O(n). Dans le cas général, on a n>k et donc la complexité spatiale est O(n * m).


Question 4 :

Voici kes structures de données utilisées pour l'optimisation des opérations de l'algorithme côté parcours :

Structure deque (liste doublement chaînée) qui est utilisée pour maintenir la file des étudiants libres. Elle permet d’ajouter et de retirer des étudiants efficacement. La complexité en temps pour ajouter ou retirer un élément en tête ou en queue est O(1), ce qui permet de gérer la file des étudiants libres de manière optimale. En espace : O(n), où n est le nombre d'étudiants.

Structure liste (pour le classement des étudiants dans chaque parcours) qui est utilisée pour suivre les préférences des étudiants. Chaque étudiant propose son prochain parcours préféré à partir de cette liste. La complexité pour accéder à l'élément suivant dans la liste (le parcours préféré de l’étudiant) est O(1). Espace : O(m), où m est le nombre de parcours (car chaque étudiant a une liste de parcours).

Structure liste de dictionnaires (pour le classement des étudiants par parcours). Une liste de dictionnaires est utilisée pour représenter le classement des étudiants pour chaque parcours. Chaque dictionnaire contient un classement des étudiants, où la clé est l'ID de l'étudiant et la valeur est son rang dans le classement du parcours. Le classement est pré-calculé et permet de retrouver rapidement la position d’un étudiant dans le classement d’un parcours. Cette structure permet de déterminer le rang d’un étudiant en O(1).
Espace : O(m * n), où m est le nombre de parcours et n le nombre d’étudiants.

Structure heap inversé (utilisation de heapq) est utilisé pour gérer les étudiants affectés à chaque parcours. L'élément de tête du heapq est l’étudiant ayant le rang le plus bas (le moins préféré). L’utilisation d’un heap inversé permet de trouver l’étudiant classé en dernière position (le moins préféré) en O(1), car il est toujours situé à la racine du heap. Espace : O(k), où k est le nombre d’étudiants affectés à un parcours.

Structures heap inversé + ensemble (set) pour gérer les suppressions et réaffectations. Le heapq est utilisé pour gérer les étudiants affectés à chaque parcours, et l’ensemble est utilisé pour vérifier la présence d’un étudiant dans l’affectation d’un parcours avant de le remplacer. L’utilisation d’un heapq permet de gérer efficacement l’ajout et la suppression d’un étudiant en O(log k), où k est le nombre d’étudiants dans un parcours. L’ensemble permet de vérifier en O(1) si un étudiant est déjà affecté à un parcours.



Complexité temporelle globale :

Le classement des étudiants pour chaque parcours nécessite O(m * n) pour construire la liste de dictionnaires.
L'initialisation des deques et des heaps est O(n) et O(m), respectivement.
Chaque étudiant fait au plus m propositions (s’il n'est pas affecté directement). Chaque proposition nécessite la manipulation de listes et dictionnaires, avec une complexité O(1) pour la gestion des préférences et O(k) pour la gestion des expulsions avec le heap.
En cas de réaffectation d’un étudiant, le coût est O(log k) pour ajuster le heap.

Complexité totale (pire cas) :
Dans le pire des cas, chaque étudiant peut être réaffecté à plusieurs parcours, ce qui donne une complexité de O(n * m * log k), où n est le nombre d'étudiants, m est le nombre de parcours, et k est la capacité maximale d’un parcours.

Complexité spatiale globale :

Classements des parcours en O(m * n), car chaque parcours contient le classement de tous les étudiants.
Affectations des étudiants en O(m * k).
File des étudiants libres en O(n).
Heaps et ensembles en O(m * k) pour maintenir les heaps et les sets des étudiants affectés.

Complexité spatiale totale :
O(m * (n + k)), car les structures de données de classement, d'affectation et de gestion des étudiants affectés doivent être stockées.


En résumé :

Complexité temporelle : O(n * m * log k).
Complexité spatiale : O(m * (n + k)).


Question 5 :

Affectations finales (Côté étudiants):
  etudiants [3, 5]: 0
  etudiants [4]: 1
  etudiants [9]: 2
  etudiants [2]: 3
  etudiants [10]: 4
  etudiants [0]: 5
  etudiants [1]: 6
  etudiants [7]: 7
  etudiants [8, 6]: 8

Affectations finales (Côté parcours):
  Parcours 0: 5, 3
  Parcours 1: 4
  Parcours 2: 9
  Parcours 3: 2
  Parcours 4: 10
  Parcours 5: 0
  Parcours 6: 1
  Parcours 7: 7
  Parcours 8: 6, 8


Question 6 :

A l'exécution :

Vérification de la stabilité de l'affectation (étudiants):
Aucune paire instable trouvée. L'affectation est stable.

Vérification de la stabilité de l'affectation (parcours):
Aucune paire instable trouvée. L'affectation est stable.


Donc, nous obtenons à la fois deux résultats identiques (côté étudiant et côté parcours) et le test de vérification pour rechercher d'éventuelles paires instables échoue, ce qui confirme l'absence de paires instables et par la même occasion, la stabilité de l'affectation.


Question 9 :

La complexité temporelle observée semble cohérente avec l'analyse théorique des algorithmes de Gale-Shapley.