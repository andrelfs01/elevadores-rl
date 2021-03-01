from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from agents import ElevatorAgent, PassagerAgent

from random import uniform
import math
from pandas import DataFrame
import numpy as np
import time

class Modelo(Model):
    """
    A model with some number of agents.
    """
    atendidos=0
    num_elevators=1
    num_floors=15
    a=1

    def __init__(self, elevators=4, floors=16, a = 0, passager_flow='radom'):
        super().__init__()
        #self.running = True
        self.num_elevators = elevators
        self.num_floors = floors
        self.grid = MultiGrid(int(elevators+1), int(floors*3), False)
        self.schedule = RandomActivation(self)
        self.a = a
                
        self.verbose = False  # Print-monitoring


#        self.datacollector = DataCollector(
#            {"Wolves": lambda m: m.schedule.get_breed_count(Wolf),
#             "Sheep": lambda m: m.schedule.get_breed_count(Sheep)})

        # Create elevators
        for i in range(self.num_elevators):
            # Add the agent to a random grid cell
            a = ElevatorAgent("e_"+str(i), (i+1, 0), self)
            self.schedule.add(a)
            
            self.grid.place_agent(a, (i+1, 0))

        self.datacollector = DataCollector(
            model_reporters={"Observation": "mean_observation"})


    def step(self):
        #aqui vai a logica do fluxo de passageiros
        while(True):
            self.schedule.step()
            #print(self.schedule.get_agent_count)
            self.datacollector.collect(self)

    def run_model(self, step_count=2000):

        if self.verbose:
            print('Initial number targets: ',
                  self.num_agents)
            print('Initial number observers: ',
                  self.num_observer_agents)

        for i in range(step_count):
            self.step()