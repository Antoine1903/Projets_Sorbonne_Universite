# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Antoine Lecomte 21103457
#  Prénom Nom No_étudiant/e : Yuxiang Zhang 
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import robot_braitenberg_hateBot, robot_braitenberg_loveBot, robot_braitenberg_hateWall, robot_subsomption, genetic_algorithms

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if sensor_view is None:
            sensor_view = [0] * 8

        # Analyse des capteurs
        sensor_to_wall = [1.0 if sensor_view[i] != 1 else sensors[i] for i in range(8)]
        sensor_to_robot = [1.0 if sensor_view[i] != 2 else sensors[i] for i in range(8)]

        # Couche 1 : éviter les murs (prioritaire)
        if any(sensor_to_wall[i] != 1.0 for i in range(8)):
            return robot_braitenberg_hateWall.Robot_player.step(
                self, sensors, sensor_view, sensor_robot, sensor_team)

        # Couche 2 : interaction avec les robots (alliés ou ennemis)
        if any(sensor_to_robot[i] != 1.0 for i in range(8)):
            if any(sensor_team[i] == self.team for i in range(8) if sensor_team[i] is not None):
                return robot_braitenberg_hateBot.Robot_player.step(
                    self, sensors, sensor_view, sensor_robot, sensor_team)
            else:
                return robot_braitenberg_loveBot.Robot_player.step(
                    self, sensors, sensor_view, sensor_robot, sensor_team)


        # --- Couche 3 : comportement par défaut si rien détecté
        # Si rien n'est détecté, avancer droit
        return 1, 0, False
