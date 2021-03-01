from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from random import uniform
import math
import time
import numpy as np
#from cto.random_walk import RandomWalker


class PassagerAgent(Agent):
    unique_id = 't_'
    destination = None
    speed = 1

    def __init__(self, unique_id, pos, model,target_speed, destination = None, old_position = None, ):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.destination = destination
        self.old_position = old_position
        self.speed = target_speed

    def step(self):
        self.move()
    
    def move(self):
        #print("dest: {}".format(self.destination))
        if (self.destination is False or self.destination is None or self.pos == self.destination):
            self.destination = self.new_destination()
        self.trace_next_move()
        
        if ( self.old_position != self.pos):
            print("pos: {} ".format(self.pos))
            _x, _y = self.pos
            self.model.grid.move_agent(self, self.correction_pos(_x, _y))

class ElevatorAgent(Agent):
    unique_id = 'e_'

    def __init__(self, unique_id, pos, model, sensor_range, multiplication_factor):
        super().__init__(unique_id, model)
        self.pos = pos
        self.under_observation = {}
        self.unique_id = unique_id
        self.sensor_range = sensor_range
        self.multiplication_factor = multiplication_factor
        self.destination = []
        
    def step(self):
        if (self.model.observers_indications.size != 0):
            self.destination = self.closer()
            self.move()
        else:
            self.move()

    def move(self):
        new_position = self.trace_next_move()
        self.model.grid.move_agent(self, new_position)
        ## verify field of view
        self.under_observation = self.check_fov()      


    def check_fov(self):
        in_fov = self.model.grid.get_neighbors(
                    self.pos,
                    int(self.sensor_range))
        return in_fov
    
    #verify indication closer to observer  
    def closer(self):
        dist = self.model.grid.height + self.model.grid.width + 100
        key = 0
        closer = []
        i = 0
        for point_indication in self.model.observers_indications:
            x1, y1 = self.pos
            x2 = math.floor(point_indication[0])
            y2 = math.floor(point_indication[1])
            #d =  self.model.grid.get_distance(self.pos, point_indication)
            d = math.sqrt( ((x1-x2)**2)+((y1-y2)**2))
            if (d <= dist):
                dist = d
                key = i
                closer = point_indication
            i += 1
        
        #print (closer, self.pos, self.model.observers_indications)
        #remove
        self.model.observers_indications = np.delete(self.model.observers_indications, key, 0)
        #return         
        return (math.floor(closer[0]), math.floor(closer[1]))

    def trace_next_move(self):
        x_pos, y_pos = self.pos
        x_dest, y_dest = self.destination
        if (x_dest > x_pos):
            x = x_pos + 1
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        elif (x_dest < x_pos):
            x = x_pos - 1
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        else:
            x = x_pos
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        return (x ,y)