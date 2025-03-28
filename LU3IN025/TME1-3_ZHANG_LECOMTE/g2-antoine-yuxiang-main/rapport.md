# Rapport de Projet : Jeu des Restaurants

# Groupe
Yuxiang ZHANG
Antoine LECOMTE

## Introduction
Dans le cadre de ce projet, nous avons développé un jeu stratégique où des joueurs concurrents doivent choisir quotidiennement un restaurant pour maximiser leurs chances d'être servis. Le système intègre plusieurs stratégies d'IA et permet d'analyser leurs performances sur 50 journées simulées.

## Implémentation

### Architecture technique
- **Bibliothèques utilisées** : 
  - `pySpriteWorld` pour la visualisation
  - `search` pour les algorithmes de pathfinding
  - `matplotlib` pour l'analyse des résultats
- **Structure du code** :
  - Module `strategies.py` contenant les implémentations des stratégies
  - Script principal `main.py` gérant la simulation
  - Cartes personnalisées au format JSON

### Mécaniques clés
1. **Déplacement** : A* pour le chemin optimal
2. **Vision** : Champ de vision Manhattan (rayon=5)
3. **Coupe-files** : Priorité aléatoire avec objets ramassables
4. **Score** : Cumul quotidien avec capacités de restaurants

## Stratégies implémentées
### 1. Stratégie Têtue  
```python
def strategie_tetue(pos_restaurants, joueur_id, choix_initiaux):
    """Persiste sur le choix initial aléatoire du premier jour."""
    if joueur_id not in choix_initiaux:
        choix_initiaux[joueur_id] = random.choice(pos_restaurants)
    return choix_initiaux[joueur_id]
```
**Mécanique** :  
- **Verrouillage initial** : Attribution aléatoire d'un restaurant au premier jour  
- **Persistance absolue** : Même choix quotidien indépendamment des conditions  
- **Avantage** : Évite la compétition dynamique par rigidité  

---

### 2. Stratégie Stochastique  
```python
def strategie_stochastique(pos_restaurants, probabilites):
    """Choix probabiliste avec distribution paramétrable."""
    return random.choices(pos_restaurants, weights=probabilites, k=1)[0]
```
**Mécanique** :  
- **Pondération explicite** : Distribution contrôlée via `probabilites`  
- **Randomisation stratégique** : Permet d'éviter les schémas prévisibles  
- **Flexibilité** : Adaptable via ajustement des poids (ex: favoriser les restaurants peu fréquentés)  

---

### 3. Stratégie Greedy  
```python
def strategie_greedy(...):
    restaurants_tries = sorted(pos_restaurants, key=lambda r: distManhattan(...), reverse=True)
    ...
```
**Mécanique** :  
- **Priorité à l'éloignement** : Trie les restaurants par distance Manhattan décroissante  
- **Recalcul dynamique** :  
  - Vérifie en temps réel la capacité (`seuil`) et l'accessibilité (`temps_restant`)  
  - Met à jour les préférences via `preferences[joueur_id]`  
- **Système de repli** :  
  1. Restaurants sous le seuil dans le champ de vision  
  2. Restaurants accessibles en temps restant  
  3. Position actuelle en dernier recours  

---

### 4. Fictitious Play  
```python
def fictitious_play(...):
    least_visited_restaurants = [r for r, v in restaurant_visits.items() if v == min_visits]
    return random.choice(least_visited_restaurants)
```
**Mécanique** :  
- **Apprentissage bayésien** : Calcule les fréquences historiques des choix adverses  
- **Minimax fréquentiel** : Cible les restaurants les moins visités (min_visits)  
- **Anti-coordination** : Évite les stratégies majoritaires via l'historique global  

---

### 5. Regret Matching  
```python
def regret_matching(...):
    regrets = np.array([scores_hypothetiques[s] - score_total for s in range(num_actions)])
    probabilites = np.array([max(0, regret)/somme_regrets_positifs for regret in regrets])
```
**Mécanique** :  
- **Calcul de regret cumulatif** : Compare les gains réels vs hypothétiques  
- **Mise à jour adaptative** :  
  - Probabilités proportionnelles aux regrets positifs  
  - Randomisation uniforme si tous regrets ≤ 0  
- **Corrélation exploration/exploitation** : Balance historique récent et opportunités  

---

### 6. Stratégie d'Imitation  
```python
def strategie_imitation(...):
    meilleurs_joueurs = [j for j, score in historique_scores.items() if score == max_score]
    return historique_choix.get(random.choice(meilleurs_joueurs))
```
**Mécanique** :  
- **Sélection élitiste** : Identifie les joueurs avec `max_score`  
- **Mimétisme aveugle** : Copie le dernier choix des meilleurs sans analyse contextuelle  
- **Effet moutonnier** : Risque de saturation des restaurants "populaires"  

