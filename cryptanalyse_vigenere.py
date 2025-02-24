# Sorbonne Université 3I024 2024-2025
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : Zhang Yuxiang 21202829
# Etudiant.e 2 : Lecomte Antoine 21103457

import sys, getopt, string, math

# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fréquence moyenne des lettres en français

# Déjà modifié
freq_FR = [0.092060, 0.010360, 0.030219, 0.037547, 0.171768, 0.010960, 0.010608, 0.010718, 0.075126, 0.003824, 0.000070, 0.061318, 0.026482, 0.070310, 0.049171, 0.023706, 0.010156, 0.066094, 0.078126, 0.073770, 0.063540, 0.016448, 0.000011, 0.004080, 0.002296, 0.001231]


# Chiffrement César
def chiffre_cesar(cipher, key):
    """
    Documentation à écrire
    """
    encrypted_text = ""
    for char in cipher:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - start + key) % len(alphabet) + start)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text


# Déchiffrement César
def dechiffre_cesar(cipher, key):
    """
    Documentation à écrire
    """
    decrypted_text = ""
    for char in cipher:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - start - key) % len(alphabet) + start)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text


# Chiffrement Vigenere
def chiffre_vigenere(cipher, key):
    """
    Chiffrement de Vigenère
    :param cipher: Texte clair (str)
    :param key: Clé (str ou liste d'entiers)
    :return: Texte chiffré (str)
    """
    encrypted_text = ""
    
    # Vérifie si la clé est une chaîne ou une liste d'entiers
    if isinstance(key, str):
        key_shifts = [ord(k.upper()) - ord('A') for k in key]
    else:
        key_shifts = key  # La clé est déjà une liste d'entiers
    
    key_length = len(key_shifts)
    
    for i, char in enumerate(cipher):
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = key_shifts[i % key_length]  # Utilisation de la clé sous forme de décalage numérique
            encrypted_char = chr((ord(char) - start + shift) % len(alphabet) + start)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    
    return encrypted_text


# Déchiffrement Vigenere
def dechiffre_vigenere(cipher, key):
    """
    Déchiffrement de Vigenère
    :param cipher: Texte chiffré (str)
    :param key: Clé (str ou liste d'entiers)
    :return: Texte déchiffré (str)
    """
    decrypted_text = ""
    
    # Vérifie si la clé est une chaîne ou une liste d'entiers
    if isinstance(key, str):
        key_shifts = [ord(k.upper()) - ord('A') for k in key]
    else:
        key_shifts = key  # La clé est déjà une liste d'entiers
    
    key_length = len(key_shifts)
    
    for i, char in enumerate(cipher):
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = key_shifts[i % key_length]
            decrypted_char = chr((ord(char) - start - shift) % len(alphabet) + start)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    
    return decrypted_text


# Analyse de fréquences
def freq(cipher):
    """
    Calcule la fréquence d'apparition de chaque lettre de l'alphabet dans un texte donné.
    
    Paramètres :
        cipher (str) : Le texte à analyser
    
    Retourne :
        list : Une liste contenant le nombre d'occurrences de chaque lettre de l'alphabet (en ordre)
    """
    hist = [0] * len(alphabet)
    
    # Filtrer et compter seulement les caractères valides (lettres)
    for char in cipher:
        if char in alphabet:
            hist[alphabet.index(char)] += 1
    
    return hist


# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(cipher):
    """
    Renvoie l'indice dans l'alphabet de la lettre la plus fréquente d'un texte.
    Si plusieurs lettres ont la même fréquence maximale, renvoie la première dans l'ordre alphabétique.
    
    Paramètres :
        cipher (str) : Le texte à analyser
    
    Retourne :
        int : L'indice de la lettre la plus fréquente dans l'alphabet
    """
    hist = freq(cipher)
    max_freq = max(hist)
    return hist.index(max_freq)


# indice de coïncidence
def indice_coincidence(hist):
    """
    Calcule l'indice de coïncidence d'un texte à partir de son histogramme de fréquences.
    
    Paramètres :
        hist (list) : Une liste contenant le nombre d'occurrences de chaque lettre de l'alphabet
    
    Retourne :
        float : L'indice de coïncidence du texte
    """
    n = sum(hist)  # Nombre total de lettres dans le texte
    if n <= 1:
        return 0  # Éviter la division par zéro
    
    ic = sum(ni * (ni - 1) for ni in hist) / (n * (n - 1))
    return ic


