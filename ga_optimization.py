
from model_full_state import Modelo
from agents_full_state import ElevatorAgent, PassagerAgent, FloorAgent
from numpy import random as random
from operator import itemgetter
from pandas import DataFrame
import pandas as pd
import sys, os
import time
#import tracemalloc
import gc
import threading
from queue import Queue

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

num_gen = 250
population_size = 20
num_tournament_competitors = 8
num_elistism = 2
cross_prob = 0.75
mutation_prob = 0.1

#GA para parametrizacao
def ga_fitness(passagers):
    fitness = None
    if len(passagers) > 0:
        df = DataFrame.from_records([s.to_dict() for s in passagers])
        df["waiting_time"] = (df["boarding_time"] - df["incoming_time"])
        df["journey_time"] = (df["attended_time"] - df["boarding_time"])
        df["total_time"] = (df["attended_time"] - df["incoming_time"])
        cols = ["waiting_time","journey_time","total_time"]
        fitness = df[cols].mean(axis=0)

    return fitness

def calc_fitness(results):
    return results['total_time']/2

def select_thebests(pop, num):
    bests = []
    while len(bests) < num:
        bests.append(min(pop,key=itemgetter(1)))
        pop.remove(min(pop,key=itemgetter(1)))

    #print(bests)
    #print(pop)
    return bests, pop

def exec_model(modelo):
    modelo.run_model()

def tournament(pop, num_tournament_competitors, cross_prob):
    parents = []
    childs = []
    while len(parents) < num_tournament_competitors:
        parents.append(min(pop,key=itemgetter(1)))
        pop.remove(min(pop,key=itemgetter(1)))

    while len(childs) < (cross_prob * population_size):
        idx_dad = random.randint(low = 0, high = len(parents) -1 )
        random_dad = parents[idx_dad][0]

        idx_mom = random.randint(low = 0, high = len(parents) -1 )
        random_mom = parents[idx_mom][0]

        point = random.randint(1, len(random_dad) -2)
        c1 = list(random_dad[:point]) + list(random_mom[point:])
        c2 = list(random_mom[:point]) + list(random_dad[point:])
        childs.append([c1,999999])
        childs.append([c2,999999])

    if len(parents) + len (childs) < len(pop):
        print("ERROR")
        quit()

    return parents + childs

def variate(pop, mutation_prob):
    for i in pop:
        for c in range(len(i[0])):
            if random.uniform(0, 1) <= mutation_prob:
                #print(i[0])
                mut = random.randint(1,9)
                #print("mutacao: {} -> {} ".format(i[0][c], mut))
                i[0][c] = mut
                #print(i[0])
    return pop

def exec(m, n, param_a , control):
    population = None
    #para cada geracao
    results = None
    best = None
    best_alpha = 0
    best_beta = 0
    best_theta = 0

    achou = False
    total_results = pd.DataFrame(columns=['gen','tms'])
    #tracemalloc.start()
    for gen in range(1, num_gen + 1):
        print ("*******************************************************")
        print ("gen {}".format(gen))
        #inicia a populacao
        if population is None:
            population = []
            population.append([[0,1,1,2,0,7,7,3,0,1,1,4], -1])
            for s in range(population_size):
                population.append([list(random.randint(9, size=12)), -1])

        #nova geracao
        else:
            new_population = []
            #selecao (mantem os 2 melhores)
            print("len : {}".format(len(population)))
            p1, p2 = select_thebests(population.copy(), num_elistism)
                    
            #reproducao/crossover
            p2 = tournament(p2, num_tournament_competitors, cross_prob)

            population = list(p1) + list(p2)

            #mutacao
            population = variate(population, mutation_prob)
        
        
        #para cada individuo
        for i in population:
            
            #print(i)
            a = i[0][:4]
            b = i[0][4:8]
            t = i[0][8:]
            alpha = int("".join(map(str, a)))
            beta = int("".join(map(str, b)))
            theta = int("".join(map(str, t)))
            #print (alpha, beta, theta)
            if ('modelo' in globals() or 'modelo' in locals()) and modelo is not None:
                del modelo
                gc.collect()
            
            if False:
                modelo = Modelo(elevators=m, floors=n, a = param_a, passager_flow=sys.argv[4], controller=control, alpha = alpha, beta = beta, theta = theta, output_file = True)
            else:
                #modelo = Modelo(elevators=sys.argv[1], floors=sys.argv[2], a = sys.argv[3], passager_flow=sys.argv[4], controller=sys.argv[5], alpha = alpha, beta = beta, theta = theta, output_file = False)
                modelo_tf1 = Modelo(elevators=m, floors=n, a = param_a, passager_flow='up', controller=control, alpha = alpha, beta = beta, theta = theta, output_file = False)
                modelo_tf2 = Modelo(elevators=m, floors=n, a = param_a, passager_flow='dp', controller=control, alpha = alpha, beta = beta, theta = theta, output_file = False)
                modelo_tf3 = Modelo(elevators=m, floors=n, a = param_a, passager_flow='du', controller=control, alpha = alpha, beta = beta, theta = theta, output_file = False)
            
            blockPrint()
            modelo_tf1.run_model()
            modelo_tf2.run_model()
            modelo_tf3.run_model()
            enablePrint()
            #print(i)
            all_results = modelo_tf1.attended + modelo_tf2.attended + modelo_tf3.attended
            results  = ga_fitness(all_results)

            new = {'gen':gen, 'tms':results['total_time']}
            df_new = pd.DataFrame(new, index=[0])
            total_results = pd.concat([total_results, df_new], ignore_index=True)

            if best is None or results['total_time'] < best:
                best = results['total_time']
                best_alpha = alpha
                best_beta = beta
                best_theta = theta
                print("best = {}".format(best))

            if best < 69.18:
                achou = True

            #calcula o desempenho do individuo
            i[1] = calc_fitness(results)
            #print(calc_fitness(results))
            #print("-----------------------------------")    
        if (achou):
            break
        #mostra a ultima populacao
        #print(population)
        #calcular a media da populacao
        #salvar resultados
    #tracemalloc.stop()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")  
    print("best = {}".format(best))
    print("best_alpha = {}".format(best_alpha))
    print("bebest_beta = {}".format(best_beta))
    print("best_theta = {}".format(best_theta))
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")  
    print(total_results)
    #total_results.to_csv('total_results_otimizacao_ga.csv', header = True, index=False, sep=',')
    df_agrupado = total_results.groupby('gen')['tms'].agg(['mean','min', 'max']).reset_index()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")  
    print(df_agrupado)
    #df_agrupado.to_csv('df_agrupado_otimizacao_ga.csv', header = True, index=False, sep=',')
    # modelo = Modelo(elevators=sys.argv[1], floors=n, a = param_a, passager_flow=sys.argv[4], controller=control, alpha = best_alpha, beta = best_beta, theta = best_theta, output_file = True)
    # modelo.run_model()
