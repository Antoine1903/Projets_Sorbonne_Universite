# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: Zhenming WANG
#  Prénom Nom: Hoang Nguyen VU

import subsomption, braitenberg_avoider, braitenberg_hateBot, braitenberg_loveBot, braitenberg_hateWall
import random, math

iteration_global = 0
iteration_robs = [0] * 8    # indique les nombres de fois d'enregistrements de mouvements pour chaque robot (valeur entre [0, 4])
score_individual = [[0,0,0,0] for _ in range(8)]
lst_individual = [[] for _ in range(8)] # {[(translation, rotation), (..), .. *5 = enregistrer le mouvement de robotId=0], [...], ...*8 = nb de robots par équipe}
population = []
flag_initial = False
lst_flag = [False] * 8


def get_team_name():
    return "STRONGEST_TEAM" # à compléter (comme vous voulez)


def step(robotId, sensors):
    global iteration_robs, lst_individual, iteration_global, population, flag_initial, lst_flag
    sensors = subsomption.get_extended_sensors(sensors) # pour obtenir les infos de distances: (sensors[sensors_front..][distance_to_..])
    
    # arbre de comportement:     
    if(sensors["sensor_front"]["isRobot"] == True or sensors["sensor_front_left"]["isRobot"] == True or sensors["sensor_front_right"]["isRobot"] == True):  #S'il existe un robot en avance:
        if(sensors["sensor_front"]["isSameTeam"] == True or sensors["sensor_front_left"]["isSameTeam"] == True or sensors["sensor_front_right"]["isSameTeam"] == True): # si le robot en avance est le même groupe
            (translation, rotation) = braitenberg_hateBot.step(robotId, sensors)
            #translation += 1 * sensors["sensor_front"]["distance_to_wall"]
        else:   # sinon, le robot en avance est dans le groupe diff
            (translation, rotation) = braitenberg_loveBot.step(robotId, sensors)
            #translation += 1 * sensors["sensor_front"]["distance_to_wall"]
        # indique la priorité de décision de mouvement:
        lst_flag[int(robotId%8)] = True # on marque la 1ere détection de l'obstacle
    elif(sensors["sensor_front"]["distance_to_wall"] != 1 or sensors["sensor_front_left"]["distance_to_wall"] != 1  or sensors["sensor_front_right"]["distance_to_wall"] != 1):
        (translation, rotation) = braitenberg_hateWall.step(robotId,sensors)
        #translation += 1 * sensors["sensor_front"]["distance_to_robot"]
        lst_flag[int(robotId%8)] = True 
    else:   
        #(translation, rotation) = braitenberg_avoider.step(robotId, sensors)    
        (translation, rotation) = 1, 0 # aller tout droit par défault

    # pour l'algo génétique:
    if(not flag_initial):   # si on est en train d'initialiser la population (c_à-d 1ère fois)
        if(int(iteration_global%160)!=0 or iteration_global == 0):  # initialise lst_indivitual:
            if(iteration_robs[int(robotId%8)] < 5): 
                initial_lst_individual(int(robotId%8), translation, rotation)   # registre ce mouvement
            elif(iteration_robs[int(robotId%8)] == 5):  # fin de lst_individual(pour robot_n°[robotId])
                if(int(iteration_global%40) == 0):      # fin de lst_individual(pour 8 robots)
                    population.append(lst_individual)   # registre la population de lst_individual[]
                    lst_individual = [[] for _ in range(8)] # prépare d'initialiser une nouvelle lst_individual[]
                iteration_robs[int(robotId%8)] = 0      # prépare de registre une nouvelle série de mouvement pour robot_n°[robotId]
                initial_lst_individual(int(robotId%8), translation, rotation)   # registre ce mouvement
        else:   # on a créé une population, commence à faire l'opérateur de sélection et de mutation
            population.append(lst_individual)
            #if(len(population) == 4):   # pour indiquer qu'on a déjà fait l'initialisation (c-à-d 1ème fois de population totale)
            flag_initial = True
            lst_individual = [[] for _ in range(8)]     # prépare d'initialiser une nouvelle lst_individual[]
            iteration_robs[int(robotId)] = 0            # prépare de registre une nouvelle série de mouvement pour robot_n°[robotId]
            genetic_algorithm()
            iteration_global -= 80    # car on a (5*8=40) iterations reste pour lst_individual num_0 
            if(not(lst_flag[int(robotId%8)])):  # on copie les stratégies de l'algo génétique               
                tmp = random.randint(0, 1)            
                (translation, rotation) = population[tmp][int(robotId%8)][iteration_robs[int(robotId%8)]]
            initial_lst_individual(int(robotId%8), translation, rotation)
    else:
        if(int(iteration_global%160)!=0 or iteration_global == 0):  # initial of generate indivitual:
            if(iteration_robs[int(robotId%8)] < 5): 
                if(not(lst_flag[int(robotId%8)])):  # on copie les stratégies de l'algo génétique               
                    tmp = random.randint(0, 1)            
                    (translation, rotation) = population[tmp][int(robotId%8)][iteration_robs[int(robotId%8)]]
                initial_lst_individual(int(robotId%8), translation, rotation)
            elif(iteration_robs[int(robotId%8)] == 5):
                if(int(iteration_global%40) == 0):    # fin de lst_individual
                    population.append(lst_individual)
                    lst_individual = [[] for _ in range(8)]
                iteration_robs[int(robotId%8)] = 0
                if(not(lst_flag[int(robotId%8)])):  # on copie les stratégies de l'algo génétique   
                    tmp = random.randint(0, 1)            
                    (translation, rotation) = population[tmp][int(robotId%8)][iteration_robs[int(robotId%8)]]
                lst_flag[int(robotId%8)] = False
                initial_lst_individual(int(robotId%8), translation, rotation)
        else:   # on a créé une population, commence à faire l'opérateur de sélection et de mutation
            population.append(lst_individual)
            lst_individual = [[] for _ in range(8)]
            iteration_robs[int(robotId)] = 0
            genetic_algorithm()
            iteration_global -= 80    # car on a (5*8=40) iterations reste pour lst_individual num_0 
            if(not(lst_flag[int(robotId%8)])):  # on copie les stratégies de l'algo génétique               
                tmp = random.randint(0, 1)            
                (translation, rotation) = population[tmp][int(robotId%8)][iteration_robs[int(robotId%8)]]  
            initial_lst_individual(int(robotId%8), translation, rotation)


    return translation, rotation


