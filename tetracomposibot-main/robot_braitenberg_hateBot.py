from robot import *
import random

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "HateBot"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.memory = 0
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        sensor_to_robot = [1.0 if sensor_view[i] != 2 else sensors[i] for i in range(8)]
        robot_team = [None if sensor_view[i] != 2 else sensor_team[i] for i in range(8)]

        stuck = sensor_to_robot[sensor_front] < 0.3 and robot_team[sensor_front] == self.team
        if stuck:
            self.memory = 3

        if self.memory > 0:
            self.memory -= 1
            return -0.3, random.choice([-0.8, 0.8]), False

        translation = sensor_to_robot[sensor_front]
        rotation = (-1) * sensor_to_robot[sensor_front_left] + (1) * sensor_to_robot[sensor_front_right]

        return max(-1, min(translation, 1)), max(-1, min(rotation, 1)), False