---

### 7. Stratégie Greedy Complexe  
```python
def strategie_greedy_complex(...):
    if nb_joueurs_current >= seuil or joueurs_arretes >= 2:
        preferences[joueur_id] = []
```
**Améliorations vs Greedy** :  
- **Détection de congestion** : Déclenche un recalcul si `seuil` dépassé  
- **Intelligence sociale** : Réévalue les choix si ≥2 joueurs immobilisés (`historique_choix_joueurs`)  
- **Optimisation temps-réel** : Combine distance, visibilité et comportements adverses  

---

### 8. Stratégie Séquence Fixe  
```python
def strategie_sequence_fixe(...):
    index_resto = (jour_actuel + joueur_id) % len(pos_restaurants_sorted)
```
**Mécanique** :  
- **Rotation déterministe** : Parcours cyclique des restaurants triés  
- **Décalage personnel** : Séquence unique par joueur via `joueur_id`  
- **Couverture équitable** : Garantit une répartition temporelle uniforme  

## Résultats

### Analyse comparative

## Stratégie Têtue vs Autres Stratégies (1 vs 7 joueurs)
![Comparaison 1 Têtue vs 7 Stochastique](./graphes/1Têtue_VS_7Stochastique.png)
Têtue (n=1) : 26.00 points
Stochastique (n=7) : 26.57 points

![Comparaison 1 Têtue vs 7 Greedy](./graphes/1Têtue_VS_7Greedy.png)
Têtue (n=1) : 28.00 points
Greedy (n=7) : 30.43 points

![Comparaison 1 Têtue vs 7 Fictitious Play](./graphes/1Têtue_VS_7FP.png)
Têtue (n=1) : 50.00 points
Fictitious Play (n=7) : 27.14 points

![Comparaison 1 Têtue vs 7 Regret Matching](./graphes/1Têtue_VS_7FP.png)
Têtue (n=1) : 50.00 points
Fictitious Play (n=7) : 27.14 points

![Comparaison 1 Têtue vs 7 Imitation](./graphes/1Têtue_VS_7Imitation.png)
Têtue (n=1) : 14.57 points
Imitation (n=7) : 13.00 points

![Comparaison 1 Têtue vs 7 Séquence Fixe](./graphes/1Têtue_VS_7SF.png)
Têtue (n=1) : 21.00 points
Séquence Fixe (n=7) : 32.71 points

## Stratégie Stochastique vs Autres Stratégies (1 vs 7 joueurs)
![Comparaison 1 Stochastique vs 7 Têtue](./graphes/1Stochastique_VS_7Têtue.png)
Stochastique (n=1) : 22.00 points
Têtue (n=7) : 27.00 points

![Comparaison 1 Stochastique vs 7 Fictitious Play](./graphes/1Stochastique_VS_7FP.png)
Stochastique (n=1) : 24.00 points
Fictitious Play (n=7) : 30.00 points

![Comparaison 1 Stochastique vs 7 Greedy](./graphes/1Stochastique_VS_7Greedy.png)
Stochastique (n=1) : 19.00 points
Greedy (n=7) : 32.00 points

![Comparaison 1 Stochastique vs 7 Imitation](./graphes/1Stochastique_VS_7Imitation.png)
Stochastique (n=1) : 31.00 points
Imitation (n=7) : 22.57 points

![Comparaison 1 Stochastique vs 7 Séquence Fixe](./graphes/1Stochastique_VS_7SF.png)
Stochastique (n=1) : 29.00 points
Séquence Fixe (n=7) : 31.57 points

## Stratégie Greedy vs Autres Stratégies (1 vs 7 joueurs)
![Comparaison 1 Greedy vs 7 Têtue](./graphes/1Greedy_VS_7Têtue.png)
Greedy (n=1) : 31.00 points
Têtue (n=7) : 27.14 points

![Comparaison 1 Greedy vs 7 Stochastique](./graphes/1Greedy_VS_7Stochastique.png)
Greedy (n=1) : 28.00 points
Têtue (n=7) : 25.57 points

![Comparaison 1 Greedy vs 7 Fictitious Play](./graphes/1Greedy_VS_7FP.png)
Greedy (n=1) : 23.00 points
Fictitious Play (n=7) : 31.86 points

![Comparaison 1 Greedy vs 7 Imitation](./graphes/1Greedy_VS_7Imitation.png)
Greedy (n=1) : 29.00 points
Imitation (n=7) : 21.00 points

![Comparaison 1 Greedy vs 7 Séquence Fixe](./graphes/1Greedy_VS_7SF.png)
Greedy (n=1) : 22.00 points
Séquence Fixe (n=7) : 32.57 points

