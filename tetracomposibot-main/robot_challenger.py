# robot_challenger.py

from robot import * 
import robot_braitenberg_hateBot, robot_braitenberg_loveBot, robot_braitenberg_hateWall, robot_subsomption, genetic_algorithms

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger"
    robot_id = -1
    memory = 0
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

        # ✅ 对第3号机器人使用 genetic_algorithms 的实例
        if self.robot_id == 3:
            self.genetic_bot = genetic_algorithms.Robot_player(
                x_0, y_0, theta_0,
                name="GeneticBot", team=self.team_name
            )
            self.genetic_bot.replay_mode = True  # 强制使用最佳策略
        else:
            self.genetic_bot = None

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if self.robot_id == 3:
            # ✅ 调用 genetic_algorithms 的实例的 step 方法
            return self.genetic_bot.step(sensors, sensor_view, sensor_robot, sensor_team)

        # 其他机器人使用 Braitenberg + Subsomption 策略
        if sensor_view is None:
            sensor_view = [0] * 8

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

        # 检测前方是否有机器人
        if (sensor_to_robot[sensor_front] != 1 or 
            sensor_to_robot[sensor_front_left] != 1 or 
            sensor_to_robot[sensor_front_right] != 1):

            if (sensor_team[sensor_front] == self.team or 
                sensor_team[sensor_front_left] == self.team or 
                sensor_team[sensor_front_right] == self.team):

                translation, rotation, _ = robot_braitenberg_hateBot.Robot_player.step(
                    self, sensors, sensor_view, sensor_robot, sensor_team)
            else:
                translation, rotation, _ = robot_braitenberg_loveBot.Robot_player.step(
                    self, sensors, sensor_view, sensor_robot, sensor_team)
        elif (sensor_to_wall[sensor_front] != 1 or 
              sensor_to_wall[sensor_front_left] != 1 or 
              sensor_to_wall[sensor_front_right] != 1):
            translation, rotation, _ = robot_braitenberg_hateWall.Robot_player.step(
                self, sensors, sensor_view, sensor_robot, sensor_team)
        else:
            translation, rotation = 1, 0

        self.iteration += 1
        return translation, rotation, False
