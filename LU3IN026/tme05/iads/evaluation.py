# -*- coding: utf-8 -*-

"""
Package: iads
File: evaluation.py
Année: LU3IN026 - semestre 2 - 2024-2025, Sorbonne Université
"""

# ---------------------------
# Fonctions d'évaluation de classifieurs

# import externe
import numpy as np
import pandas as pd

# ------------------------ 
def crossval(X, Y, n_iterations, iteration):
    N = len(X)
    fold_size = N // n_iterations

    i_start = iteration * fold_size
    i_end = (iteration + 1) * fold_size

    Xtest = X[i_start:i_end]
    Ytest = Y[i_start:i_end]

    Xapp = np.concatenate((X[:i_start], X[i_end:]), axis=0)
    Yapp = np.concatenate((Y[:i_start], Y[i_end:]), axis=0)

    return Xapp, Yapp, Xtest, Ytest

# code de la validation croisée (version qui respecte la distribution des classes)

def crossval_strat(X, Y, n_iterations, iteration):
    unique_classes, class_counts = np.unique(Y, return_counts=True)
    indices_by_class = {cls: np.where(Y == cls)[0] for cls in unique_classes}
    
    test_indices = []
    train_indices_set = set(range(len(X)))  # On part de tous les indices
    
    for cls in unique_classes:
        indices = indices_by_class[cls]
        fold_size = len(indices) // n_iterations
        i_start = iteration * fold_size
        i_end = (iteration + 1) * fold_size if iteration < n_iterations else len(indices)
        
        test_indices.extend(indices[i_start:i_end])
    
    # Suppression des indices test pour obtenir les indices train
    train_indices = sorted(train_indices_set - set(test_indices))

    Xtest, Ytest = X[test_indices], Y[test_indices]
    Xapp, Yapp = X[train_indices], Y[train_indices]
    
    return Xapp, Yapp, Xtest, Ytest

def analyse_perfs(L):
    """ L : liste de nombres réels non vide
        rend le tuple (moyenne, écart-type)
    """
    moyenne = np.mean(L)
    ecart_type = np.std(L)
    return (moyenne, ecart_type)

# ------------------------ 
