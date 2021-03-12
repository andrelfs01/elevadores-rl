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
import json

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

        self.simulation = self.get_simulation('default')

        # Create elevators
        for i in range(self.num_elevators):
            # Add the agent to a random grid cell
            a = ElevatorAgent("e_"+str(i), (i+1, 0), self)
            #seta todos UP
            #
            #estado de todos é 5 (0 =fora d servico, 1 = parado com viagem para baixo, 2 = parado com viagem para cima, 3 = sem missao, 4 = descendo, 5 = subindo)
            self.schedule.add(a)
            
            self.grid.place_agent(a, (i+1, 0))

        self.datacollector = DataCollector(
            model_reporters={"Observation": "mean_observation"})


    def step(self):
        #aqui vai a logica do fluxo de passageiros
        #chegada de passageiros linha 39
        
        #lista de botoes linha 50
        
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

    def get_simulation(self, fluxo):
        #le o arquivo de fluxos
        # simulação:
               
        if fluxo == 'up':
            with open('resources/traff_up.txt', 'r') as f:
                traff_up = json.loads(f.read())
                return traff_up

        elif fluxo == 'dp':
            with open('resources/traff_dp.txt', 'r') as f:
                traff_dp = json.loads(f.read())
                return traff_dp

        elif fluxo == 'du':
            with open('resources/traff_du.txt', 'r') as f:
                traff_du = json.loads(f.read())
                return traff_du
        
        else:
            with open('resources/traff_poisson.txt', 'r') as f:
                traff_poisson = json.loads(f.read())
                return traff_poisson