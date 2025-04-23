# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : _________
#  Prénom Nom No_étudiant/e : _________
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

        if self.robot_id == 3:
            self.genetic_bot = genetic_algorithms.Robot_player(
                x_0, y_0, theta_0,
                name="GeneticBot", team=self.team_name
            )
            self.genetic_bot.replay_mode = True
        else:
            self.genetic_bot = None

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if self.robot_id == 3:
            return self.genetic_bot.step(sensors, sensor_view, sensor_robot, sensor_team)

        if sensor_view is None:
            sensor_view = [0] * 8

        # Analyse des capteurs
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range(8):
            if sensor_view[i] == 1:  # Wall
                sensor_to_wall.append(sensors[i])
                sensor_to_robot.append(1.0)
            elif sensor_view[i] == 2:  # Robot
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(sensors[i])
            else:  # Empty
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # --- Couche 1 : éviter les murs (prioritaire)
        if (sensor_to_wall[sensor_front] != 1 or 
            sensor_to_wall[sensor_front_left] != 1 or 
            sensor_to_wall[sensor_front_right] != 1):
            return robot_braitenberg_hateWall.Robot_player.step(
                self, sensors, sensor_view, sensor_robot, sensor_team)

        # --- Couche 2 : si robots détectés devant
        if (sensor_to_robot[sensor_front] != 1 or 
            sensor_to_robot[sensor_front_left] != 1 or 
            sensor_to_robot[sensor_front_right] != 1):

            # Si au moins un est un allié → éviter (hateBot)
            if (sensor_team[sensor_front] == self.team or 
                sensor_team[sensor_front_left] == self.team or 
                sensor_team[sensor_front_right] == self.team):
                return robot_braitenberg_hateBot.Robot_player.step(
                    self, sensors, sensor_view, sensor_robot, sensor_team)
            else:
                # Sinon, aller vers les ennemis (loveBot)
                return robot_braitenberg_loveBot.Robot_player.step(
                    self, sensors, sensor_view, sensor_robot, sensor_team)

        # --- Couche 3 : comportement par défaut si rien détecté
        return 1, 0, False
