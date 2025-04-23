from robot import * 
import random

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "HateBot"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.memory = 0         # Indique si le robot est en mode "évasion"
        self.stuck_counter = 0  # Compteur de détections de blocage frontal
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
            print("Robot", self.robot_id, "(team "+str(self.team_name)+") at step", self.iteration, ":")
            print("\tsensors (distance, max is 1.0)  =", sensors)
            print("\t\tsensors to wall  =", sensor_to_wall)
            print("\t\tsensors to robot =", sensor_to_robot)
            print("\ttype (0:empty, 1:wall, 2:robot) =", sensor_view)
            print("\trobot's name (if relevant)      =", sensor_robot)
            print("\trobot's team (if relevant)      =", sensor_team)

        # === Détection de blocage : si un robot est trop proche devant, incrémenter le compteur ===
        if sensor_to_robot[sensor_front] < 0.3:
            self.stuck_counter += 1
        else:
            self.stuck_counter = max(0, self.stuck_counter - 1)

        # === Si le robot est bloqué plusieurs fois, entrer temporairement en mode "évasion" ===
        if self.stuck_counter > 5:
            self.memory = 10  # Les 10 prochaines itérations appliqueront une stratégie d’évasion
            self.stuck_counter = 0

        # === Comportement par défaut : poursuite du robot devant ===
        if self.memory == 0:
            translation = sensor_to_robot[sensor_front]
            rotation = (
                (-1) * sensor_to_robot[sensor_front_left] +
                (1) * sensor_to_robot[sensor_front_right]
            )
        else:
            # === Mode évasion : marche arrière + rotation aléatoire pour sortir du blocage ===
            translation = -0.3
            rotation = random.choice([-0.8, 0.8])  # Choisit aléatoirement de tourner à gauche ou à droite
            self.memory -= 1

        # Limite les valeurs de translation et rotation
        translation = max(-1, min(translation, 1))
        rotation = max(-1, min(rotation, 1))

        self.iteration += 1
        return translation, rotation, False
