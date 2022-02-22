import pandas as pd

cols = ['id', 'from', 'to', 'car', 'incoming_time', 'boarding_time', 'attended_time', 'dist_d' , 'n_call' ,
            'n_floor', 'car_position_call', 'car_direction_call', 'car_queue_buttons', 'car_queue_floor', 
            'dist_d_deny1', 'n_call_deny1', 'n_floor_deny1', 'car_position_deny1', 'car_direction_deny1',
            'car_queue_buttons_deny1', 'car_queue_floor_deny1' , 'dist_d_deny2', 'n_call_deny2',
            'n_floor_deny2', 'car_position_deny2', 'car_direction_deny2', 'car_queue_buttons_deny2',
            'car_queue_floor_deny2', 'dist_d_deny3', 'n_call_deny3', 'n_floor_deny3', 'car_position_deny3',
            'car_direction_deny3', 'car_queue_buttons_deny3', 'car_queue_floor_deny3', 'waiting_time', 'journey_time', 'total_time']

df = pd.read_csv('/home/andre/projetos/elevadores-rl/resultados_finais/tabela/resultado_ga_dp_2021-09-15_16:17base_full.csv', names = cols)


df2 = pd.read_csv('/home/andre/projetos/elevadores-rl/resultados_finais/tabela/resultado_ga_du_2021-09-15_16:17base_full.csv', names = cols)

df3 = pd.read_csv('/home/andre/projetos/elevadores-rl/resultados_finais/tabela/resultado_ga_up_2021-09-15_16:17base_full.csv', names = cols)

dfs = [df, df2, df3]

df = pd.concat(dfs)

print(len(cols))
df.to_csv('resultado_geral.csv')