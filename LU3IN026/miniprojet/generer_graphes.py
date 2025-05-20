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
    "KNN (Euclidean, Binaire)": {
        "Temps": 2.69899,
        "Train Accuracy": 0.9133,
        "Test Accuracy": 0.5236,
        "Mean Accuracy": 0.5588,
        "Std Dev": 0.0744
    },
    "KNN (Euclidean, Comptage)": {
        "Temps": 2.85428,
        "Train Accuracy": 0.9306,
        "Test Accuracy": 0.6129,
        "Mean Accuracy": 0.5647,
        "Std Dev": 0.0937
    },
    "KNN (Euclidean, Frequence)": {
        "Temps": 2.74317,
        "Train Accuracy": 0.9827,
        "Test Accuracy": 0.7577,
        "Mean Accuracy": 0.7059,
        "Std Dev": 0.0588
    },
    "KNN (Euclidean, TF-IDF)": {
        "Temps": 2.71967,
        "Train Accuracy": 0.9942,
        "Test Accuracy": 0.8361,
        "Mean Accuracy": 0.7882,
        "Std Dev": 0.0861
    },
    "KNN (Cosinus, Binaire)": {
        "Temps": 1.26868,
        "Train Accuracy": 0.9191,
        "Test Accuracy": 0.8323,
        "Mean Accuracy": 0.8647,
        "Std Dev": 0.0478
    },
    "KNN (Cosinus, Comptage)": {
        "Temps": 2.54309,
        "Train Accuracy": 0.9133,
        "Test Accuracy": 0.8629,
        "Mean Accuracy": 0.8529,
        "Std Dev": 0.0322
    },
    "KNN (Cosinus, Frequence)": {
        "Temps": 2.54003,
        "Train Accuracy": 0.9133,
        "Test Accuracy": 0.8622,
        "Mean Accuracy": 0.8529,
        "Std Dev": 0.0322
    },
    "KNN (Cosinus, TF-IDF)": {
        "Temps": 2.60417,
        "Train Accuracy": 0.9480,
        "Test Accuracy": 0.8807,
        "Mean Accuracy": 0.8941,
        "Std Dev": 0.0399
    },
    "Naive Bayes (Binaire)": {
        "Temps": 0.0008771419525146484,
        "Train Accuracy": 0.9826589595375722,
        "Test Accuracy": 0.920280612244898,
        "Mean Accuracy": None,
        "Std Dev": None
    },
    "Naive Bayes (Count)": {
        "Temps": 0.0003383159637451172,
        "Train Accuracy": 0.9826589595375722,
        "Test Accuracy": 0.9196428571428571,
        "Mean Accuracy": None,
        "Std Dev": None
    },
    "Naive Bayes (Frequence)": {
        "Temps": 0.0003361701965332031,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8131377551020408,
        "Mean Accuracy": None,
        "Std Dev": None
    },
    "Naive Bayes (TF-IDF)": {
        "Temps": 0.0003390312194824219,
        "Train Accuracy": 0.9884393063583815,
        "Test Accuracy": 0.8679846938775511,
        "Mean Accuracy": None,
        "Std Dev": None
    }
}

# Données pour les classifications multi-classe
multi_class_data = {
    "Perceptron (Bag-of-Words Binaire)": {
        "Temps": 1.215670108795166,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4583,
        "Mean Accuracy": 0.4367,
        "Std Dev": 0.0223
    },
    "Perceptron (Bag-of-Words Comptage)": {
        "Temps": 1.511552095413208,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4396,
        "Mean Accuracy": 0.4139,
        "Std Dev": 0.0095
    },
    "Perceptron (Bag-of-Words Frequence)": {
        "Temps": 1.565065860748291,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4317,
        "Mean Accuracy": 0.4000,
        "Std Dev": 0.0188
    },
    "Perceptron (Bag-of-Words TF-IDF)": {
        "Temps": 1.0787138938903809,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4479,
        "Mean Accuracy": 0.4072,
        "Std Dev": 0.0200
    },
    "PerceptronBiais (Bag-of-Words Binaire)": {
        "Temps": 31.315280199050903,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4615,
        "Mean Accuracy": None,
        "Std Dev": None
    },
    "PerceptronBiais (Bag-of-Words Comptage)": {
        "Temps": 37.30403804779053,
        "Train Accuracy": 0.9875,
        "Test Accuracy": 0.4790,
        "Mean Accuracy": None,
        "Std Dev": None
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
