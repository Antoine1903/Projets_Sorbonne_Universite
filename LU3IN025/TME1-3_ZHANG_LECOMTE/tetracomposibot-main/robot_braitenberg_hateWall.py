from robot import *
import random

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "HateWall"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.memory = random.randint(0, 1)  # 0 = gauche, 1 = droite
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        sensor_to_wall = [1.0 if sensor_view[i] != 1 else sensors[i] for i in range(8)]

        rotation = (
            -1.5 * (1.0 - sensor_to_wall[sensor_front_left]) +
            1.5 * (1.0 - sensor_to_wall[sensor_front_right]) +
            0.3 * (self.memory - 0.5)
        )
        translation = (
            0.6 * sensor_to_wall[sensor_front] +
            0.2 * sensor_to_wall[sensor_front_left] +
            0.2 * sensor_to_wall[sensor_front_right]
        )

        self.memory = 1 - self.memory * (sensor_to_wall[sensor_front] < 0.3)

        translation = max(-1, min(translation, 1))
        rotation = max(-1, min(rotation, 1))

        return translation, rotation, False

