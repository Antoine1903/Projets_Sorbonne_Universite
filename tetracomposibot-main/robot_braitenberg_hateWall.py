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
        self.memory = random.randint(0, 1)  # 初始偏好方向：0 = 左偏, 1 = 右偏
        self.stuck_counter = 0
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

        # 检测是否正前方卡墙（或太接近）
        if sensor_to_wall[sensor_front] < 0.3:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0

        # 如果连续多帧都卡住，切换偏好方向
        if self.stuck_counter > 5:
            self.memory = 1 - self.memory  # 左右切换
            self.stuck_counter = 0

        # 计算 rotation（左右避障）+ memory 影响（偏向某边）
        rotation_weight = 1.5
        rotation = (
            (-rotation_weight) * (1.0 - sensor_to_wall[sensor_front_left]) +
            (rotation_weight) * (1.0 - sensor_to_wall[sensor_front_right])
        )

        if self.memory == 0:
            rotation -= 0.3  # 偏左
        else:
            rotation += 0.3  # 偏右

        # translation 越靠近墙越慢
        translation = (
            0.6 * sensor_to_wall[sensor_front] +
            0.2 * sensor_to_wall[sensor_front_left] +
            0.2 * sensor_to_wall[sensor_front_right]
        )

        # 加点小随机性避免卡角落
        if random.random() < 0.05:
            rotation += (random.random() - 0.5) * 0.3

        # 限制值范围
        translation = max(-1, min(translation, 1))
        rotation = max(-1, min(rotation, 1))

        self.iteration += 1
        return translation, rotation, False
