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

    def __init__(self, unique_id, pos, model, destination):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.destination = destination
        self.initial_position = pos

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
    direction = 'UP'

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.destination = []
        self.passageiros = []
        
    def step(self):
        if (self.model.observers_indications.size != 0):
            self.destination = self.closer()
            self.move()
        else:
            self.move()

    def move(self):
        new_position = self.trace_next_move()
        self.model.grid.move_agent(self, new_position)
    
    def trace_next_move(self):
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