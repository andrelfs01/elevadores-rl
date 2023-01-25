import numpy as np
import csv
from sklearn.neighbors import NearestNeighbors

path = '.\\resources\\resultado_geral_com_permutacoes_3s.csv'
with open(path, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    headers = next(reader)
    data = np.array(list(reader)).astype(float)
    

def similarity_search(floor, passager, car_selected, elevators):
    # passager origin destino
    if (passager.destination > floor.number):
        bt = 'up'
    else:
        bt = 'down'
    # dist_d	n_call	n_floor	car_position_call	car_direction_call	car_queue_buttons	car_queue_floor
    
    state = [passager.origem, passager.destination, floor.controller.dist_d(bt, car_selected, floor), len(car_selected.destination), floor.controller.n_floor(bt, car_selected,floor), car_selected.pos[1],
    car_selected.state, len(list(set(x['destination'] for x in car_selected.passageiros))), len(list(x for x in car_selected.destination if x not in list(set(x['destination'] for x in car_selected.passageiros))))]
 
    for e in elevators:
        if e != car_selected:
            # 3x dist_d	n_call	n_floor	car_position_call	car_direction_call	car_queue_buttons	car_queue_floor
            state.append(floor.controller.dist_d(bt, e,floor))
            state.append(len(e.destination))
            state.append(floor.controller.n_floor(bt, e,floor))
            state.append(e.pos[1])
            state.append(e.state)
            state.append(len(list(set(x['destination'] for x in e.passageiros))))
            state.append(len(list(x for x in e.destination if x not in list(set(x['destination'] for x in e.passageiros)))))

    neigh = NearestNeighbors(n_neighbors=3)
    neigh.fit(data[:,:30])
    distances, indices= neigh.kneighbors(np.asarray(state).reshape(1,-1))
    print('distances',distances)
    print('indices', indices)
    print('state:', state)
    return indices[0]

def worst_option(indices):
    '''
    Recebe um array com n indices e retorna o "pior" indice dos dados
    '''
    worst = -1
    res = -1
    for i in indices:
        if data[i][32] > worst:
            res = i
            worst = data[i][32]
    
    return res

def best_option(options):
    '''
    Recebe uma lista de tuplas (elevador, indice) correspondente ao pior cenario para a escolha deste elevador, e retorna o elevador da melhor opção
    '''
    best = 9999999999999
    res = -1
    for elevator, i in options:
        if data[i][32] < best:
            res = elevator
            best = data[i][32]
    
    return res

def pessimistic_choice(floor, passager, elevators):
#dado esse passageiro e a tabela (tabela gerada GA full ou /data_resources/tabela/tabela_algoritmo_pessimista)
        #escolher o elevador
    options = []    
    for e in elevators:
        if len(e.passageiros) < 15 or floor.number != e.pos[1]:
        #para cada elevador, encontra as 3 opções mais similares e retorna a pior
            most_similars = []
            most_similars = similarity_search(floor, passager, e, elevators)
            options.append((e, worst_option(most_similars)))
    return best_option(options)