## Stratégie Fictitious Play vs Autres Stratégies (1 vs 7 joueurs)
![Comparaison 1 Fictitious Play vs 7 Têtue](./graphes/1FP_VS_7Têtue.png)
Fictitious Play (n=1) : 50.00 points
Têtue (n=7) : 21.90 points

![Comparaison 1 Fictitious Play vs 7 Stochastique](./graphes/1FP_VS_7Stochastique.png)
Fictitious Play (n=1) : 18.00 points
Têtue (n=7) : 27.86 points

![Comparaison 1 Fictitious Play vs 7 Greedy](./graphes/1FP_VS_7Greedy.png)
Fictitious Play (n=1) : 27.00 points
Greedy (n=7) : 31.29 points

![Comparaison 1 Fictitious Play vs 7 Imitation](./graphes/1FP_VS_7Imitation.png)
Fictitious Play (n=1) : 32.00 points
Imitation (n=7) : 20.86 points

![Comparaison 1 Fictitious Play vs 7 Séquence Fixe](./graphes/1FP_VS_7SF.png)
Fictitious Play (n=1) : 16.00 points
Séquence Fixe (n=7) : 33.43 points

## Stratégie Regret Matching vs Autres Stratégies (1 vs 7 joueurs)
![Comparaison 1 Regret Matching vs 7 Têtue](./graphes/1RM_VS_7Tetu.png)
Regret Matching (n=1) : 34.00 points
Têtue (n=7) : 27.57 points

![Comparaison 1 Regret Matching vs 7 Stochastique](./graphes/1RM_VS_7Stochastique.png)
Regret Matching (n=1) : 24.00 points
Stochastique (n=7) : 26.57 points

![Comparaison 1 Regret Matching vs 7 Greedy](./graphes/1RM_VS_7Greedy.png)
Regret Matching (n=1) : 29.00 points
Greedy (n=7) : 25.29 points

![Comparaison 1 Regret Matching vs 7 Fictitious Play](./graphes/1RM_VS_7FP.png)
Regret Matching (n=1) : 18.00 points
Fictitious Play (n=7) : 30.71 points

![Comparaison 1 Regret Matching vs 7 Imitation](./graphes/1RM_VS_7Imitation.png)
Regret Matching (n=1) : 28.00 points
Imitation (n=7) : 21.43 points

![Comparaison 1 Regret Matching vs 7 Séquence Fixe](./graphes/1RM_VS_7SF.png)
Regret Matching (n=1) : 28.00 points
Séquence Fixe (n=7) : 31.71 points

## Stratégie Imitation vs Autres Stratégies (1 vs 7 joueurs)
![Comparaison 1 Imitation vs 7 Têtue](./graphes/1Imitation_VS_7Têtue.png)
Imitation (n=1) : 21.00 points
Têtue (n=7) : 32.71 points

![Comparaison 1 Imitation vs 7 Stochastique](./graphes/1Imitation_VS_7Stochastique.png)
Imitation (n=1) : 24.00 points
Stochastique (n=7) : 26.00 points

![Comparaison 1 Imitation vs 7 Greedy](./graphes/1Imitation_VS_7Greedy.png)
Imitation (n=1) : 25.00 points
Greedy (n=7) : 30.43 points

![Comparaison 1 Imitation vs 7 Fictitious Play](./graphes/1Imitation_VS_7FP.png)
Imitation (n=1) : 22.00 points
Fictitious Play (n=7) : 31.43 points

![Comparaison 1 Imitation vs 7 Séquence Fixe](./graphes/1Imitation_VS_7FP.png)
Imitation (n=1) : 18.00 points
Séquence Fixe (n=7) : 33.14 points

## Stratégie Séquence Fixe vs Autres Stratégies (1 vs 7 joueurs)
![Comparaison 1 Séquence Fixe vs 7 Têtue](./graphes/1SF_VS_7Têtue.png)
Séquence Fixe (n=1) : 28.00 points
Têtue (n=7) : 20.29 points

![Comparaison 1 Séquence Fixe vs 7 Stochastique](./graphes/1SF_VS_7Stochastique.png)
Séquence Fixe (n=1) : 26.00 points
Stochastique (n=7) : 25.43 points

![Comparaison 1 Séquence Fixe vs 7 Greedy](./graphes/1SF_VS_7Greedy.png)
Séquence Fixe (n=1) : 32.00 points
Greedy (n=7) : 25.71 points

![Comparaison 1 Séquence Fixe vs 7 Fictitious Play](./graphes/1SF_VS_7FP.png)
Séquence Fixe (n=1) : 21.00 points
Fictitious Play (n=7) : 31.43 points

![Comparaison 1 Séquence Fixe vs 7 Imitation](./graphes/1SF_VS_7Imitation.png)
Séquence Fixe (n=1) : 32.00 points
Imitation (n=7) : 21.29 points

