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

nb_robots = 0

class Robot_player(Robot):

    team_name = "Yutoine"  # nom de l'équipe
    robot_id = -1          # Identifiant du robot
    memory = 0             # Mémoire (entier)
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

                sensor_to_wall[sensor_front] * (1) +
                sensor_to_wall[sensor_rear] * (-1) 
            )

            translation = max(-1, min(translation, 1))
            rotation = max(-1, min(rotation, 1))
            return translation, rotation, False

        # --- Couche 2 : interaction avec les robots (alliés ou ennemis) ---
        # Vérifier si un robot est détecté
        if any(sensor_to_robot[i] != 1.0 for i in range(8)):
            if any(sensor_team[i] == "Yutoine" for i in range(8) if sensor_team[i] is not None):
            # Comportement "hateBot" (fuir les robots alliés)
                translation = sensor_to_robot[sensor_front]

                # Rotation pour s'éloigner des robots alliés (tournant dans la direction opposée)
                rotation = (
                    sensor_to_robot[sensor_front_right] * (-1) +  
                    sensor_to_robot[sensor_right] * (-1) +        
                    sensor_to_robot[sensor_rear_right] * (-1) + 
                    
                    sensor_to_robot[sensor_front_left] * (1) +    
                    sensor_to_robot[sensor_left] * (1) +         
                    sensor_to_robot[sensor_rear_left] * (1) +

                    sensor_to_robot[sensor_front] * (1) +
                    sensor_to_robot[sensor_rear] * (-1) 
                )

                translation = max(-1, min(translation, 1))
                rotation = max(-1, min(rotation, 1))
                return translation, rotation, False

            # Comportement "loveBot" (suivre les robots ennemis)
            else:
                translation = 1
                rotation = (
                    sensor_to_robot[sensor_front_right] * (1) +  
                    sensor_to_robot[sensor_right] * (1) +        
                    sensor_to_robot[sensor_rear_right] * (1) + 
                    
                    sensor_to_robot[sensor_front_left] * (-1) +    
                    sensor_to_robot[sensor_left] * (-1) +         
                    sensor_to_robot[sensor_rear_left] * (-1) +

                    sensor_to_robot[sensor_front] * (1) +
                    sensor_to_robot[sensor_rear] * (-1) 
                )
                                
                translation = max(-1, min(translation, 1))
                rotation = max(-1, min(rotation, 1))
                return translation, rotation, False

        # --- Couche 3 : avancer tout droit par défaut ---
        translation = 1  # Avancer tout droit si rien d'autre
        rotation = 0  # Avancer tout droit

        self.iteration += 1
        return translation, rotation, False
