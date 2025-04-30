# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Antoine Lecomte 21103457
#  Prénom Nom No_étudiant/e : Yuxiang Zhang 21202829
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import *
import math
import random
import csv

nb_robots = 0
debug = False

iteration_global = 0
iteration_robs = [0] * 8    # indique les nombres de fois d'enregistrements de mouvements pour chaque robot (valeur entre [0, 4])
score_individual = [[0, 0, 0, 0] for _ in range(8)]
lst_individual = [[] for _ in range(8)]  # {[(translation, rotation), (..), .. *5 = enregistrer le mouvement de robotId=0], [...], ...*8 = nb de robots par équipe}
population = []
flag_initial = False
lst_flag = [False] * 8

class Robot_player(Robot):

    team_name = "Yutoine"  # nom de l'équipe
    robot_id = -1          # Identifiant du robot
    memory = 0             # Mémoire (entier)
    iteration = 0
    replay_mode = False

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        self.mu = 5
        self.lambda_ = 20
        self.population = [[random.uniform(-1, 1) for _ in range(8)] for _ in range(self.mu)]
        self.fitnesses = [0 for _ in range(self.mu)]
        self.current_candidate = 0
        self.param = self.population[0]
        self.bestParam = self.param.copy()
        self.best_score = -float('inf')
        self.bestTrial = -1

        self.evaluations = 500
        self.it_per_evaluation = 400
        self.subtrial_per_evaluation = 3
        self.trial = 0
        self.total_score = 0
        self.subtrial = 0

        self.coverage_grid_size = 20
        self.coverage_grid = set()

        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def reset(self):
        self.theta = random.uniform(0, 2 * math.pi)
        super().reset()
        self.memory = 0  # Réinitialiser la mémoire à chaque reset

    def mutate(self, params):
        child = params.copy()
        for i in range(len(child)):
            if random.random() < 0.3:  # Taux de mutation plus élevé
                child[i] = random.uniform(-1, 1)
        return child

    def selection(self, mu, lambda_, population, fitnesses):
        sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
        parents = [ind for ind, _ in sorted_population[:mu]]
        children = []
        for _ in range(lambda_):
            parent = random.choice(parents)
            child = self.mutate(parent)
            children.append(child)
        return parents + children

    def score(self, param):
        # Simuler le robot avec les paramètres donnés et calculer la couverture
        coverage_score = 0
        for _ in range(self.it_per_evaluation):
            translation = math.tanh(
                param[0] +
                param[1] * random.random() +
                param[2] * random.random() +
                param[3] * random.random()
            )
            rotation = math.tanh(
                param[4] +
                param[5] * random.random() +
                param[6] * random.random() +
                param[7] * random.random()
            )
            coverage_score += translation * (1 - abs(rotation))
        return coverage_score

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        global iteration_robs, lst_individual, iteration_global, population, flag_initial, lst_flag

        if sensor_view is None:
            sensor_view = [0] * 8

        # Analyse des capteurs
        sensor_to_wall = [1.0 if sensor_view[i] != 1 else sensors[i] for i in range(8)]
        sensor_to_robot = [1.0 if sensor_view[i] != 2 else sensors[i] for i in range(8)]

        # --- Couche 1 : éviter les murs (Comportement "hateWall") ---
        if any(sensor_to_wall[i] != 1.0 for i in range(8)):  # Si un mur est détecté
            translation = sensor_to_wall[sensor_front]
            rotation = (
                sensor_to_wall[sensor_front_right] * (-1) +
                sensor_to_wall[sensor_right] * (-1) +
                sensor_to_wall[sensor_rear_right] * (-1) +
                sensor_to_wall[sensor_front_left] * (1) +
                sensor_to_wall[sensor_left] * (1) +
                sensor_to_wall[sensor_rear_left] * (1) +
                sensor_to_wall[sensor_front] * random.randint(-1,1) +
                sensor_to_wall[sensor_rear] * random.randint(-1,1)
            )
            translation = max(-1, min(translation, 1))
            rotation = max(-1, min(rotation, 1))
            return translation, rotation, False

        # --- Couche 2 : interaction avec les robots (alliés ou ennemis) ---
        if any(sensor_to_robot[i] != 1.0 for i in range(8)):
            if any(sensor_team[i] == "Yutoine" for i in range(8) if sensor_team[i] is not None):
                # Comportement "hateBot" (fuir les robots alliés)
                translation = sensor_to_robot[sensor_front]
                rotation = (
                    sensor_to_robot[sensor_front_right] * (-1) +
                    sensor_to_robot[sensor_right] * (-1) +
                    sensor_to_robot[sensor_rear_right] * (-1) +
                    sensor_to_robot[sensor_front_left] * (1) +
                    sensor_to_robot[sensor_left] * (1) +
                    sensor_to_robot[sensor_rear_left] * (1) +
                    sensor_to_robot[sensor_front] * random.randint(-1,1) +
                    sensor_to_robot[sensor_rear] * random.randint(-1,1) 
                )
                translation = max(-1, min(translation, 1))
                rotation = max(-1, min(rotation, 1))
                return translation, rotation, False
            else:
                # Comportement "loveBot" (suivre les robots ennemis)
                translation = 1
                rotation = (
                    sensor_to_robot[sensor_front_right] * (1) +
                    sensor_to_robot[sensor_right] * (1) +
                    sensor_to_robot[sensor_rear_right] * (1) +
                    sensor_to_robot[sensor_front_left] * (-1) +
                    sensor_to_robot[sensor_left] * (-1) +
                    sensor_to_robot[sensor_rear_left] * (-1)
                )
                translation = max(-1, min(translation, 1))
                rotation = max(-1, min(rotation, 1))
                return translation, rotation, False

        # --- Couche 3 : algorithme génétique ---
        if not self.replay_mode and self.iteration % self.it_per_evaluation == 0:
            if self.iteration > 0:
                coverage_score = len(self.coverage_grid)
                trial_score = coverage_score
                self.total_score += trial_score

                print(f"\n[Trial {self.trial} - Subtrial {self.subtrial}/{self.subtrial_per_evaluation}] Score: {trial_score}")
                print("\tCouverture =", coverage_score)

            self.subtrial += 1
            self.coverage_grid.clear()

            if self.subtrial == self.subtrial_per_evaluation:
                print(f"\n>>> Trial {self.trial}/{self.evaluations} completed: Total score = {self.total_score}")
                print(f"    Params: {self.param}")

                if self.total_score > self.best_score:
                    self.best_score = self.total_score
                    self.bestParam = self.param.copy()
                    self.bestTrial = self.trial
                    print(">>> New best strategy found!")
                    print(">>> Best score =", self.best_score)

                mode = 'w' if self.trial == 0 else 'a'
                with open('genetic_algorithm_results.csv', mode, newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([self.trial, self.total_score, self.best_score] + self.bestParam)
                    file.flush()

                self.fitnesses[self.current_candidate] = self.total_score
                self.trial += 1
                self.total_score = 0
                self.subtrial = 0

                if self.trial >= self.evaluations:
                    print("\n[INFO] All evaluations done. Entering replay mode.")
                    print(">>> FINAL BEST STRATEGY from trial", self.bestTrial)
                    print(">>> Parameters:", self.bestParam)
                    print(">>> Score:", self.best_score)
                    self.param = self.bestParam.copy()
                    self.replay_mode = True
                else:
                    if self.trial % self.lambda_ == 0:
                        self.population = self.selection(self.mu, self.lambda_, self.population, self.fitnesses)
                        self.fitnesses = [0 for _ in range(self.mu)] + [0 for _ in range(self.lambda_)]
                        print(f"[GENERATION {self.trial // self.lambda_}] Nouvelle population sélectionnée")

                    self.current_candidate = (self.trial % (self.mu + self.lambda_)) % len(self.population)
                    self.param = self.population[self.current_candidate]
                    print("\nTrying new strategy, trial", self.trial)

            self.reset()
            self.iteration += 1
            return 0, 0, True

        cell_x = int(self.x * self.coverage_grid_size)
        cell_y = int(self.y * self.coverage_grid_size)
        self.coverage_grid.add((cell_x, cell_y))

        translation = math.tanh(
            self.param[0] +
            self.param[1] * sensors[sensor_front_left] +
            self.param[2] * sensors[sensor_front] +
            self.param[3] * sensors[sensor_front_right]
        )

        rotation = math.tanh(
            self.param[4] +
            self.param[5] * sensors[sensor_front_left] +
            self.param[6] * sensors[sensor_front] +
            self.param[7] * sensors[sensor_front_right]
        )

        self.iteration += 1

        if debug and self.iteration % 100 == 0:
            print("Robot", self.robot_id, "(team", self.team_name + ")", "at step", self.iteration)
            print("\tsensors =", sensors)
            print("\ttranslation =", translation, "; rotation =", rotation)

        return translation, rotation, False
