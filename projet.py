def lire_pref_etudiants(fichier):
    with open(fichier, "r") as f:
        lignes = f.readlines()
    
    nb_etudiants = int(lignes[0].strip())
    CE = []
    
    for ligne in lignes[1:]:
        _, _, *preferences = ligne.strip().split()
        CE.append(list(map(int, preferences)))
    
    return CE


def lire_pref_parcours(fichier):
    with open(fichier, "r") as f:
        lignes = f.readlines()
    
    nb_etudiants = int(lignes[0].strip())
    capacites = list(map(int, lignes[1].strip().split()))
    CP = []
    
    for ligne in lignes[2:]:
        _, _, *preferences = ligne.strip().split()
        CP.append(list(map(int, preferences)))
    
    return CP

pref_etu_file = "PrefEtu.txt"
pref_spe_file = "PrefSpe.txt"

# 调用函数读取数据
CE = lire_pref_etudiants(pref_etu_file)
CP, capacites = lire_pref_parcours(pref_spe_file)

# 打印结果以验证
print("学生偏好矩阵 (CE)：")
for i, row in enumerate(CE):
    print(f"学生 {i}: {row}")

print("\n专业偏好矩阵 (CP)：")
for i, row in enumerate(CP):
    print(f"专业 {i}: {row}")

print("\n专业的容量 (Capacités)：")
print(capacites)