import matplotlib.pyplot as plt
import numpy as np

# Données pour les classifications binaires
binary_data = {
    "Perceptron (df2array)": {
        "Temps": 1.2344508171081543,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8220663265306123,
        "Mean Accuracy": 0.9882,
        "Std Dev": 0.0144
    },
    "Perceptron (Bag-of-Words Binaire)": {
        "Temps": 0.6260800361633301,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8233418367346939,
        "Mean Accuracy": 0.9882,
        "Std Dev": 0.0144
    },
    "Perceptron (Bag-of-Words Count)": {
        "Temps": 0.6280159950256348,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8418367346938775,
        "Mean Accuracy": 0.9765,
        "Std Dev": 0.0118
    },
    "Perceptron (Bag-of-Words Freq)": {
        "Temps": 0.6283278465270996,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8392857142857143,
        "Mean Accuracy": 0.8176,
        "Std Dev": 0.0343
    },
    "Perceptron (TF-IDF)": {
        "Temps": 0.6245517730712891,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8367346938775511,
        "Mean Accuracy": 0.8353,
        "Std Dev": 0.0546
    },
    "PerceptronBiais (df2array)": {
        "Temps": 1.439255952835083,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8596938775510204,
        "Mean Accuracy": 0.9882,
        "Std Dev": 0.0144
    },
    "PerceptronBiais (Bag-of-Words Binaire)": {
        "Temps": 0.7138469219207764,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8596938775510204,
        "Mean Accuracy": 0.9882,
        "Std Dev": 0.0144
    },
    "PerceptronBiais (Bag-of-Words Count)": {
        "Temps": 0.6987202167510986,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8596938775510204,
        "Mean Accuracy": 0.9882,
        "Std Dev": 0.0144
    },
    "PerceptronBiais (Bag-of-Words Freq)": {
        "Temps": 0.8460118770599365,
        "Train Accuracy": 0.976878612716763,
        "Test Accuracy": 0.8405612244897959,
        "Mean Accuracy": 0.9824,
        "Std Dev": 0.0235
    },
    "PerceptronBiais (TF-IDF)": {
        "Temps": 0.855891227722168,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.9139030612244898,
        "Mean Accuracy": 0.9882,
        "Std Dev": 0.0144
    },
    "KNN k=3 (Euclidean, Binaire)": {
        "Temps": 2.69899,
        "Train Accuracy": 0.9133,
        "Test Accuracy": 0.5236,
        "Mean Accuracy": 0.5588,
        "Std Dev": 0.0744
    },
    "KNN k=3 (Euclidean, Comptage)": {
        "Temps": 2.85428,
        "Train Accuracy": 0.9306,
        "Test Accuracy": 0.6129,
        "Mean Accuracy": 0.5647,
        "Std Dev": 0.0937
    },
    "KNN k=3 (Euclidean, Frequence)": {
        "Temps": 2.74317,
        "Train Accuracy": 0.9827,
        "Test Accuracy": 0.7577,
        "Mean Accuracy": 0.7059,
        "Std Dev": 0.0588
    },
    "KNN k=3 (Euclidean, TF-IDF)": {
        "Temps": 2.71967,
        "Train Accuracy": 0.9942,
        "Test Accuracy": 0.8361,
        "Mean Accuracy": 0.7882,
        "Std Dev": 0.0861
    },
    "KNN k=3 (Cosinus, Binaire)": {
        "Temps": 1.26868,
        "Train Accuracy": 0.9191,
        "Test Accuracy": 0.8323,
        "Mean Accuracy": 0.8647,
        "Std Dev": 0.0478
    },
    "KNN k=3 (Cosinus, Comptage)": {
        "Temps": 2.54309,
        "Train Accuracy": 0.9133,
        "Test Accuracy": 0.8629,
        "Mean Accuracy": 0.8529,
        "Std Dev": 0.0322
    },
    "KNN k=3 (Cosinus, Frequence)": {
        "Temps": 2.54003,
        "Train Accuracy": 0.9133,
        "Test Accuracy": 0.8622,
        "Mean Accuracy": 0.8529,
        "Std Dev": 0.0322
    },
    "KNN k=3 (Cosinus, TF-IDF)": {
        "Temps": 2.60417,
        "Train Accuracy": 0.9480,
        "Test Accuracy": 0.8807,
        "Mean Accuracy": 0.8941,
        "Std Dev": 0.0399
    },
    "Naive Bayes (Bag-of-Words Binaire) - Version 1": {
        "Temps": 0.0003540515899658203,
        "Train Accuracy": 0.9826589595375722,
        "Test Accuracy": 0.920280612244898,
        "Mean Accuracy": 0.5035,
        "Std Dev": 0.0062
    },
    "Naive Bayes (Bag-of-Words Count) - Version 2": {
        "Temps": 0.0003299713134765625,
        "Train Accuracy": 0.9826589595375722,
        "Test Accuracy": 0.9196428571428571,
        "Mean Accuracy": 0.5069,
        "Std Dev": 0.0022
    },
    "Naive Bayes (Bag-of-Words Freq) - Version 3": {
        "Temps": 0.0003440380096435547,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8131377551020408,
        "Mean Accuracy": 0.5277,
        "Std Dev": 0.0044
    },
    "Naive Bayes (TF-IDF) - Version 4": {
        "Temps": 0.0004019737243652344,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8679846938775511,
        "Mean Accuracy": 0.5194,
        "Std Dev": 0.0071
    },
    "Arbre de Decision (Bag-of-Words Binaire) - Version 1": {
        "Temps": 0.011491060256958008,
        "Train Accuracy": 0.9942,
        "Test Accuracy": 0.7838,
        "Mean Accuracy": 0.7339,
        "Std Dev": 0.0694
    },
    "Arbre de Decision (Bag-of-Words Comptage) - Version 2": {
        "Temps": 0.012052059173583984,
        "Train Accuracy": 0.9942,
        "Test Accuracy": 0.7838,
        "Mean Accuracy": 0.7397,
        "Std Dev": 0.0663
    },
    "Arbre de Decision (Bag-of-Words Freq) - Version 3": {
        "Temps": 0.012031078338623047,
        "Train Accuracy": 0.9942,
        "Test Accuracy": 0.7640,
        "Mean Accuracy": 0.7049,
        "Std Dev": 0.0479
    },
    "Arbre de Decision (TF-IDF) - Version 4": {
        "Temps": 0.012356281280517578,
        "Train Accuracy": 0.9942,
        "Test Accuracy": 0.7615,
        "Mean Accuracy": 0.6877,
        "Std Dev": 0.0784
    }
}

