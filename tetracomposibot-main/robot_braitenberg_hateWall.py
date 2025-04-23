from robot import * 
import random

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "HateWall"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.memory = random.randint(0, 1)  # Direction préférée initiale : 0 = gauche, 1 = droite
        self.stuck_counter = 0              # Compteur pour détecter les blocages face au mur
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range(8):
            if sensor_view[i] == 1:
                sensor_to_wall.append(sensors[i])
                sensor_to_robot.append(1.0)
            elif sensor_view[i] == 2:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(sensors[i])
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        if debug and self.iteration % 100 == 0:
            print("Robot", self.robot_id, "(team " + str(self.team_name) + ")", "at step", self.iteration, ":")
            print("\tsensors (distance, max is 1.0)  =", sensors)
            print("\t\tsensors to wall  =", sensor_to_wall)
            print("\ttype (0:empty, 1:wall, 2:robot) =", sensor_view)
            print("\trobot's name (if relevant)      =", sensor_robot)
            print("\trobot's team (if relevant)      =", sensor_team)

        # Détection de mur en face (ou trop proche)
        if sensor_to_wall[sensor_front] < 0.3:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0

        # Si bloqué plusieurs étapes de suite, changer de direction préférée
        if self.stuck_counter > 5:
            self.memory = 1 - self.memory  # Alterner entre gauche et droite
            self.stuck_counter = 0

        # Calcul de la rotation (éviter les murs à gauche/droite) + influence de la mémoire
        rotation_weight = 1.5
        rotation = (
            (-rotation_weight) * (1.0 - sensor_to_wall[sensor_front_left]) +
            (rotation_weight) * (1.0 - sensor_to_wall[sensor_front_right])
        )

        if self.memory == 0:
            rotation -= 0.3  # Biais vers la gauche
        else:
            rotation += 0.3  # Biais vers la droite

        # Translation : plus le robot est proche d’un mur, plus il ralentit
        translation = (
            0.6 * sensor_to_wall[sensor_front] +
            0.2 * sensor_to_wall[sensor_front_left] +
            0.2 * sensor_to_wall[sensor_front_right]
        )

        # Ajouter une légère part de hasard pour éviter de rester coincé
        if random.random() < 0.05:
            rotation += (random.random() - 0.5) * 0.3

        # Limiter les valeurs dans l’intervalle [-1, 1]
        translation = max(-1, min(translation, 1))
        rotation = max(-1, min(rotation, 1))

        self.iteration += 1
        return translation, rotation, False
