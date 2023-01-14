from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from random import uniform
import math
import time
import numpy as np
from copy import copy
from pessimistic import pessimistic_choice 

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
    
    dist_d = -1
    n_call = -1
    n_floor = -1
    pos_car_call = -1
    dir_car_call = -1
    buttons_car_call = -1
    floor_car_call = -1

    dist_d_deny1 = -1
    n_call_deny1 = -1
    n_floor_deny1 = -1
    pos_car_call_deny1 = -1
    dir_car_call_deny1 = -1
    buttons_car_call_deny1 = -1
    floor_car_call_deny1 = -1


    dist_d_deny2 = -1
    n_call_deny2 = -1
    n_floor_deny2 = -1
    pos_car_call_deny2 = -1
    dir_car_call_deny2 = -1
    buttons_car_call_deny2 = -1
    floor_car_call_deny2 = -1


    dist_d_deny3= -1
    n_call_deny3 = -1
    n_floor_deny3 = -1
    pos_car_call_deny3 = -1
    dir_car_call_deny3 = -1
    buttons_car_call_deny3 = -1
    floor_car_call_deny3 = -1

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
            'attended_time': self.attended,
            'dist_d' : self.dist_d,
            'n_call' : self.n_call,
            'n_floor' : self.n_floor,
            'car_position_call': self.pos_car_call,
            'car_direction_call': self.dir_car_call,
            'car_queue_buttons': self.buttons_car_call,
            'car_queue_floor': self.floor_car_call,
            'dist_d_deny1' : self.dist_d_deny1,
            'n_call_deny1' : self.n_call_deny1,
            'n_floor_deny1' : self.n_floor_deny1,
            'car_position_deny1' : self.pos_car_call_deny1,
            'car_direction_deny1' : self.dir_car_call_deny1,
            'car_queue_buttons_deny1' : self.buttons_car_call_deny1,
            'car_queue_floor_deny1' : self.floor_car_call_deny1,
            'dist_d_deny2' : self.dist_d_deny2,
            'n_call_deny2' : self.n_call_deny2,
            'n_floor_deny2' : self.n_floor_deny2,
            'car_position_deny2' : self.pos_car_call_deny2,
            'car_direction_deny2' : self.dir_car_call_deny2,
            'car_queue_buttons_deny2' : self.buttons_car_call_deny2,
            'car_queue_floor_deny2' : self.floor_car_call_deny2,
            'dist_d_deny3' : self.dist_d_deny3,
            'n_call_deny3' : self.n_call_deny3,
            'n_floor_deny3' : self.n_floor_deny3,
            'car_position_deny3' : self.pos_car_call_deny3,
            'car_direction_deny3' : self.dir_car_call_deny3,
            'car_queue_buttons_deny3' : self.buttons_car_call_deny3,
            'car_queue_floor_deny3' : self.floor_car_call_deny3
        }

    def __getitem__(self,key):
        return getattr(self,key)

    def get_global_state(self, fl, all_elevators):
        if self.car_designed is None:
            print("Erro carro sem carro atribuido")
            quit()
        else:
            contador = 1 
            if (self.destination > fl.number):
                bt = 'up'
            else:
                bt = 'down'

            for el in all_elevators:
                if el != self.car_designed:
                    if contador == 1:
                        self.dist_d_deny1 = fl.dist_d(bt, el)
                        self.n_call_deny1 = len(el.destination)
                        self.n_floor_deny1 = fl.n_floor(bt, el)
                        self.pos_car_call_deny1 =  copy((el.pos[1]))
                        self.dir_car_call_deny1 = copy((el.state))
                        self.buttons_car_call_deny1 = len(list(set(x['destination'] for x in el.passageiros)))
                        self.floor_car_call_deny1 = len(list(x for x in el.destination if x not in list(set(x['destination'] for x in el.passageiros))))
                    elif contador == 2:
                        self.dist_d_deny2 = fl.dist_d(bt, el)
                        self.n_call_deny2 = len(el.destination)
                        self.n_floor_deny2 = fl.n_floor(bt, el)
                        self.pos_car_call_deny2 =  copy((el.pos[1]))
                        self.dir_car_call_deny2 = copy((el.state))
                        self.buttons_car_call_deny2 = len(list(set(x['destination'] for x in el.passageiros)))
                        self.floor_car_call_deny2 = len(list(x for x in el.destination if x not in list(set(x['destination'] for x in el.passageiros))))
                    else:
                        self.dist_d_deny3 = fl.dist_d(bt, el)
                        self.n_call_deny3 = len(el.destination)
                        self.n_floor_deny3 = fl.n_floor(bt, el)
                        self.pos_car_call_deny3 =  copy((el.pos[1]))
                        self.dir_car_call_deny3 = copy((el.state))
                        self.buttons_car_call_deny3 = len(list(set(x['destination'] for x in el.passageiros)))
                        self.floor_car_call_deny3 = len(list(x for x in el.destination if x not in list(set(x['destination'] for x in el.passageiros))))

                    contador = contador + 1