# Données pour les classifications multi-classe
multi_class_data = {
    "Perceptron (Bag-of-Words Binaire) - Version 1": {
        "Temps": 1.340700387954712,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4487,
        "Mean Accuracy": 0.4406,
        "Std Dev": 0.0139
    },
    "Perceptron (Bag-of-Words Comptage) - Version 2": {
        "Temps": 1.5071141719818115,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4396,
        "Mean Accuracy": 0.4139,
        "Std Dev": 0.0095
    },
    "Perceptron (Bag-of-Words Frequence) - Version 3": {
        "Temps": 1.550534963607788,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4317,
        "Mean Accuracy": 0.4000,
        "Std Dev": 0.0188
    },
    "Perceptron (TF-IDF) - Version 4": {
        "Temps": 1.0824470520019531,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4479,
        "Mean Accuracy": 0.4072,
        "Std Dev": 0.0200
    },
    "PerceptronBiais (Bag-of-Words Binaire) - Version 1": {
        "Temps": 15.13516092300415,
        "Train Accuracy": 0.9891,
        "Test Accuracy": 0.4274,
        "Mean Accuracy": 0.4083,
        "Std Dev": 0.0288
    },
    "PerceptronBiais (Bag-of-Words Comptage) - Version 2": {
        "Temps": 15.734153985977173,
        "Train Accuracy": 0.9891,
        "Test Accuracy": 0.4500,
        "Mean Accuracy": 0.4233,
        "Std Dev": 0.0182
    },
    "PerceptronBiais (Bag-of-Words Frequence) - Version 3": {
        "Temps": 22.45213007926941,
        "Train Accuracy": 0.9831,
        "Test Accuracy": 0.5198,
        "Mean Accuracy": 0.5117,
        "Std Dev": 0.0107
    },
    "PerceptronBiais (TF-IDF) - Version 4": {
        "Temps": 24.96455693244934,
        "Train Accuracy": 0.9782,
        "Test Accuracy": 0.5690,
        "Mean Accuracy": 0.5544,
        "Std Dev": 0.0150
    },
    "KNN k=3 (Bag-of-Words Binaire) - Version 1 (Euclidienne)": {
        "Temps": 0.015555143356323242,
        "Train Accuracy": 0.3252,
        "Test Accuracy": 0.0783,
        "Mean Accuracy": 0.0773,
        "Std Dev": 0.0053
    },
    "KNN k=3 (Bag-of-Words Comptage) - Version 2 (Euclidienne)": {
        "Temps": 0.01619720458984375,
        "Train Accuracy": 0.3883,
        "Test Accuracy": 0.1278,
        "Mean Accuracy": 0.1182,
        "Std Dev": 0.0173
    },
    "KNN k=3 (Bag-of-Words Frequence) - Version 3 (Euclidienne)": {
        "Temps": 0.015926122665405273,
        "Train Accuracy": 0.3617,
        "Test Accuracy": 0.1158,
        "Mean Accuracy": 0.1073,
        "Std Dev": 0.0163
    },
    "KNN k=3 (TF-IDF) - Version 4 (Euclidienne)": {
        "Temps": 0.016103267669677734,
        "Train Accuracy": 0.3203,
        "Test Accuracy": 0.0981,
        "Mean Accuracy": 0.0839,
        "Std Dev": 0.0053
    },
    "KNN k=3 (Bag-of-Words Binaire) - Version 1 (Cosinus)": {
        "Temps": 0.0025701522827148438,
        "Train Accuracy": 0.5501,
        "Test Accuracy": 0.2569,
        "Mean Accuracy": 0.2511,
        "Std Dev": 0.0282
    },
    "KNN k=3 (Bag-of-Words Comptage) - Version 2 (Cosinus)": {
        "Temps": 0.0020890235900878906,
        "Train Accuracy": 0.5561,
        "Test Accuracy": 0.3004,
        "Mean Accuracy": 0.2761,
        "Std Dev": 0.0085
    },
    "KNN k=3 (Bag-of-Words Frequence) - Version 3 (Cosinus)": {
        "Temps": 0.0019431114196777344,
        "Train Accuracy": 0.5561,
        "Test Accuracy": 0.3004,
        "Mean Accuracy": 0.2761,
        "Std Dev": 0.0085
    },
    "KNN k=3 (TF-IDF) - Version 4 (Cosinus)": {
        "Temps": 0.0019330978393554688,
        "Train Accuracy": 0.6389,
        "Test Accuracy": 0.3996,
        "Mean Accuracy": 0.3736,
        "Std Dev": 0.0226
    },
    "Naive Bayes (Bag-of-Words Binaire) - Version 1 (Multi-classe)": {
        "Temps": 0.005355119705200195,
        "Train Accuracy": 0.9183006535947712,
        "Test Accuracy": 0.49284425736620563,
        "Mean Accuracy": 0.0519,
        "Std Dev": 0.0001
    },
    "Naive Bayes (Bag-of-Words Comptage) - Version 2 (Multi-classe)": {
        "Temps": 0.004981040954589844,
        "Train Accuracy": 0.9183006535947712,
        "Test Accuracy": 0.49284425736620563,
        "Mean Accuracy": 0.0519,
        "Std Dev": 0.0001
    },
    "Naive Bayes (Bag-of-Words Frequence) - Version 3 (Multi-classe)": {
        "Temps": 0.0052738189697265625,
        "Train Accuracy": 0.9183006535947712,
        "Test Accuracy": 0.49284425736620563,
        "Mean Accuracy": 0.0519,
        "Std Dev": 0.0001
    },
    "Naive Bayes (TF-IDF) - Version 4 (Multi-classe)": {
        "Temps": 0.006360054016113281,
        "Train Accuracy": 0.9183006535947712,
        "Test Accuracy": 0.49284425736620563,
        "Mean Accuracy": 0.0519,
        "Std Dev": 0.0001
    },
    "Arbre de Decision (Bag-of-Words Binaire) - Version 1 (Multi-classe)": {
        "Temps": 0.9992218017578125,
        "Train Accuracy": 0.9891,
        "Test Accuracy": 0.2162,
        "Mean Accuracy": 0.2037,
        "Std Dev": 0.0096
    },
    "Arbre de Decision (Bag-of-Words Comptage) - Version 2 (Multi-classe)": {
        "Temps": 0.976754903793335,
        "Train Accuracy": 0.9891,
        "Test Accuracy": 0.2191,
        "Mean Accuracy": 0.2157,
        "Std Dev": 0.0175
    },
    "Arbre de Decision (Bag-of-Words Frequence) - Version 3 (Multi-classe)": {
        "Temps": 1.0161161422729492,
        "Train Accuracy": 0.9891,
        "Test Accuracy": 0.2162,
        "Mean Accuracy": 0.2092,
        "Std Dev": 0.0124
    },
    "Arbre de Decision (TF-IDF) - Version 4 (Multi-classe)": {
        "Temps": 1.052858829498291,
        "Train Accuracy": 0.9891,
        "Test Accuracy": 0.2163,
        "Mean Accuracy": 0.2092,
        "Std Dev": 0.0124
    }
}

