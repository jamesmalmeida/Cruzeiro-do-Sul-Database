import numpy as np
import plotly.graph_objs as go
import time  # For the random seed
import pickle
import os
import pandas as pd

import keyboard 

def ga(
    n_materials: int,
    absorbing_element: str,
    edge: str,
    target_function: pd.DataFrame,
    pop_size: int = 200,
    pm: float = 0.6,
    pc: float = 0.8,
):
    """
    Utiliza um algoritmo genético para encontrar a melhor combinação para um dado espectro.

    Parâmetros:
    - n_materials (int): O número de materiais no espectro.
    - absorbing_element: O elemento absorvedor
    - edge: Borda de absorção
    - target_function: Dataframe com o espectro normalizado a ser comparado, de referência
    - pop_size (int, opcional): O tamanho da população. Padrão é 200.
    - pm (float, opcional): A taxa de mutação. Padrão é 0.6.
    - pc (float, opcional): A taxa de crossover. Padrão é 0.8.

    Retorna:
    - Gráfico contendo os espectros encontrados pelo algoritmo genético com seus respectivos coeficientes.
    """
    print("GA_COMBINATOR LOADED.")

    seed = int(time.time())
    np.random.seed(seed)

    POP_SIZE = pop_size
    PM = pm  # Mutation rate
    PC = pc  # Crossover rate

    N_MATERIALS = n_materials

    try:
        processed_pickle_files = {}

        norm_pkl_path = os.path.join(os.getcwd(), 'norm_pkl_files')
        abs_element_pkl_path = os.path.join(norm_pkl_path, absorbing_element)

        for filename in os.listdir(abs_element_pkl_path):
            file_path = os.path.join(abs_element_pkl_path, filename)
            if filename.endswith(".pickle") and os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        header, df = pickle.load(file)
                    file_key = filename[:-12]
                    processed_pickle_files[file_key] = (header, df)
                except Exception as e:
                    print(f"Erro ao processar o arquivo {filename}: {e}")

        min_max_ranges = [(min(df['energy eV']), max(df['energy eV'])) for _, df in processed_pickle_files.values()]
        min_of_maxes = max([min_max[0] for min_max in min_max_ranges])
        max_of_mins = min([min_max[1] for min_max in min_max_ranges])
        domain = np.linspace(min_of_maxes, max_of_mins, num=5000)

        try: # Arrumar isso pra deixar padrão
            x = target_function['energy eV']
            y = target_function['norm']
            target_spectrum = np.interp(domain, x, y)
        except:
            print('target_function columns must be ["Energy eV", "norm"]')
    except Exception as e:
        raise ValueError(e)

    spectra = {}
    interpolated_functions = []
    for key, (header, df) in processed_pickle_files.items():
        interpolated_norm = np.interp(domain, df['energy eV'], df['norm'])
        interpolated_functions.append(interpolated_norm)

    for i in range(len(processed_pickle_files.keys())):
        key = list(processed_pickle_files.keys())[i]
        spectra[key] = interpolated_functions[i]

    def fitness(individual, target_function=target_spectrum):
        rmse = (sum((target_function - individual)**2))**(1/2)
        fitness_score = 1 / (1 + rmse)  # Use rMSE method to compare; lower the rMSE, higher the fitness
        return fitness_score

    def create_individual(functions, domain, n=N_MATERIALS, target_function=target_spectrum):
        num_functions = len(functions)
        coefficients = np.random.rand(num_functions)
        
        # Find the highest coeff
        sorted_indices = np.argsort(coefficients)[::-1]
        np.random.shuffle(sorted_indices)

        selected_coeffs = coefficients[sorted_indices[:n]]
        selected_keys = [list(functions.keys())[idx] for idx in sorted_indices[:n]]

        selected_coeffs /= np.sum(selected_coeffs)

        individual = {}
        individual['array'] = np.zeros(len(domain))
        for i, key in enumerate(selected_keys):
            individual['array'] += selected_coeffs[i] * functions[key]

        individual['coeff'] = selected_coeffs
        individual['funcs'] = [functions[key] for key in selected_keys]
        individual['funcs_keys'] = list(selected_keys )

        individual['fitness'] = fitness(individual['array'], target_function)
        
        return individual

    def create_population(pop_size, functions, domain, target_function=target_spectrum, n=N_MATERIALS):
        population = {}
        for i in range(pop_size):
            population[i+1] = {}
            individual = create_individual(functions, domain, n)
            population[i+1]['ind'] = individual
        
        return population

    def roulette_selection(pop, target_function=target_spectrum):
        fitness_values = [pop[i]['ind']['fitness'] for i in pop]
        total_fitness = sum(fitness_values)
        normalized_fitness = [fitness / total_fitness for fitness in fitness_values]

        selected_indices = np.random.choice(len(pop), size=len(pop), p=normalized_fitness)
        selected_individuals = [pop[i+1]['ind'] for i in selected_indices]

        new_population = {}
        for i, individual in enumerate(selected_individuals):
            new_population[i+1] = {
                'ind': {
                    'array': individual['array'],
                    'coeff': individual['coeff'],
                    'funcs': individual.get('funcs', []),
                    'funcs_keys': individual.get('funcs_keys', []),
                    'fitness': fitness(individual['array'], target_function)
                }
            }
        
        return new_population

    def mutate(individual, functions, mutation_rate=0.1, n=N_MATERIALS):
        mutated_individual = individual.copy()
        
        if np.random.rand() < mutation_rate:  # Mutate coefficients with mutation_rate probability
            num_functions = len(functions)

            coefficients = np.random.rand(num_functions)
        
            # Find the highest coeff
            sorted_indices = np.argsort(coefficients)[::-1]
            np.random.shuffle(sorted_indices)

            selected_coeffs = coefficients[sorted_indices[:n]]
            selected_keys = [list(functions.keys())[idx] for idx in sorted_indices[:n]]

            selected_coeffs /= np.sum(selected_coeffs)

            mutated_individual['coeff'] = selected_coeffs
            
        if np.random.rand() < mutation_rate:  # Mutate functions with mutation_rate probability
            mutated_keys = np.random.choice(list(functions.keys()), size=len(individual['funcs']))
            mutated_individual['funcs'] = [functions[key] for key in mutated_keys]
            mutated_individual['funcs_keys'] = list(mutated_keys)
            
        mutated_individual['array'] = np.zeros(len(domain))
        for i, key in enumerate(np.argsort(mutated_individual['coeff'])[::-1][:len(mutated_individual['funcs'])]):
            mutated_individual['array'] += mutated_individual['coeff'][i] * mutated_individual['funcs'][i]
        
        mutated_individual['fitness'] = fitness(mutated_individual['array'])
        
        return mutated_individual

    def crossover(parent1, parent2, domain, target_function=target_spectrum):
        child1 = {}
        child2 = {}

        num_coeffs_p1 = len(parent1['coeff'])
        num_coeffs_p2 = len(parent2['coeff'])
        
        # Escolha do ponto de corte
        crossover_point = np.random.randint(min(num_coeffs_p1, num_coeffs_p2))

        # Cruzamento de funções
        child1['funcs'] = parent1['funcs'][:crossover_point] + parent2['funcs'][crossover_point:]
        child2['funcs'] = parent2['funcs'][:crossover_point] + parent1['funcs'][crossover_point:]
        
        # Cruzamento de chaves das funções
        child1['funcs_keys'] = parent1['funcs_keys'][:crossover_point] + parent2['funcs_keys'][crossover_point:]
        child2['funcs_keys'] = parent2['funcs_keys'][:crossover_point] + parent1['funcs_keys'][crossover_point:]
        
        # Cruzamento de coeficientes
        child1['coeff'] = np.concatenate((parent1['coeff'][:crossover_point], parent2['coeff'][crossover_point:]))
        child2['coeff'] = np.concatenate((parent2['coeff'][:crossover_point], parent1['coeff'][crossover_point:]))
        
        child1['array'] = np.zeros(len(domain))
        for i, key in enumerate(np.argsort(child1['coeff'])[::-1][:len(child1['funcs'])]):
            child1['array'] += child1['coeff'][i] * child1['funcs'][i]
        
        child2['array'] = np.zeros(len(domain))
        for i, key in enumerate(np.argsort(child2['coeff'])[::-1][:len(child2['funcs'])]):
            child2['array'] += child2['coeff'][i] * child2['funcs'][i]

        child1['fitness'] = fitness(child1['array'], target_function)
        child2['fitness'] = fitness(child2['array'], target_function)

        return child1, child2
    
    # Iniciando o algoritmo

    pop = create_population(POP_SIZE, spectra, domain)
    max_fitness = -float('inf')
    ind_with_max_fitness = None
    gen = 0

    stop_flag = False

    while not stop_flag:#max_fitness < 1:# and gen<100:
        pop = roulette_selection(pop)  

        mutated_population = {}
        for i, individual_data in pop.items():
            mutated_individual = mutate(individual_data['ind'], spectra, PM)
            mutated_population[i] = {
                'ind': mutated_individual
            }
        pop = mutated_population

        crossed_population = {}
        for i in range(0, POP_SIZE, 2):
            parent1 = pop[i + 1]['ind']
            parent2 = pop[i + 2]['ind']
            if np.random.rand() < PC:
                child1, child2 = crossover(parent1, parent2, domain)
                crossed_population[i + 1] = {'ind': child1}
                crossed_population[i + 2] = {'ind': child2}
            else:
                crossed_population[i + 1] = {'ind': parent1}
                crossed_population[i + 2] = {'ind': parent2}

        pop = crossed_population

        for ind_data in pop.values():
            if ind_data['ind']['fitness'] > max_fitness:
                max_fitness = ind_data['ind']['fitness']
                ind_with_max_fitness = ind_data['ind']

        if ind_with_max_fitness is not None:
            array_with_max_fitness = ind_with_max_fitness['array']

        ind_with_max_fitness = max(pop.values(), key=lambda ind_data: ind_data['ind']['fitness'])['ind']
        array_with_max_fitness = ind_with_max_fitness['array']
        funcs_keys_with_max_fitness = ind_with_max_fitness['funcs_keys']
        coeffs_with_max_fitness = ind_with_max_fitness['coeff']

        gen += 1

        print(gen, max_fitness)

        if keyboard.is_pressed('space'):
            stop_flag = True

    best_result = f''
    for i in range(len(coeffs_with_max_fitness)):
        best_result += f' + {round(coeffs_with_max_fitness[i],2)} * {funcs_keys_with_max_fitness[i]}'

    dic_plot = {
        "domain": domain,
        "array_with_max_fitness": array_with_max_fitness,
        "target_spectrum": target_spectrum,
        "spectra": spectra,
        "funcs_keys_with_max_fitness": funcs_keys_with_max_fitness,
        "coeffs_with_max_fitness": coeffs_with_max_fitness,
        "gen": gen,
        "best_result": best_result
    }

    return dic_plot