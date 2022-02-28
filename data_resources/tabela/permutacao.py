import pandas as pd

cols = ['id', 'from', 'to', 'car', 'incoming_time', 'boarding_time', 'attended_time', 'dist_d' , 'n_call' ,
            'n_floor', 'car_position_call', 'car_direction_call', 'car_queue_buttons', 'car_queue_floor', 
            'dist_d_deny1', 'n_call_deny1', 'n_floor_deny1', 'car_position_deny1', 'car_direction_deny1',
            'car_queue_buttons_deny1', 'car_queue_floor_deny1' , 'dist_d_deny2', 'n_call_deny2',
            'n_floor_deny2', 'car_position_deny2', 'car_direction_deny2', 'car_queue_buttons_deny2',
            'car_queue_floor_deny2', 'dist_d_deny3', 'n_call_deny3', 'n_floor_deny3', 'car_position_deny3',
            'car_direction_deny3', 'car_queue_buttons_deny3', 'car_queue_floor_deny3', 'waiting_time', 'journey_time', 'total_time']

df = pd.read_csv('/home/andre/projetos/elevadores-rl/resultados_finais/tabela/tabela_algoritmo_pessimista.csv')


#para cada linha da tabela gerar todas as permutacoes

# 1 3 2 
# 2 1 3
# 2 3 1
# 3 1 2
# 3 2 1

dfs = 

df = pd.concat(dfs)

df.to_csv('resultado_geral_com_permutacoes.csv')