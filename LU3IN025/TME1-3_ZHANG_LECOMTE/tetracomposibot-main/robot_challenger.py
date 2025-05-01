# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Antoine Lecomte 21103457
#  Prénom Nom No_étudiant/e : Yuxiang Zhang 21202829

from robot import *
import math
import random
import csv

nb_robots = 0
debug = False

class Robot_player(Robot):
    team_name = "Yutoine"
    robot_id = -1
    memory = 0
    iteration = 0

    # Genetic Algorithm parameters
    param = []
    bestParam = []
    best_score = -float('inf')
    current_score = 0
    bestTrial = -1
    total_score = 0

    evaluations = 10000  # Reduced for practical training
    it_per_evaluation = 5000  # Increased steps per evaluation
    subtrial_per_evaluation = 1
    trial = 0
    subtrial = 0

    # Coverage tracking
    visited_cells = set()
    cell_size = 0.5
    log_sum_of_translation = 0
    log_sum_of_rotation = 0
    last_position = (0, 0)  # For actual movement tracking

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        # Initialize GA parameters with biased start
        self.param = [
            random.choice([-1, 0, 1]),  # Front weight (positive)
            random.choice([-1, 0, 1]),  # Front-left
            random.choice([-1, 0, 1]),  # Front-right
            random.choice([-1, 0, 1]),
            random.choice([-1, 0, 1]),
            random.choice([-1, 0, 1]),
            random.choice([-1, 0, 1]),
            random.choice([-1, 0, 1])
        ]
        self.bestParam = self.param.copy()
        
        # Initialize position tracking
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.visited_cells = set()
        self.last_position = (x_0, y_0)
        self.total_score = 0
        
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def reset(self):
        """Reset robot position and tracking metrics"""
        self.theta = random.uniform(0, 2 * math.pi)
        self.log_sum_of_translation = 0
        self.log_sum_of_rotation = 0
        self.last_position = (self.x, self.y)
        super().reset()

    def update_coverage(self, x, y):
        """Track visited cells for coverage calculation"""
        cell_x = int(x / self.cell_size)
        cell_y = int(y / self.cell_size)
        self.visited_cells.add((cell_x, cell_y))

    def calculate_coverage_score(self):
        """Calculate normalized coverage score"""
        max_cells = (20 / self.cell_size) * (20 / self.cell_size)
        return len(self.visited_cells) / max_cells
    
    def mutate(self, params, mutation_rate=0.5):
        """Enhanced mutation operator with adaptive rate"""
        child = params.copy()
        for i in range(len(child)):
            if random.random() < mutation_rate:
                original = child[i]
                # More aggressive mutation
                child[i] = random.choice([-1, -0.5, 0, 0.5, 1, original*1.2])
                child[i] = max(-1, min(1, child[i]))  # Clamp to [-1,1]
        return child
    
    def evaluate_params(self, params):
        """Score function focusing on coverage (90%) and movement efficiency (10%)"""
        coverage = self.calculate_coverage_score()
        efficiency = 1 - abs(self.log_sum_of_rotation/self.it_per_evaluation)
        return coverage * 0.9 + efficiency * 0.1

    def selection(self, population):
        """μ+λ selection (μ=5, λ=20)"""
        evaluated = [(p, self.evaluate_params(p)) for p in population]
        evaluated.sort(key=lambda x: -x[1])  # Sort by score descending
        return [x[0] for x in evaluated[:5]]  # Return top 5

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if sensor_view is None:
            sensor_view = [0] * 8

        # Update coverage and track actual movement
        self.update_coverage(self.x, self.y)
        actual_move = math.sqrt((self.x - self.last_position[0])**2 + 
                               (self.y - self.last_position[1])**2)
        self.log_sum_of_translation += actual_move
        self.last_position = (self.x, self.y)

        if not hasattr(self, 'replay_mode'):
            self.replay_mode = False
        
        # GA evaluation logic
        if not self.replay_mode and self.iteration % self.it_per_evaluation == 0 and self.iteration > 0:
            total_score = self.evaluate_params(self.param)
            self.total_score += total_score
            self.subtrial += 1

            if self.subtrial == self.subtrial_per_evaluation:
                if self.total_score > self.best_score:
                    self.best_score = self.total_score
                    self.bestParam = self.param.copy()
                
                # μ+λ selection with adaptive mutation
                current_mutation_rate = 0.5 - 0.4*(self.trial/self.evaluations)
                children = [self.mutate(self.bestParam, current_mutation_rate) for _ in range(20)]
                next_gen = self.selection(children + [self.bestParam]*5)
                
                self.param = random.choice(next_gen)  # Random select from top 5
                self.bestParam = next_gen[0]  # Elite preservation
                
                # Logging
                mode = 'w' if self.trial == 0 else 'a'
                with open('ga_results.csv', mode, newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([self.trial, self.total_score, self.best_score] + self.bestParam)
                
                if debug and self.trial % 50 == 0:
                    print(f"Gen {self.trial}: Score={self.best_score:.2f} "
                          f"Params={self.bestParam} MutRate={current_mutation_rate:.2f}")
                
                self.trial += 1
                self.total_score = 0
                self.subtrial = 0
                
                if self.trial >= self.evaluations:
                    print(f"Optimization complete. Best score: {self.best_score}")
                    print(f"Best params: {self.bestParam}")
                    self.replay_mode = True
                    self.param = self.bestParam.copy()
                
                self.reset()
                return 0, 0, True

        # Sensor processing
        sensor_to_wall = [1.0 if sensor_view[i] != 1 else sensors[i] for i in range(8)]
        sensor_to_robot = [1.0 if sensor_view[i] != 2 else sensors[i] for i in range(8)]

        # Layer 1: Wall avoidance (GA-optimized)
        if any(sensor_to_wall[i] != 1.0 for i in range(8)):
            translation = sensor_to_wall[sensor_front]

            rotation = (
                sensor_to_wall[sensor_front_right] * (-1) +  
                sensor_to_wall[sensor_right] * (-1) +        
                sensor_to_wall[sensor_rear_right] * (-1) + 
                
                sensor_to_wall[sensor_front_left] * (1) +    
                sensor_to_wall[sensor_left] * (1) +         
                sensor_to_wall[sensor_rear_left] * (1) +

                sensor_to_wall[sensor_front] * random.randint(-1,1) +
                sensor_to_wall[sensor_rear] * random.randint(-1,1)
            )

            translation = max(-1, min(translation, 1))
            rotation = max(-1, min(rotation, 1))
            return self.normalize_output(translation, rotation)

        # Layer 2: Robot interaction
        if any(sensor_to_robot[i] != 1.0 for i in range(8)):
            if any(sensor_team[i] == "Yutoine" for i in range(8) if sensor_team[i] is not None):
                # Comportement "hateBot" (fuir les robots alliés)
                translation = sensor_to_robot[sensor_front]
                rotation = (
                    sensor_to_robot[sensor_front_right] * (-1) +  
                    sensor_to_robot[sensor_right] * (-1) +        
                    sensor_to_robot[sensor_rear_right] * (-1) + 
                    
                    sensor_to_robot[sensor_front_left] * (1) +    
                    sensor_to_robot[sensor_left] * (1) +         
                    sensor_to_robot[sensor_rear_left] * (1) +

                    sensor_to_robot[sensor_front] * random.randint(-1,1) +
                    sensor_to_robot[sensor_rear] * random.randint(-1,1) 
                )

            # Comportement "loveBot" (suivre les robots ennemis)
            else:
                translation = sensor_to_robot[sensor_front]
                rotation = (
                    sensor_to_robot[sensor_front_right] * (1) +  
                    sensor_to_robot[sensor_right] * (1) +        
                    sensor_to_robot[sensor_rear_right] * (1) + 
                    
                    sensor_to_robot[sensor_front_left] * (-1) +    
                    sensor_to_robot[sensor_left] * (-1) +         
                    sensor_to_robot[sensor_rear_left] * (-1)
                )

            translation = max(-1, min(translation, 1))
            rotation = max(-1, min(rotation, 1))
            return self.normalize_output(translation, rotation)

        # Layer 3: Default exploration with GA-optimized parameters
        translation = math.tanh(
            self.param[0] +
            self.param[1] * sensors[sensor_front_left] +
            self.param[2] * sensors[sensor_front] +
            self.param[3] * sensors[sensor_front_right]
        )

        rotation = math.tanh(
            self.param[4] +
            self.param[5] * sensors[sensor_front_left] +
            self.param[6] * sensors[sensor_front] +
            self.param[7] * sensors[sensor_front_right]
        )
        return self.normalize_output(translation, rotation)

    def normalize_output(self, translation, rotation):
        """Clip and log movement values"""
        translation = max(-1, min(1, translation))
        rotation = max(-1, min(1, rotation))
        
        self.log_sum_of_rotation += abs(rotation)  # Only log magnitude
        self.iteration += 1
        return translation, rotation, False
