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
    
    

class ElevatorAgent(Agent):
    unique_id = 'e_'
    state = 5

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.destination = []
        self.passageiros = []
        
    def step(self):
        #se chegou no andar
            # verifica se vai parar
            # se for parar 
                # muda para parado descendo ou parado subindo ou sem missao
        #se estiver no andar e parado 
            self.check_leaving()
            self.check_boarding()
            self.check_destination()
            #atualiza o proximo status (subir descer ou sem missao)
            
         
        #se estiver descendo ou subindo
        if (self.state == 4 or self.state == 5):
            self.move()

    def move(self):
        #se estiver parado para embarque desembarque???
        #se estiver subindo pos + 1
            #move todos os passageiros
        #se estiver descendo pos + 1
            #move todos os passageiros
    
    def check_leaving():
        #percorre a lista de passageiros e se for o destino ele sai

    def check_boarding():
        #percorre a lista de passageiros e se for o carro atribuido e sentido certo ele entra

class FloorAgent(Agent):
    number = 0
    up_button = False
    down_button = False
    passageiros = []

    def __init__(self, unique_id, number, model):
        super().__init__(unique_id, model)
        self.number = number
        self.unique_id = unique_id
        self.passageiros = []
        self.up_button = False
        self.down_button = False
        
    def step(self):
        #se chegou passageiro
            #aperta o botao
            #define o carro