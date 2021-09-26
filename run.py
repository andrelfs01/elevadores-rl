import os
#from model import Modelo
from model_full_state import Modelo

#configuration 
num_elevators =str(4)
num_floors = str(16)
a = str(0)

#choose one
#passager_flow = 'up'      #
#passager_flow = 'dp'      #
#passager_flow = 'du'      #
#passager_flow = 'poison'  # 

#choose one
#controller = 'baseline'
#controller = 'ga'
#controller = 'nn'
controller = 'gerar_tabela_q'


if controller == 'baseline':
    ##se for baseline
    alpha = 1
    beta = 1
    theta = 1
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='baseline', alpha = alpha, beta = beta, theta = theta, output_file = True)
    modelo.run_model()

    #modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='baseline', alpha = alpha, beta = beta, theta = theta, output_file = True)
    #modelo.run_model()
    
    #modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='baseline', alpha = alpha, beta = beta, theta = theta, output_file = True)
    #modelo.run_model()


elif controller == 'ga':
    #os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 "+passager_flow+" "+controller)
    os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 up "+controller)
    os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 dp "+controller)
    os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 du "+controller)
    
elif controller == 'gerar_tabela_q':
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='ga', alpha = 1117, beta = 8513, theta = 3836, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='ga', alpha = 3833, beta = 6881, theta = 3564, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='ga', alpha = 5838, beta = 6867, theta = 62, output_file = True)
    modelo.run_model()