# Fonction pour créer les graphes
def plot_comparison(data, title, ylabel, key):
    plt.figure(figsize=(12, 8))
    labels = []
    values = []

    for label, d in data.items():
        value = d[key]
        if value is not None:  # Ignorer les valeurs None
            labels.append(label)
            values.append(value)

    bars = plt.bar(labels, values)
    plt.xticks(rotation=90)
    plt.title(title)
    plt.ylabel(ylabel)

    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height:.4f}',
                 ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# Graphes pour les classifications binaires
plot_comparison(binary_data, "Temps d'exécution pour les classifications binaires", "Temps (secondes)", "Temps")
plot_comparison(binary_data, "Accuracy de train pour les classifications binaires", "Accuracy", "Train Accuracy")
plot_comparison(binary_data, "Accuracy de test pour les classifications binaires", "Accuracy", "Test Accuracy")
plot_comparison(binary_data, "Taux moyen de bonne classification pour les classifications binaires", "Taux moyen", "Mean Accuracy")
plot_comparison(binary_data, "Écarts-type pour les classifications binaires", "Écart-type", "Std Dev")

# Graphes pour les classifications multi-classe
plot_comparison(multi_class_data, "Temps d'exécution pour les classifications multi-classe", "Temps (secondes)", "Temps")
plot_comparison(multi_class_data, "Accuracy de train pour les classifications multi-classe", "Accuracy", "Train Accuracy")
plot_comparison(multi_class_data, "Accuracy de test pour les classifications multi-classe", "Accuracy", "Test Accuracy")
plot_comparison(multi_class_data, "Taux moyen de bonne classification pour les classifications multi-classe", "Taux moyen", "Mean Accuracy")
plot_comparison(multi_class_data, "Écarts-type pour les classifications multi-classe", "Écart-type", "Std Dev")