class ElevatorAgent(Agent):
    unique_id = 'e_'
    state = 3
    cont = 0

    def __init__(self, unique_id, pos, model, alpha=0,beta=0,theta=0):
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.destination = []
        self.passageiros = []
        self.cont = 0
        self.alpha = alpha
        self.beta = beta
        self.theta = theta
        
    def step(self):
        #se nao tem destino, para
        if not self.destination and self.state != 3 and self.cont == 0:
            self.state = 3
        #se esta movendo, continua
        if (self.state == 4 or self.state == 5) and self.cont != 0:
            self.move()

        #se chegou no andar
        elif ((self.state == 4 or self.state == 5) and self.cont == 0):
            actual_floor = self.pos[1] 
            # verifica se vai parar
            if (actual_floor in self.destination):
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
        elif ((self.state == 1 or self.state == 2 or self.state == 3) and self.cont == 0):
            leave = self.check_leaving()
            boarding = self.check_boarding()
            self.check_destination()
            #atualiza o proximo status (subir descer ou sem missao)
            #tira dos destinos
            print("antes",self.destination)
            if not leave and not boarding:
                actual_floor = self.pos[1]
                while (actual_floor in self.destination):
                    self.destination.remove(actual_floor)
            print("depois",self.destination)
            
        #se estiver descendo ou subindo
        elif (self.cont != 0 and (self.state == 4 or self.state == 5)):
            self.move()

        else:
            self.check_destination()

    def move(self):

        #se estiver descendo pos + 1
        new_pos = self.pos
        x, y = self.pos
        if (self.state == 4 ):
            if (self.pos[1] == 0):
                self.state = 3
                return 0

            self.cont += 1
            if self.cont == (self.model.between_floors):
                new_pos = x, y - 1
                self.cont = 0
        
        #se estiver subindo pos + 1
        if (self.state == 5 ):
            if (self.pos[1] == self.model.grid.height - 1):
                self.state = 3
                return 0

            print("cont: {}/{}".format(self.cont, self.model.between_floors))
            self.cont += 1
            if self.cont == (self.model.between_floors):
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
        actual_floor = self.pos[1]
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
                return True
        
        return False

    def check_boarding(self):
        actual_floor = self.pos[1] 
        for f in self.model.floors:
            if f.number == actual_floor:
                remover = []
                for p in f.passageiros:
                    #se for o carro atribuido
                    # ou se o  carro vai na mesma rota
                    print("EMBARCA?")
                    if (p.car_designed is None):
                        if (self.state == 3 and len(self.passageiros) < 15):
                            p.car_designed = self
                            p.pos_car_call = copy((self.pos[1]))
                            p.dir_car_call = copy((self.state))
                            p.buttons_car_call = len(list(set(x['destination'] for x in self.passageiros)))
                            p.floor_car_call = len(list(x for x in self.destination if x not in list(set(x['destination'] for x in self.passageiros))))

                            p.get_global_state(f, self.model.elevators)

                            if f.number not in self.destination:
                                self.destination.append(f.number)
                        else:
                            print("sem designado")
                            if (p.destination > f.number):
                                bt = 'up'
                            else:
                                bt = 'down'
                            f.select_car(p, bt)
                    #print ("{} designado | carro {} ".format(p.car_designed.unique_id, self.unique_id))
                    #if (p.car_designed == self or (self.state == 3) or (self.state in (1,4) and p.destination < p.origem) or (self.state in (2,5) and p.destination > p.origem)) and len(self.passageiros) < 15:
                    if (p.car_designed == self and len(self.passageiros) < 15):
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
                            for p in remover:
                                f.passageiros.remove(p)
                            return True
                    else:
                        print("nao embarcou *****************")
                        if len(self.passageiros) >= 15:
                            print("lotado, chamar novamente *****************")
                            p.car_designed = None
                print("tinha {} passageiros e embarcaram {}".format(len(f.passageiros), len(remover)))
                
                for p in remover:
                    f.passageiros.remove(p)
                print("ficaram {} passageiros ".format(len(f.passageiros)))     
                return False       
    
    def check_destination(self):
        print(self.unique_id, self.destination)
        if(not self.destination and self.state != 3):
            print("ver")
        if not self.destination:
            self.state = 3
        else:
            actual_floor = self.pos[1] 
            if self.state == 3 and self.destination:
                if self.destination[0] < actual_floor:
                    self.state = 4
                else:
                    self.state = 5
            elif  self.state in (1,2) and actual_floor in self.destination:
                pass
            elif self.state in (2,5):
                if max(self.destination) > actual_floor:
                    self.state = 5
                elif len(self.destination) > 0:
                    self.state = 4
                else:
                    self.state = 3
            elif self.state in (1,4):
                if min(self.destination) < actual_floor:
                    self.state = 4
                elif len(self.destination) > 0:
                    self.state = 5
                else:
                    self.state = 3
            else:
                actual_floor = self.pos[1] 
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
            if p.car_designed == -1 or p.car_designed is None:
                #aperta o botao
                if (p.destination > self.number):
                    bt = 'up'
                else:
                    bt = 'down'

                e, _dist_d, _ncall, _nfloor = self.select_car(p, bt)
                if e != -1:
                    p.n_call = _ncall
                    p.n_floor = _nfloor
                    p.dist_d = _dist_d
                    p.car_designed = e
                    p.pos_car_call = copy((e.pos[1]))
                    p.dir_car_call = copy((e.state))
                    p.buttons_car_call = len(list(set(x['destination'] for x in self.passageiros)))
                    p.floor_car_call = len(list(x for x in e.destination if x not in list(set(x['destination'] for x in e.passageiros))))

                    p.get_global_state(self, self.model.elevators)

                    if self.number not in e.destination:
                        e.destination.append(self.number)

                else:
                    print("nao selecionou carro")
                    #exit()
            else:
                if self.number not in p.car_designed.destination and (p.car_designed.pos[1] != self.number):
                    p.car_designed.destination.append(self.number)

        #se chegou passageiro
        if (self.next_passager[1] < self.model.schedule.time):
            #0: id, 1: previsao chegada, 2: setar como chegada, 3: andar origem, 4: andar destino
                    
            #cria o passageiro
            p = PassagerAgent("p_"+str(self.next_passager[0]), self.pos, self.model, self.next_passager[3], self.next_passager[4], self.model.schedule.time)
            
            #aperta o botao
            if (self.next_passager[4] > self.number):
                self.up_button = True
                bt = 'up'
            else:
                self.down_button = True
                bt = 'down'

            #define o carro
            e, _dist_d, _ncall, _nfloor = self.select_car(p, bt)
            if e != -1:
                p.n_call = _ncall
                p.n_floor = _nfloor
                p.dist_d = _dist_d
                p.car_designed = e
                p.pos_car_call = copy((e.pos[1]))
                p.dir_car_call = copy((e.state))
                p.buttons_car_call = len(list(set(x['destination'] for x in e.passageiros)))
                p.floor_car_call = len(list(x for x in e.destination if x not in list(set(x['destination'] for x in e.passageiros))))

                p.get_global_state(self, self.model.elevators)

                if self.number not in e.destination:
                    e.destination.append(self.number)
            else:
                print("nao selecionou nenhum carro")
                #exit()        
            
            self.model.schedule.add(p)
            self.model.grid.place_agent(p, self.pos)
            #add na fila
            self.passageiros.append(p)
            

            #proximo
            if len(self.flow) > 0:
                self.next_passager = self.flow.pop()
            else:
                self.next_passager = [ 0, 9000000000]
        

    def get_flow(self, simulation):
        return simulation[self.number]

    def select_car(self, passager, button):
        if self.model.controller == 'baseline':
            return (self.baseline(passager), -1, -1, -1)
        elif self.model.controller == 'pessimistic':
            return (self.pessimistic(passager), -1, -1, -1)
        elif self.model.controller == 'ga':
            return self.fitness_algorithm(button, self.model.alpha, self.model.beta, self.model.theta)
        elif self.model.controller == 'dist':
            return self.fitness_algorithm(button, 1, 0, 0)
        else:
            return self.fitness_algorithm(button, 1, 1, 1)
    def baseline(self, passager):
        #se passageiro subindo
        if passager.destination > passager.origem:
            # se tem carro subindo e em pisso inferior, atribui
            for e in self.model.elevators:
                if (e.state == 2 or e.state == 5) and ((e.pos[1]) <= self.number) and len(e.passageiros) < 15:
                    return e
            
        #se passageiro descendo
        if passager.destination < passager.origem:
            # se tem carro descendo e em pisso superior, atribui
            for e in self.model.elevators:
                if (e.state == 1 or e.state == 4) and ((e.pos[1]) >= self.number)  and len(e.passageiros) < 15:
                    return e
        # se nao conseguiu aproveitar um carro em movimento, astribui um carro sem missao
        for e in self.model.elevators:
            if (e.state == 3 and len(e.passageiros) < 15):
                return e
        
        return -1

    def dist_d(self, button, car):
        '''
        Distancia definida pelo numero de andares ate o carro passar pelo andar no sentido desejado
        '''
        # se subindo e dest < atual
        if ((car.state == 2 or car.state == 5) and button == 'up'):
            if (car.pos[1] < self.number):
                # modulo de atual - dest
                return abs(int(car.pos[1]) - self.number)
            else:
                #pior caso
                return abs(abs(max(car.destination,default = 0) - car.pos[1]) + max(car.destination,default = 0) + self.number)

        #se descendo e dest > atual ou
        elif ((car.state == 1 or car.state == 4) and button == 'down'):
            if (car.pos[1] > self.number):
                return abs(int(car.pos[1]) - self.number)
            else:
                #pior caso
                return abs(abs(min(car.destination,default = 0) - car.pos[1]) + (len(self.model.floors) -1) + ((len(self.model.floors) -1) - self.number))

        #se subido e dest < atual
        elif ((car.state == 2 or car.state == 5) and button == 'down'):
            # (topo - atual) + (topo - dest)
            return abs(abs(max(car.destination,default = 0) - self.number) + abs(max(car.destination,default = 0) - car.pos[1]))

        #se descendo e dest > atual
        elif ((car.state == 1 or car.state == 4) and button == 'up'):
            return abs(self.number - min(car.destination,default = 0)) + abs(car.pos[1] - min(car.destination,default = 0))

        elif (car.state == 3):
            return abs(int(car.pos[1]) - self.number)

    def n_floor(self, button, car):
        '''
        Numero esperado de paradas ate o carro passar pelo andar no sentido desejado
        '''
        #numero de andares que vai parar ate atender o passageiro 
        # se subindo e dest < atual
        if ((car.state == 2 or car.state == 5) and button == 'up'):
            if (car.pos[1] < self.number):
                # modulo de atual - dest
                return len(list(filter(lambda x: x > int(car.pos[1]) and x < self.number, car.destination)))
            else:
                #pior caso
                return len(car.destination)

        #se descendo e dest > atual ou
        elif ((car.state == 1 or car.state == 4) and button == 'down'):
            if (car.pos[1] > self.number):
                return len(list(filter(lambda x: x < int(car.pos[1]) and x > self.number, car.destination)))
            else:
                #pior caso
                return len(car.destination)

        #se subido e dest < atual
        elif ((car.state == 2 or car.state == 5) and button == 'down'):
            # (topo - atual) + (topo - dest)
            return len(list(filter(lambda x: x > int(car.pos[1]) and x > self.number, car.destination)))

        #se descendo e dest > atual
        elif ((car.state == 1 or car.state == 4) and button == 'up'):
            return len(list(filter(lambda x: x < int(car.pos[1]) and x < self.number, car.destination)))

        elif (car.state == 3):
            return len(car.destination)

    #fitness
    def fitness_algorithm(self, button, alpha, beta, theta):
        '''
        Funcao fitness para um carro atender o passageiro determinado com os parametros definidos
        '''

        best_df = None
        best_e = -1

        #para cada elevador e
        for e in self.model.elevators:
            df_e = (alpha * self.dist_d(button, e)) + (beta * len(e.destination)) + (theta * self.n_floor(button, e))
            if best_df is None or df_e < best_df:
                best_e = e
                best_df = df_e
        
        #return best car
        return (best_e, self.dist_d(button, e), len(e.destination), self.n_floor(button, e) )

    def pessimistic(self, passager):
        #andar de origem, o passageiro e os elevadores
        best_e = pessimistic_choice(self, passager, self.model.elevators)
        return best_e