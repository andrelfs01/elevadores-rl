from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from random import uniform
import math
import time
import numpy as np
#from cto.random_walk import RandomWalker


class PassagerAgent(Agent):
    unique_id = 'p_'
    destination = None
    initial_position = (0,0)
    car_designed = None
    origem = None
    utilized_car = None
    incoming = -1
    boarding = -1
    attended = -1

    def __init__(self, unique_id, pos, model, origem, destination, incoming):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.destination = destination
        self.initial_position = pos
        self.origem = origem
        self.incoming = incoming

    def step(self):
        pass

    def to_dict(self):
        return {
            'id' : self.unique_id,
            'from': self.origem,
            'to': self.destination,
            'car': self.utilized_car.unique_id,
            'incoming_time': self.incoming,
            'boarding_time': self.boarding,
            'attended_time': self.attended
        }

class ElevatorAgent(Agent):
    unique_id = 'e_'
    state = 3
    cont = 0

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.destination = []
        self.passageiros = []
        self.cont = 0
        
    def step(self):
        #se esta movendo, continua
        if (self.state == 4 or self.state == 5) and self.cont != 0:
            self.move()

        #se chegou no andar
        elif (self.pos[1] % 2 == 0 and (self.state == 4 or self.state == 5) and self.cont == 0):
            actual_floor = self.pos[1] / 2 
            # verifica se vai parar
            if (actual_floor in self.destination):
                #tira dos destinos
                print("antes",self.destination)
                while (actual_floor in self.destination):
                    self.destination.remove(actual_floor)
                print("depois",self.destination)
                # muda para parado descendo ou parado subindo
                if (self.state == 4):
                    if (actual_floor == 0):
                        self.state = 3
                    else: 
                        self.state = 1
                #se esta subindo
                else:
                    if (actual_floor == len(self.model.elevators)):
                        self.state = 3
                    else: 
                        self.state = 2
            else:
                self.move()        
                             
        #se estiver no andar e parado 
        elif (self.pos[1] % 2 == 0 and (self.state == 1 or self.state == 2 or self.state == 3)):
            self.check_leaving()
            self.check_boarding()
            self.check_destination()
            #atualiza o proximo status (subir descer ou sem missao)
            
        #se estiver descendo ou subindo
        elif (self.pos[1] % 2 != 0 and (self.state == 4 or self.state == 5)):
            self.move()

    def move(self):

        #se estiver subindo pos + 1
        new_pos = self.pos
        x, y = self.pos
        if (self.state == 4 ):
            if (self.pos[1] == 0):
                self.state = 3
                return 0

            self.cont += 1
            if self.cont == (self.model.between_floors/2):
                new_pos = x, y - 1
                self.cont = 0
        
        #se estiver descendo pos + 1
        if (self.state == 5 ):
            if (self.pos[1] == self.model.grid.height - 1):
                self.state = 3
                return 0

            print("cont: {}".format(self.cont, self.model.between_floors/2))
            self.cont += 1
            if self.cont == (self.model.between_floors/2):
                new_pos = x, y + 1
                self.cont = 0

        #move todos os passageiros
        for p in self.passageiros:
            p.model.grid.move_agent(p, new_pos)
        self.model.grid.move_agent(self, new_pos)
        
    
    def check_leaving(self):
        '''
            check if
        '''
        actual_floor = self.pos[1] / 2 
        remover = []
        for p in self.passageiros:
            if p.destination == actual_floor:
                print("saindo passageiro", p.unique_id)
                remover.append(p)
                self.model.grid.remove_agent(p)
                self.model.schedule.remove(p)
                p.attended = self.model.schedule.time
                self.model.attended.append(p)
        for p in remover:
            self.passageiros.remove(p)

    def check_boarding(self):
        actual_floor = self.pos[1] / 2 
        for f in self.model.floors:
            if f.number == actual_floor:
                remover = []
                for p in f.passageiros:
                    #se for o carro atribuido
                    # ou se o  carro vai na mesma rota
                    print("EMBARCA?")
                    if (p.car_designed == self or (self.state == 3) or (self.state in (1,4) and p.destination < p.origem) or (self.state in (2,5) and p.destination > p.origem)) and len(self.passageiros) < 15:
                        #se o carro esta ok, embarca
                        if (self.state != 0):
                            print("embarque")
                            p.utilized_car = self
                            p.model.grid.move_agent(p, self.pos)
                            p.boarding = self.model.schedule.time
                            self.passageiros.append(p)
                            if p.destination not in self.destination:
                                self.destination.append(p.destination)
                            remover.append(p)
                    else:
                        print("nao embarcou *****************")
                        if len(self.passageiros) >= 15:
                            print("lotado *****************")
                print("tinha {} passageiros e embarcaram {}".format(len(f.passageiros), len(remover)))
                
                for p in remover:
                    f.passageiros.remove(p)
                print("ficaram {} passageiros ".format(len(f.passageiros)))            
    
    def check_destination(self):
        print(self.unique_id, self.destination)
        if not self.destination:
            self.state = 3
        else:
            actual_floor = self.pos[1] / 2 
            if self.state == 3:
                if self.destination[0] < actual_floor:
                    self.state = 4
                else:
                    self.state = 5
            elif self.state in (2,5):
                if max(self.destination) > actual_floor:
                    self.state = 5
                else:
                    self.state = 4
            elif self.state in (1,4):
                if min(self.destination) < actual_floor:
                    self.state = 4
                else:
                    self.state = 5
            else:
                actual_floor = self.pos[1] / 2 
                if self.destination[0] == actual_floor and self.cont == 0:
                    self.check_leaving()
                    self.check_boarding()
                    while (actual_floor in self.destination):
                        self.destination.remove(actual_floor)
                    self.check_destination()
                        

