# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Li Laurrene
#  Prénom Nom No_étudiant/e : Gourdette Beeverly
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

import robot_dumb
import robot_braitenberg_avoider
import robot_braitenberg_loveWall
import robot_braitenberg_loveBot
import robot_braitenberg_hateWall
import robot_braitenberg_hateBot
import robot_subsomption

nb_robots = 0

class Robot_player(Robot):

    team_name = "Pacman"  
    robot_id = -1               
    memory = 0                

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        # == Les robots sont rapides et n'ont pas tous la même stratégie == #

        translation = 0.8
        rotation = 0 
    
        # Les premiers robots ont pour rôle de suivre les ennemis
        if self.id >= 1:
            
            for i in range(8):
                
                # Si on atteint un mur, on cherche à l'éviter à tout prix : 
                if sensor_view[i] == 1:
                            translation = 0.8
                            rotation = (
                                sensors[sensor_front_right] * (-1) +  
                                sensors[sensor_right] * (-1) +        
                                sensors[sensor_rear_right] * (-1) + 
                                
                                sensors[sensor_front_left] * (1) +    
                                sensors[sensor_left] * (1) +         
                                sensors[sensor_rear_left] * (1) + 

                                sensors[sensor_front] * (-1) +
                                sensors[sensor_rear] * (1)  
                            )
        
                # Si on approche un robot ennemi, on cherche à le suivre
                if sensor_view[i] == 2  and sensor_team[i] != "Pacman":
                    translation = 0.6
                    rotation = (
                    sensors[sensor_front] * 1 +
                    sensors[sensor_front_right] * 1 +  
                    sensors[sensor_right] * 1 +        
                    sensors[sensor_front_left] * (-1) +  
                    sensors[sensor_left] * (-1) 
                    )   

                # Si on approche un robot de notre équipe, on évite
                if sensor_view[i] == 2 and sensor_team[i] == "Pacman":

                    translation = 0.8
                    rotation = (
                        sensors[sensor_front_right] * (-1) +  
                        sensors[sensor_right] * (-1) +        
                        sensors[sensor_rear_right] * (-1) + 
                        
                        sensors[sensor_front_left] * (1) +    
                        sensors[sensor_left] * (1) +         
                        sensors[sensor_rear_left] * (1) + 

                        sensors[sensor_front] * (-1)  
                        
                    )
                    
                    
        else :
            translation = sensors[sensor_front]*0.1+0.2
            rotation = 0.2 * sensors[sensor_left] + 0.2 * sensors[sensor_front_left] - 0.2 * sensors[sensor_right] - 0.2 * sensors[sensor_front_right] + (random.random()-0.5)*1. #+ sensors[sensor_front] * 0.1

                
        return translation,rotation, False