def calcul_score(robotId, translation, rotation, iteration_global):
    global score_individual
    #print("score_individual =: ", score_individual)
    #print("iteration_global=: ", iteration_global, "\titeration_global/40=: ", int(iteration_global/40))
    score_individual[int(robotId%8)][int(iteration_global/40)] += translation * (1 - abs(rotation))
    # print(f"Score of the {int(robotId%8)}th robot is:= {score_individual[int(robotId%8)]}")
    return score_individual

def initial_lst_individual(num_rob, translation, rotation):
    global lst_individual, iteration_global
    lst_individual[num_rob].append((translation, rotation))
    calcul_score(num_rob, translation, rotation, iteration_global)
    iteration_robs[num_rob] += 1
    iteration_global += 1
    return
def mutation(individual_rob):
    index = random.randint(0, 4)
    #(tmp_a, tmp_b) = individual_rob[index]
    individual_rob[index] = (random.uniform(-1, 1), random.uniform(-1, 1))    # translation: max = t + 0.2(9); min = t - 0.3, rotation: max = r + 0.(9);s min = r - 1 
    return individual_rob
    
def recombinaison(parent1, parent2):
    point = random.randint(2, 6)
    ind_rob = parent1[:point] + parent2[point:]
    return ind_rob

def genetic_algorithm():
    global score_individual, iteration_robs, lst_individual, population

    for num_rob in range(0, 8):
        score_tmp = 0
        max_num_ind = 0
        second_num_ind = 0
        for i in range(len(score_individual[num_rob])):
            if(score_individual[num_rob][i] > score_individual[num_rob][max_num_ind]):  #sélectionner le meilleur individual
                max_num_ind = i
            elif(score_individual[num_rob][i] < score_individual[num_rob][max_num_ind] and score_individual[num_rob][i] > score_individual[num_rob][second_num_ind]):
                second_num_ind = i
        population[0][num_rob] = recombinaison(population[max_num_ind][num_rob], population[second_num_ind][num_rob])
        population[0][num_rob] = mutation(population[0][num_rob])   

        population[1][num_rob] = [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]
        for i in range(0, 5):
            (tmp_trans, tmp_rotat) = population[0][num_rob][i]
            score_tmp += tmp_trans * (1 - abs(tmp_rotat))
        score_individual[num_rob][0] = score_tmp
        for i in range(0, 5):
            (tmp_trans, tmp_rotat) = population[1][num_rob][i]
            score_tmp += tmp_trans * (1 - abs(tmp_rotat))
        score_individual[num_rob][1] = score_tmp
        for i in range(2, 4):
            score_individual[num_rob][i] = 0
    # for i in range(len(population)):
    #     print(f"population[{i}]:= ", population[i])
    for i in range(0, 2):
        population.pop()
        # print(f"delect [{i}] ème fois")
    #     for i in range(len(population)):
    #         print(f"population[{i}]:= ", population[i])
    # print("#######################################")
    # for i in range(len(population)):
    #         print(f"population[{i}]:= ", population[i])

    
