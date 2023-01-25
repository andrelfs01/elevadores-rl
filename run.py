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
controller = 'pessimistic'
#controller = 'df'
#controller = 'dist'
#controller='gerar_tabela_q'


if controller == 'baseline':
    ##se for baseline
    alpha = 1
    beta = 1
    theta = 1
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='baseline', alpha = alpha, beta = beta, theta = theta, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='baseline', alpha = alpha, beta = beta, theta = theta, output_file = True)
    modelo.run_model()
    
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='baseline', alpha = alpha, beta = beta, theta = theta, output_file = True)
    modelo.run_model()


elif controller == 'ga':
    #os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 "+passager_flow+" "+controller)
    os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 up "+controller)
    #os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 dp "+controller)
    #os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 du "+controller)
    
elif controller == 'gerar_tabela_q':
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='ga', alpha = 804, beta = 7335, theta = 7734, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='ga', alpha = 2331, beta = 4223, theta = 4255, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='ga', alpha = 4613, beta = 2662, theta = 5608, output_file = True)
    modelo.run_model()

elif controller == 'pessimistic':
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='pessimistic', alpha = 1, beta = 1, theta = 1, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='pessimistic', alpha = 1, beta = 1, theta = 1, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='pessimistic', alpha = 1, beta = 1, theta = 1, output_file = True)
    modelo.run_model()

elif controller == 'df':
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='df', alpha = 1, beta = 1, theta = 1, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='df', alpha = 1, beta = 1, theta = 1, output_file = True)
    modelo.run_model()
    
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='df', alpha = 1, beta = 1, theta = 1, output_file = True)
    modelo.run_model()

elif controller == 'dist':
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='dist', alpha = 1, beta = 0, theta = 0, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='dist', alpha = 1, beta = 0, theta = 0, output_file = True)
    modelo.run_model()
    
    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='dist', alpha = 1, beta = 0, theta = 0, output_file = True)
    modelo.run_model()