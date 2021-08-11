import os
from model import Modelo

#configuration 
num_elevators =str(4)
num_floors = str(16)
a = str(0)

#choose one
passager_flow = 'up'      #
#passager_flow = 'dp'      #
#passager_flow = 'du'      #
#passager_flow = 'poison'  # 

#choose one
# controller = 'baseline'
controller = 'ga'
#controller = 'nn'


if controller == 'baseline':
    ##se for baseline
    alpha = 1
    beta = 1
    theta = 1
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='baseline', alpha = alpha, beta = beta, theta = theta, output_file = True)
    modelo.run_model()

elif controller == 'ga':
    os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 "+passager_flow+" "+controller)