class FloorAgent(Agent):
    unique_id = 'f_'
    number = 0
    up_button = False
    down_button = False
    passageiros = []

    def __init__(self, unique_id, number,  pos, model):
        super().__init__(unique_id, model)
        self.number = number
        self.pos = pos
        self.unique_id = unique_id
        self.passageiros = []
        self.up_button = False
        self.down_button = False
        self.flow = self.get_flow(model.simulation)
        self.next_passager = self.flow.pop()
        
    def step(self):
        #se tem algum passageiro sem carro atribuido
        for p in self.passageiros:
            if p.car_designed == -1:
                e = self.select_car(p)
                if e != -1:
                    p.car_designed = e
                    if self.number not in e.destination:
                        e.destination.append(self.number)


        #se chegou passageiro
        if (self.next_passager[1] < self.model.schedule.time):
            #0: id, 1: previsao chegada, 2: setar como chegada, 3: andar origem, 4: andar destino
            #print("andar:",self.number)
            #print("previsao: ",self.next_passager[1])
            #print("origem: ",self.next_passager[3])
            #print("destino: ",self.next_passager[4])
            #print("---------------------")
           
            #cria o passageiro
            p = PassagerAgent("p_"+str(self.next_passager[0]), self.pos, self.model, self.next_passager[3], self.next_passager[4], self.model.schedule.time)
            #define o carro
            e = self.select_car(p)
            if e != -1:
                if self.number not in e.destination:
                    e.destination.append(self.number)
                    p.car_designed = e
            
            self.model.schedule.add(p)
            self.model.grid.place_agent(p, self.pos)
            #add na fila
            self.passageiros.append(p)
            #aperta o botao
            if (self.next_passager[4] > self.number):
                self.up_button = True
            else:
                self.down_button = True

            #proximo
            self.next_passager = self.flow.pop()
        

    def get_flow(self, simulation):
        return simulation[self.number]

    def select_car(self, passager):
        if True:
            return self.baseline(passager)

    def baseline(self, passager):
        #se passageiro subindo
        if passager.destination > passager.origem:
            # se tem carro subindo e em pisso inferior, atribui
            for e in self.model.elevators:
                if (e.state == 2 or e.state == 5) and ((e.pos[1] / 2) < self.number):
                    return e
            
        #se passageiro descendo
        if passager.destination < passager.origem:
            # se tem carro descendo e em pisso superior, atribui
            for e in self.model.elevators:
                if (e.state == 1 or e.state == 4) and ((e.pos[1] / 2) > self.number):
                    return e
        # se nao conseguiu aproveitar um carro em movimento, astribui um carro sem missao
        for e in self.model.elevators:
            if (e.state == 3):
                return e
        
        return -1
