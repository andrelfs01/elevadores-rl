from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler #RandomActivation
from mesa.datacollection import DataCollector
import os
from agents_full_state import ElevatorAgent, PassagerAgent, FloorAgent, ControllerAgent
import numpy as np

from random import uniform
import math
from pandas import DataFrame
import numpy as np
import time
import json
import statistics
from datetime import datetime
import sys

def save_file_results(model):
    passagers = model.attended
    if len(passagers) > 0:
        df = DataFrame.from_records([s.to_dict() for s in passagers])
        df["waiting_time"] = (df["boarding_time"] - df["incoming_time"])
        df["journey_time"] = (df["attended_time"] - df["boarding_time"])
        df["total_time"] = (df["attended_time"] - df["incoming_time"])

        #now = datetime.now()
        #df.to_csv('saida_'+model.passager_flow+"_"+now.strftime("%Y-%m-%d_%H:%M")+".csv", index=False, sep=';')
        print(df.head())
        df.to_csv('resultado_'+model.controller+'_'+model.passager_flow+'.csv', header = True, index=False, sep=',')


        #calcula medias e salva em txt
        original_stdout = sys.stdout # Save a reference to the original standard output
        with open('resultado_'+model.controller+'_'+model.passager_flow+".txt", 'w') as f:
            sys.stdout = f # Change the standard output to the file we created.
            cols = ['waiting_time', 'journey_time', 'total_time']
            print(df[cols].mean(axis=0))
            print("alpha: {}".format(model.alpha))
            print("beta: {}".format(model.beta))
            print("theta: {}".format(model.theta))
            print("crowding:{}".format(get_crowding(model)))
            sys.stdout = original_stdout # Reset the standard output to its original value

def get_floors(model):
    total = 0
    for f in model.floors:
        total = total + len(f.passageiros)
    return total
    
def get_cars(model):
    total = 0
    for e in model.elevators:
        total = total + len(e.passageiros)
    return total

def get_journey_time(model):
    times = []
    for p in model.attended:
        times.append(p.attended - p.boarding)
    if len(times) < 1:
        return 0
    return statistics.mean(times)

def get_waiting_time(model):    
    times = []
    for p in model.attended:
        times.append(p.boarding - p.incoming)
    if len(times) < 1:
        return 0
    return statistics.mean(times)

def get_waiting_floor(model):    
    times = []
    for f in model.floors:
        for p in f.passageiros:
            times.append(model.schedule.time - p.incoming)
    if len(times) < 1:
        return 0
    return statistics.mean(times)

def get_total_time(model):    
    times = []
    for p in model.attended:
        times.append(p.attended - p.incoming)
    if len(times) < 1:
        return 0
    return statistics.mean(times)

def get_attended(model):
    return len(model.attended)

# def get_crowding(model):    
#     crowd = []
#     for p in model.attended:
#         crowd.append(p.crowding)
#     if len(crowd) < 1:
#         return 0
#     return statistics.mean(crowd)
def get_crowding(model):
    if len(model.crowding_history) == 0:
        return 0

    numerador = [x for x in model.crowding_history if x >= 0.5]
    numerador = sum(numerador * 15)
    denominador = sum(model.crowding_history * 15)
       
    return numerador/denominador

class Modelo(Model):
    """
    A model with some number of agents.
    """
    atendidos=0
    num_elevators=1
    num_floors=15
    a=1
    floors = []
    elevators = []
    attended = []
    gerado_saida = False
    crowding_history = []

    def __init__(self, elevators=4, floors=16, a = 0, passager_flow='up', controller='baseline', alpha = 1, beta = 1, theta = 1, output_file = False):
        super().__init__()
        #self.running = True
        self.num_elevators = int(elevators)
        self.num_floors = int(floors)
        self.grid = MultiGrid(int(elevators)+1, (int(floors)), False)
        self.schedule = BaseScheduler(self)
        self.a = a
        self.between_floors = 2
        self.verbose = False  # Print-monitoring
        self.floors = []
        self.elevators = []
        self.attended = []
        self.passager_flow = passager_flow
        self.simulation = self.get_simulation(passager_flow)
        self.alpha = alpha
        self.beta = beta
        self.theta = theta
        self.controller = controller
        self.gerado_saida = not output_file

        print(self.controller, self.alpha, self.beta, self.theta)
        # Create elevators
        for i in range(self.num_elevators):
            # Add the agent to a random grid cell
            a = ElevatorAgent("e_"+str(i), (i+1, 0), self, self.alpha, self.beta, self.theta)
            #seta todos UP
            #
            #estado de todos é 5 (0 =fora d servico, 1 = parado com viagem para baixo, 2 = parado com viagem para cima, 3 = sem missao, 4 = descendo, 5 = subindo)
            self.schedule.add(a)
            self.elevators.append(a)
            self.grid.place_agent(a, (i+1, 0))

        c = ControllerAgent("c_0", self)

        # Create floors
        for i in range(self.num_floors):
            a = FloorAgent("f_"+str(i), i, (0, i), self, c)
            self.schedule.add(a)
            self.grid.place_agent(a, (0, i))
            self.floors.append(a)

        #tempo medio de espera
        #tempo medio de atendimento
        #tempo medio global
        #numero de passageiros em cada andar
        #numero de passageiros em cada carro
        self.datacollector = DataCollector(
            model_reporters={
                "Attended": get_attended,
                "Floors":get_floors,
                "Cars": get_cars,
                "JourneyTime": get_journey_time,
                "WaitingTime": get_waiting_time,
                "TotalTime": get_total_time,
                "WaitingFloor": get_waiting_floor,
                "Crowding": get_crowding
                })

    def step(self):
        #aqui vai a logica do fluxo de passageiros
        #chegada de passageiros 
        
        #lista de botoes
        self.schedule.step()
        print(self.schedule.get_agent_count)
        self.datacollector.collect(self)

        #se nao tem mais passageiros pra chegar nem pra ser atendido
        #cria um csv com os dados
        #so uma vez
        if not self.gerado_saida and self.schedule.time > 2398:
            self.gerado_saida = True
            save_file_results(self)


    def run_model(self, step_count=2400):

        for i in range(step_count):
            self.step()
            print("step: ", i)

    def get_simulation(self, fluxo):
        #le o arquivo de fluxos
        # simulação:
               
        if fluxo == 'up':
            with open('resources/TF1_traff_up.txt', 'r') as f:
                traff_up = json.loads(f.read())
                return traff_up

        elif fluxo == 'dp':
            with open('resources/TF2_traff_dp.txt', 'r') as f:
                traff_dp = json.loads(f.read())
                return traff_dp

        elif fluxo == 'du':
            with open('resources/TF3_traff_du.txt', 'r') as f:
                traff_du = json.loads(f.read())
                return traff_du
        
        else:
            with open('resources/traff_poisson.txt', 'r') as f:
                traff_poisson = json.loads(f.read())
                return traff_poisson


