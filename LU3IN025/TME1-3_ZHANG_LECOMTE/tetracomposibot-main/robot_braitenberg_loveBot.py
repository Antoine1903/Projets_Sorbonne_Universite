from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "LoveBot"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        sensor_to_robot = [1.0 if sensor_view[i] != 2 else sensors[i] for i in range(8)]

        translation = 1 - 0.8 * (sensor_to_robot[sensor_front] < 0.3)
        rotation = sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right]

        translation = max(-1, min(translation, 1))
        rotation = max(-1, min(rotation, 1))

        return translation, rotation, False
