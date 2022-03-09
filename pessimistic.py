def similarity_search():
    pass

def worst_option():
    pass

def best_option():
    pass

def pessimistic_choice(floor, passager, elevators):
#dado esse passageiro e a tabela (tabela gerada GA full ou /data_resources/tabela/tabela_algoritmo_pessimista)
        #escolher o elevador
    best_e = -1
    options = []    
    for e in elevators:
        #para cada elevador, encontra as 3 opções mais similares e retorna a pior
        most_similars = []
        most_similars = similarity_search()
        options.append(worst_option(most_similars))



    return best_option(options)