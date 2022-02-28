from itertools import permutations
import pandas as pd

cols = ['id', 'from', 'to', 'car', 'incoming_time', 'boarding_time', 'attended_time', 'dist_d' , 'n_call' ,
            'n_floor', 'car_position_call', 'car_direction_call', 'car_queue_buttons', 'car_queue_floor', 
            'dist_d_deny1', 'n_call_deny1', 'n_floor_deny1', 'car_position_deny1', 'car_direction_deny1',
            'car_queue_buttons_deny1', 'car_queue_floor_deny1' , 'dist_d_deny2', 'n_call_deny2',
            'n_floor_deny2', 'car_position_deny2', 'car_direction_deny2', 'car_queue_buttons_deny2',
            'car_queue_floor_deny2', 'dist_d_deny3', 'n_call_deny3', 'n_floor_deny3', 'car_position_deny3',
            'car_direction_deny3', 'car_queue_buttons_deny3', 'car_queue_floor_deny3', 'waiting_time', 'journey_time', 'total_time']

df = pd.read_csv('/home/andre/projetos/elevadores-rl/resultados_finais/tabela/tabela_algoritmo_pessimista.csv')


permutacoes = pd.DataFrame(columns=cols)

#para cada linha da tabela gerar todas as permutacoes
for row in df.iterrows():
    # 1 3 2 
    new_row = {'id': row['id'], 'from': row['from'], 'to': row['to'], 'car': row['car'], 'incoming_time': row['incoming_time'], 'boarding_time': row['boarding_time'],
                'attended_time' : row['attended_time'], 'dist_d': row['dist_d'] , 'n_call': row['n_call'] ,
                'n_floor': row['n_floor'], 'car_position_call': row['car_position_call'], 'car_direction_call': row['car_direction_call'], 
                'car_queue_buttons': row['car_queue_buttons'], 'car_queue_floor': row['car_queue_floor'],
                'dist_d_deny1' : row['dist_d_deny1'],
                'n_call_deny1': row['n_call_deny1'],
                'n_floor_deny1': row['n_floor_deny1'],
                'car_position_deny1': row['car_position_deny1'],
                'car_direction_deny1': row['car_direction_deny1'],
                'car_queue_buttons_deny1': row['car_queue_buttons_deny1'],
                'car_queue_floor_deny1': row['car_queue_floor_deny1'],

                'dist_d_deny2': row['dist_d_deny3'],
                'n_call_deny2': row['n_call_deny3'],
                'n_floor_deny2': row['n_floor_deny3'],
                'car_position_deny2': row['car_position_deny3'],
                'car_direction_deny2': row['car_direction_deny3'],
                'car_queue_buttons_deny2': row['car_queue_buttons_deny3'],
                'car_queue_floor_deny2': row['car_queue_floor_deny3'],

                'dist_d_deny3': row['dist_d_deny2'],
                'n_call_deny3': row['n_call_deny2'],
                'n_floor_deny3': row['n_floor_deny2'],
                'car_position_deny3': row['car_position_deny2'],
                'car_direction_deny3': row['car_direction_deny2'],
                'car_queue_buttons_deny3': row['car_queue_buttons_deny2'],
                'car_queue_floor_deny3': row['car_queue_floor_deny2'],
                'waiting_time': row['waiting_time'], 'journey_time': row['journey_time'],'total_time': row['total_time']}

    permutacoes = permutacoes.append(pd.Series(new_row), ignore_index=True)
 
    # 2 1 3
    new_row = {'id': row['id'], 'from': row['from'], 'to': row['to'], 'car': row['car'], 'incoming_time': row['incoming_time'], 'boarding_time': row['boarding_time'],
                'attended_time' : row['attended_time'], 'dist_d': row['dist_d'] , 'n_call': row['n_call'] ,
                'n_floor': row['n_floor'], 'car_position_call': row['car_position_call'], 'car_direction_call': row['car_direction_call'], 
                'car_queue_buttons': row['car_queue_buttons'], 'car_queue_floor': row['car_queue_floor'],
                'dist_d_deny1' : row['dist_d_deny2'],
                'n_call_deny1': row['n_call_deny2'],
                'n_floor_deny1': row['n_floor_deny2'],
                'car_position_deny1': row['car_position_deny2'],
                'car_direction_deny1': row['car_direction_deny2'],
                'car_queue_buttons_deny1': row['car_queue_buttons_deny2'],
                'car_queue_floor_deny1': row['car_queue_floor_deny2'],

                'dist_d_deny2': row['dist_d_deny1'],
                'n_call_deny2': row['n_call_deny1'],
                'n_floor_deny2': row['n_floor_deny1'],
                'car_position_deny2': row['car_position_deny1'],
                'car_direction_deny2': row['car_direction_deny1'],
                'car_queue_buttons_deny2': row['car_queue_buttons_deny1'],
                'car_queue_floor_deny2': row['car_queue_floor_deny1'],

                'dist_d_deny3': row['dist_d_deny3'],
                'n_call_deny3': row['n_call_deny3'],
                'n_floor_deny3': row['n_floor_deny3'],
                'car_position_deny3': row['car_position_deny3'],
                'car_direction_deny3': row['car_direction_deny3'],
                'car_queue_buttons_deny3': row['car_queue_buttons_deny3'],
                'car_queue_floor_deny3': row['car_queue_floor_deny3'],
                'waiting_time': row['waiting_time'], 'journey_time': row['journey_time'],'total_time': row['total_time']}

    permutacoes = permutacoes.append(pd.Series(new_row), ignore_index=True)

    # 2 3 1
    new_row = {'id': row['id'], 'from': row['from'], 'to': row['to'], 'car': row['car'], 'incoming_time': row['incoming_time'], 'boarding_time': row['boarding_time'],
                'attended_time' : row['attended_time'], 'dist_d': row['dist_d'] , 'n_call': row['n_call'] ,
                'n_floor': row['n_floor'], 'car_position_call': row['car_position_call'], 'car_direction_call': row['car_direction_call'], 
                'car_queue_buttons': row['car_queue_buttons'], 'car_queue_floor': row['car_queue_floor'],
                'dist_d_deny1' : row['dist_d_deny2'],
                'n_call_deny1': row['n_call_deny2'],
                'n_floor_deny1': row['n_floor_deny2'],
                'car_position_deny1': row['car_position_deny2'],
                'car_direction_deny1': row['car_direction_deny2'],
                'car_queue_buttons_deny1': row['car_queue_buttons_deny2'],
                'car_queue_floor_deny1': row['car_queue_floor_deny2'],

                'dist_d_deny2': row['dist_d_deny3'],
                'n_call_deny2': row['n_call_deny3'],
                'n_floor_deny2': row['n_floor_deny3'],
                'car_position_deny2': row['car_position_deny3'],
                'car_direction_deny2': row['car_direction_deny3'],
                'car_queue_buttons_deny2': row['car_queue_buttons_deny3'],
                'car_queue_floor_deny2': row['car_queue_floor_deny3'],

                'dist_d_deny3': row['dist_d_deny1'],
                'n_call_deny3': row['n_call_deny1'],
                'n_floor_deny3': row['n_floor_deny1'],
                'car_position_deny3': row['car_position_deny1'],
                'car_direction_deny3': row['car_direction_deny1'],
                'car_queue_buttons_deny3': row['car_queue_buttons_deny1'],
                'car_queue_floor_deny3': row['car_queue_floor_deny1'],
                'waiting_time': row['waiting_time'], 'journey_time': row['journey_time'],'total_time': row['total_time']}

    permutacoes = permutacoes.append(pd.Series(new_row), ignore_index=True)

    # 3 1 2
    new_row = {'id': row['id'], 'from': row['from'], 'to': row['to'], 'car': row['car'], 'incoming_time': row['incoming_time'], 'boarding_time': row['boarding_time'],
                'attended_time' : row['attended_time'], 'dist_d': row['dist_d'] , 'n_call': row['n_call'] ,
                'n_floor': row['n_floor'], 'car_position_call': row['car_position_call'], 'car_direction_call': row['car_direction_call'], 
                'car_queue_buttons': row['car_queue_buttons'], 'car_queue_floor': row['car_queue_floor'],
                'dist_d_deny1' : row['dist_d_deny3'],
                'n_call_deny1': row['n_call_deny3'],
                'n_floor_deny1': row['n_floor_deny3'],
                'car_position_deny1': row['car_position_deny3'],
                'car_direction_deny1': row['car_direction_deny3'],
                'car_queue_buttons_deny1': row['car_queue_buttons_deny3'],
                'car_queue_floor_deny1': row['car_queue_floor_deny3'],

                'dist_d_deny2': row['dist_d_deny1'],
                'n_call_deny2': row['n_call_deny1'],
                'n_floor_deny2': row['n_floor_deny1'],
                'car_position_deny2': row['car_position_deny1'],
                'car_direction_deny2': row['car_direction_deny1'],
                'car_queue_buttons_deny2': row['car_queue_buttons_deny1'],
                'car_queue_floor_deny2': row['car_queue_floor_deny1'],

                'dist_d_deny3': row['dist_d_deny2'],
                'n_call_deny3': row['n_call_deny2'],
                'n_floor_deny3': row['n_floor_deny2'],
                'car_position_deny3': row['car_position_deny2'],
                'car_direction_deny3': row['car_direction_deny2'],
                'car_queue_buttons_deny3': row['car_queue_buttons_deny2'],
                'car_queue_floor_deny3': row['car_queue_floor_deny2'],
                'waiting_time': row['waiting_time'], 'journey_time': row['journey_time'],'total_time': row['total_time']}

    permutacoes = permutacoes.append(pd.Series(new_row), ignore_index=True)
# 3 2 1

df = pd.concat(permutacoes)

#df.to_csv('resultado_geral_com_permutacoes.csv')