# Recherche la longueur de la clé
def longueur_clef(cipher, max_len=20):
    """
    Estime la longueur de la clé en testant plusieurs longueurs de clé,
    et en calculant l'indice de coïncidence moyen pour chaque longueur.
    
    Paramètres :
        cipher (str) : Le texte chiffré
    
    Retourne :
        int : La longueur de la clé estimée
    """
    best_key_length = 0
    best_avg_ic = 0  # La meilleure moyenne d'indice de coïncidence trouvée

    # Tester pour chaque longueur de clé entre 1 et 20
    for key_length in range(1, max_len + 1):  
        colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet)
                    for i in range(key_length)]
        
        # Calcul de la moyenne des indices de coïncidence pour toutes les colonnes
        avg_ic = sum(indice_coincidence(freq(col)) for col in colonnes) / key_length
        
        # Si la moyenne de l'indice de coïncidence dépasse 0.06, on retourne immédiatement la clé
        if avg_ic > 0.06:
            return key_length
    
        # Sinon, on cherche à garder la meilleure longueur de clé
        if avg_ic > best_avg_ic:
            best_avg_ic = avg_ic  # On met à jour la meilleure moyenne
            best_key_length = key_length  # Et on garde cette longueur de clé
    
    # Si aucune longueur de clé n'a dépassé 0.06, on retourne la meilleure trouvée
    return best_key_length

    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Détermine la clé sous forme d'une table de décalages en supposant que la lettre la plus fréquente est 'E'.
    
    Paramètres :
        cipher (str) : Le texte chiffré
        key_length (int) : La longueur de la clé estimée
    
    Retourne :
        list : Une liste d'entiers représentant les décalages de la clé
    """
    reference_letter = 'E'
    ref_index = alphabet.index(reference_letter)
    
    key_shifts = []
    
    for i in range(key_length):
        colonne = "".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet)
        
        if colonne:
            most_freq_index = lettre_freq_max(colonne)  # Trouver la lettre la plus fréquente
            shift = (most_freq_index - ref_index) % len(alphabet)  # Calculer le décalage
            key_shifts.append(shift)
    
    return key_shifts


# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Effectue une cryptanalyse basique du chiffrement de Vigenère en déterminant la clé
    et en déchiffrant le texte chiffré.
    
    Paramètres :
        cipher (str) : Le texte chiffré
    
    Retourne :
        str : Le texte déchiffré
    """
    # Estimer la longueur de la clé
    key_length = longueur_clef(cipher)
    
    # Déterminer la clé sous forme de décalages
    best_key = clef_par_decalages(cipher, key_length)
    
    # Utiliser la fonction dechiffre_vigenere avec la clé obtenue pour déchiffrer le texte
    decrypted_text = dechiffre_vigenere(cipher, best_key)
    
    return decrypted_text

################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1, h2, d):
    """
    Calcule l'indice de coïncidence mutuelle entre deux histogrammes de fréquences,
    en testant un décalage de d positions.

    Paramètres :
        h1 (list) : Histogramme des fréquences de la première colonne
        h2 (list) : Histogramme des fréquences de la seconde colonne
        d (int) : Décalage testé
    
    Retourne :
        float : L'indice de coïncidence mutuelle
    """
    N1 = sum(h1)
    N2 = sum(h2)
    
    if N1 == 0 or N2 == 0:
        return 0.0  # Éviter la division par zéro

    icm = sum(h1[i] * h2[(i + d) % len(h2)] for i in range(len(alphabet))) / (N1 * N2)
    
    return icm


# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Détermine les décalages relatifs des colonnes par rapport à la première colonne
    en maximisant l'indice de coïncidence mutuelle.

    Paramètres :
        cipher (str) : Le texte chiffré
        key_length (int) : La longueur de la clé estimée
    
    Retourne :
        list : Une liste d'entiers représentant les décalages de la clé
    """
    # Découper le texte en colonnes
    colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet)
                for i in range(key_length)]
    
    decalages = [0]  # La première colonne a un décalage nul par rapport à elle-même

    # Calculer le décalage relatif pour chaque colonne
    for i in range(1, key_length):
        max_icm = 0  # Initialiser la valeur maximale de l'ICM
        best_decalage = 0  # Initialiser le meilleur décalage

        # Calculer l'ICM pour chaque décalage de 0 à 25
        for d in range(len(alphabet)):
            icm_value = indice_coincidence_mutuelle(freq(colonnes[0]), freq(colonnes[i]), d)
            if icm_value > max_icm:
                max_icm = icm_value
                best_decalage = d

        # Ajouter le décalage trouvé pour cette colonne
        decalages.append(best_decalage)

    return decalages


# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Déchiffre un texte chiffré par Vigenère en utilisant l'indice de coïncidence pour déterminer la longueur de la clé,
    puis en calculant les décalages relatifs de chaque colonne. Une fois les colonnes alignées, on applique le déchiffrement 
    de Vigenère avec la clé trouvée.
    
    Paramètre :
        cipher (str) : Le texte chiffré
    
    Retourne :
        str : Le texte déchiffré
    """
    
    # Estimer la longueur de la clé à partir de l'indice de coïncidence
    key_length = longueur_clef(cipher)
    print(f"Longueur de clé estimée : {key_length}")
    
    # Trouver les décalages relatifs par rapport à la première colonne
    decalages = tableau_decalages_ICM(cipher, key_length)
    print(f"Décalages trouvés : {decalages}")
    
    # Convertir les décalages en clé sous forme de chaîne de caractères
    best_key = "".join(alphabet[d] for d in decalages)
    
    # Utiliser la fonction dechiffre_vigenere avec la clé obtenue pour déchiffrer le texte
    decrypted_text = dechiffre_vigenere(cipher, best_key)
    
    return decrypted_text


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1, L2):
    """
    Calcule la corrélation de Pearson entre deux listes de même taille.

    Paramètres :
        L1 (list) : Première liste
        L2 (list) : Seconde liste
    
    Retourne :
        float : Coefficient de corrélation de Pearson
    """
    if len(L1) != len(L2) or len(L1) == 0:
        return 0.0

    mean1, mean2 = sum(L1) / len(L1), sum(L2) / len(L2)
    
    num = sum((L1[i] - mean1) * (L2[i] - mean2) for i in range(len(L1)))
    denom = math.sqrt(sum((L1[i] - mean1) ** 2 for i in range(len(L1))) * 
                      sum((L2[i] - mean2) ** 2 for i in range(len(L2))))
    
    return num / denom if denom != 0 else 0.0


# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Trouve la clé qui maximise la corrélation avec un texte français pour une longueur de clé donnée.
    
    Paramètres :
        cipher (str) : Le texte chiffré
        key_length (int) : La longueur de la clé estimée
    
    Retourne :
        tuple : (moyenne des corrélations, liste des décalages)
    """
    colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet)
                for i in range(key_length)]
    
    histos = [freq(col) for col in colonnes]
    
    best_shifts = []
    best_corrs = []
    
    for hist in histos:
        best_d, best_corr = 0, -1
        for d in range(len(alphabet)):
            shifted_hist = hist[d:] + hist[:d]  # Décalage circulaire
            corr = correlation(shifted_hist, freq_FR)
            if corr > best_corr:
                best_corr, best_d = corr, d
        
        best_corrs.append(best_corr)
        best_shifts.append(best_d)
    
    # Moyenne des corrélations sur toutes les colonnes
    avg_corr = sum(best_corrs) / key_length
    return avg_corr, best_shifts


# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Déchiffre un texte chiffré par le chiffrement de Vigenère en utilisant l'analyse de la corrélation de Pearson.
    Teste différentes tailles de clé et choisit celle qui maximise la moyenne des corrélations.
    
    Paramètre :
        cipher (str) : Le texte chiffré
    
    Retourne :
        str : Le texte déchiffré
    """
    best_avg_corr = -1  # Initialiser la meilleure moyenne de corrélation
    best_shifts = []  # Initialiser les meilleurs décalages
    
    # Tester pour chaque taille de clé de 1 à 20
    for key_length in range(1, 21):
        avg_corr, shifts = clef_correlations(cipher, key_length)
        
        # Si la moyenne des corrélations est meilleure, on met à jour les variables
        if avg_corr > best_avg_corr:
            best_avg_corr = avg_corr
            best_shifts = shifts
    
    # Déchiffrer le texte avec la clé obtenue
    best_key = "".join(alphabet[shift] for shift in best_shifts)
    decrypted_text = dechiffre_vigenere(cipher, best_key)
    
    return decrypted_text


################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])
