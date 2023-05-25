import os
#from model import Modelo
from model_full_state import Modelo
from ga_optimization import exec
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
controller = 'ga'
# controller = 'pessimistic'
#controller = 'df'
#controller = 'dist'
#controller = 'gerar_tabela_q'


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
    #os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 up "+controller)
    #os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 dp "+controller)
    #os.system("python3 ga_optimization.py "+num_elevators+" "+num_floors+" 0 du "+controller)
    exec(num_elevators, num_floors, 0 , controller )
    
elif controller == 'gerar_tabela_q':
    # modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='ga', alpha = 1117, beta = 8513, theta = 3836, output_file = True)
    # modelo.run_model()

    # modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='ga', alpha = 3833, beta = 6881, theta = 3564, output_file = True)
    # modelo.run_model()

    # modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='ga', alpha = 5838, beta = 6867, theta = 62, output_file = True)
    # modelo.run_model()
    #alpha=2331
    #beta = 4223
    #theta = 4255

    ##40 geracoes:
    #best = 75.10144927536231
    alpha = 2452
    beta = 8127
    theta = 8576

    ###resultado final do texto
    alpha = 0.112
    beta = 0.773
    theta = 0.114

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='up', controller='ga', alpha = alpha, beta = beta, theta = theta, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='dp', controller='ga', alpha = alpha, beta = beta, theta = theta, output_file = True)
    modelo.run_model()

    modelo = Modelo(elevators=4, floors=16, a = 0, passager_flow='du', controller='ga', alpha = alpha, beta = beta, theta = theta, output_file = True)

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