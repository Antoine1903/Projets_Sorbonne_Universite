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
def chiffre_cesar(txt, key):
    """
    Documentation à écrire
    """
    encrypted_text = ""
    for char in txt:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - start + key) % 26 + start)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

# Déchiffrement César
def dechiffre_cesar(txt, key):
    """
    Documentation à écrire
    """
    decrypted_text = ""
    for char in txt:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - start - key) % 26 + start)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
    """
    Chiffrement de Vigenère
    :param txt: Texte clair (str)
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
    
    for i, char in enumerate(txt):
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = key_shifts[i % key_length]  # Utilisation de la clé sous forme de décalage numérique
            encrypted_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    
    return encrypted_text

# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
    """
    Déchiffrement de Vigenère
    :param txt: Texte chiffré (str)
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
    
    for i, char in enumerate(txt):
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = key_shifts[i % key_length]
            decrypted_char = chr((ord(char) - start - shift) % 26 + start)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    
    return decrypted_text


# Analyse de fréquences
def freq(txt):
    """
    Calcule la fréquence d'apparition de chaque lettre de l'alphabet dans un texte donné.
    
    Paramètres :
        txt (str) : Le texte à analyser
    
    Retourne :
        list : Une liste contenant le nombre d'occurrences de chaque lettre de l'alphabet (en ordre)
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    hist = [0.0] * len(alphabet)
    
    txt = txt.lower()  # Convertir en minuscules pour uniformiser
    
    for char in txt:
        if char in alphabet:
            hist[alphabet.index(char)] += 1
    
    return hist

# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Renvoie l'indice dans l'alphabet de la lettre la plus fréquente d'un texte.
    Si plusieurs lettres ont la même fréquence maximale, renvoie la première dans l'ordre alphabétique.
    
    Paramètres :
        txt (str) : Le texte à analyser
    
    Retourne :
        int : L'indice de la lettre la plus fréquente dans l'alphabet
    """
    hist = freq(txt)
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
def longueur_clef(txt, max_len=20):
    """
    Détermine la longueur probable de la clé utilisée pour chiffrer un texte avec Vigenère.
    On teste toutes les tailles de clé possibles jusqu'à max_len et on calcule l'indice de coïncidence moyen.
    La bonne taille est celle où l'IC moyen dépasse 0.06.
    
    :param txt: Texte chiffré (str)
    :param max_len: Longueur maximale de clé à tester (int, par défaut 20)
    :return: Longueur estimée de la clé (int)
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    best_length = 1
    best_ic = 0.0
    
    for key_len in range(1, max_len + 1):
        ic_values = []
        
        # Diviser le texte en colonnes selon la longueur de clé testée
        for i in range(key_len):
            colonne = "".join(txt[j] for j in range(i, len(txt), key_len) if txt[j] in alphabet)
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
    Documentation à écrire
    """
    decalages=[0]*key_length
    return decalages

# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Documentation à écrire
    """
    return "TODO"


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1,h2,d):
    """
    Documentation à écrire
    """
    return 0.0

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Documentation à écrire
    """
    decalages=[0]*key_length
    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Documentation à écrire
    """
    return "TODO"


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1,L2):
    """
    Documentation à écrire
    """
    return 0.0

# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Documentation à écrire
    """
    key=[0]*key_length
    score = 0.0
    return (score, key)

# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Documentation à écrire
    """
    return "TODO"


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