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
            encrypted_char = chr((ord(char) - start + key) % 26 + start)
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
            decrypted_char = chr((ord(char) - start - key) % 26 + start)
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
            encrypted_char = chr((ord(char) - start + shift) % 26 + start)
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
            decrypted_char = chr((ord(char) - start - shift) % 26 + start)
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
    hist = [0.0] * len(alphabet)
    
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
        return 0.0  # Éviter la division par zéro
    
    ic = sum(ni * (ni - 1) for ni in hist) / (n * (n - 1))
    return ic

# Recherche la longueur de la clé
def longueur_clef(cipher, max_len=20):
    """
    Détermine la longueur probable de la clé utilisée pour chiffrer un texte avec Vigenère.
    On teste toutes les tailles de clé possibles jusqu'à max_len et on calcule l'indice de coïncidence moyen.
    La bonne taille est celle où l'IC moyen dépasse 0.06.
    
    :param cipher: Texte chiffré (str)
    :param max_len: Longueur maximale de clé à tester (int, par défaut 20)
    :return: Longueur estimée de la clé (int)
    """
    best_length = 1
    best_ic = 0.0
    
    for key_len in range(1, max_len + 1):
        ic_values = []
        
        # Diviser le texte en colonnes selon la longueur de clé testée
        for i in range(key_len):
            colonne = "".join(cipher[j] for j in range(i, len(cipher), key_len) if cipher[j] in alphabet)
            if colonne:  # S'assurer que la colonne n'est pas vide
                hist = freq(colonne)  # Utiliser la fonction freq pour calculer l'histogramme
                ic_values.append(indice_coincidence(hist))
        
        # Calculer la moyenne des IC des colonnes
        if ic_values:
            ic_moyen = sum(ic_values) / len(ic_values)
            if ic_moyen > 0.06:  # Seuil indicatif pour une langue naturelle
                return key_len
            
            # Sauvegarde la meilleure valeur trouvée au cas où
            if ic_moyen > best_ic:
                best_ic = ic_moyen
                best_length = key_len
    
    return best_length

    
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
    Effectue une cryptanalyse basique du chiffre de Vigenère en déterminant la clé
    et en déchiffrant le texte chiffré.
    
    Paramètres :
        cipher (str) : Le texte chiffré
    
    Retourne :
        str : Le texte déchiffré
    """
    # Étape 1 : Déterminer la longueur de la clé
    key_length = longueur_clef(cipher)
    
    if key_length is None:
        return "Impossible de déterminer la longueur de la clé."
    
    # Étape 2 : Déterminer la clé sous forme de décalages
    key_shifts = clef_par_decalages(cipher, key_length)
    
    # Étape 3 : Déchiffrer le texte avec la clé trouvée
    decrypted_text = dechiffre_vigenere(cipher, key_shifts)
    
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
    N1, N2 = sum(h1), sum(h2)
    if N1 == 0 or N2 == 0:
        return 0.0  # Éviter la division par zéro

    icm = sum(h1[i] * h2[(i + d) % 26] for i in range(26)) / (N1 * N2)
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
    colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet)
                for i in range(key_length)]
    
    # Calculer les histogrammes des colonnes
    histos = [freq(col) for col in colonnes]
    
    decalages = [0]  # La première colonne est la référence
    
    for i in range(1, key_length):
        best_d, best_icm = 0, 0.0
        for d in range(26):  # Tester tous les décalages possibles
            icm = indice_coincidence_mutuelle(histos[0], histos[i], d)
            if icm > best_icm:
                best_icm, best_d = icm, d
        decalages.append(best_d)
    
    return decalages


# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Effectue la cryptanalyse du chiffre de Vigenère avec l'ICM pour retrouver la clé et déchiffrer le message.
    
    Paramètre :
        cipher (str) : Texte chiffré
    
    Retourne :
        tuple : (clé estimée, texte déchiffré)
    """
    # 1. Déterminer la longueur probable de la clé
    key_length = longueur_clef(cipher)
    
    # 2. Trouver les décalages des colonnes
    decalages = tableau_decalages_ICM(cipher, key_length)
    
    # 3. Déduire la clé en prenant la lettre la plus fréquente dans chaque colonne
    colonnes = ["".join(cipher[j] for j in range(i, len(cipher), key_length) if cipher[j] in alphabet)
                for i in range(key_length)]
    
    clef = ""
    for i in range(key_length):
        histo = freq(colonnes[i])
        lettre_plus_frequente = histo.index(max(histo))  # Trouver la lettre la plus fréquente
        shift = (lettre_plus_frequente - (ord('E') - ord('A'))) % 26  # Supposer que 'E' est la plus fréquente
        clef += alphabet[shift]
    
    # 4. Déchiffrer le texte avec la clé trouvée
    texte_dechiffre = ""
    for i, c in enumerate(cipher):
        if c in alphabet:
            shift = ord(clef[i % key_length]) - ord('A')
            texte_dechiffre += alphabet[(ord(c) - ord('A') - shift) % 26]
        else:
            texte_dechiffre += c
    
    return clef, texte_dechiffre


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
    Trouve la clé qui maximise la corrélation avec un texte français.

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
        for d in range(26):
            shifted_hist = hist[d:] + hist[:d]  # Décalage circulaire
            corr = correlation(shifted_hist, freq_FR)
            if corr > best_corr:
                best_corr, best_d = corr, d
        
        best_corrs.append(best_corr)
        best_shifts.append(best_d)

    return (sum(best_corrs) / key_length, best_shifts)


# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Effectue une cryptanalyse en utilisant la corrélation de Pearson pour trouver 
    la meilleure taille de clé et ses décalages.

    Paramètres :
        cipher (str) : Le texte chiffré
    
    Retourne :
        str : La clé estimée sous forme de chaîne de caractères
    """
    best_key, best_score = "", 0.0
    
    for key_length in range(1, 21):
        score, shifts = clef_correlations(cipher, key_length)
        if score > best_score:
            best_score, best_key = score, "".join(alphabet[d] for d in shifts)
    
    return best_key


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
