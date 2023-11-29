from tkinter import Y
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from evaluateTree import evaluateTree
from infixToPrefix import infix_to_prefix
from treebuild import *

def plot(fun_optimal_tree, fun_generated_tree, xs):
    
    fun_optimal_values = np.zeros(len(xs))
    fun_generated_values = np.zeros(len(xs))
    fitness = np.zeros(len(xs))
    
    for i, x in enumerate(xs):
        val = evaluateTree(fun_optimal_tree, x)
        if isinstance(val, complex):
            fun_optimal_values[i] = 0.00000001
        else:
            fun_optimal_values[i] = val
            
        val = evaluateTree(fun_generated_tree, x)
        if isinstance(val, complex):
            fun_generated_values[i] = 0.00000001
        else:
            fun_generated_values[i] = val

    fitness = np.square(np.subtract(fun_generated_values,fun_optimal_values))
    
    # mean squared error
    mean_sq_error = mse(fun_optimal_values, fun_generated_values)
    
    #print("mse plot: ", 1/(1+mean_sq_error))
    
    # plot optimal and actual graphs
    plt.figure(figsize=(15,9))
    plt.subplot(2,1,1)
    plt.plot(xs, fun_optimal_values, 'o', label="Optimal")
    plt.plot(xs, fun_generated_values, 'o', label="Actual")
    ax = plt.gca()
    for label in ax.get_xticklabels():
        label.set_fontsize(5)
    plt.legend()

    plt.subplot(2,1,2)
    plt.plot(xs, fitness, 'o')
    plt.title("Squared difference between optimal and actual values")
    plt.tight_layout()
    ax = plt.gca()
    for label in ax.get_xticklabels():
        label.set_fontsize(5)
    plt.show()
    
    
def mse(desired_output, output):
    return np.square(np.subtract(desired_output, output)).mean() 


def fitness_func(ga_instance, solution, solution_idx):
    # Convert the solution array into an expression tree
    solution_tree = arrayToTree(solution)
    #print()
    # Evaluate the tree with the input data
    predicted_output = [evaluateTree(solution_tree, x) for x in xs]
    desired_output = [evaluateTree(fun_optimal_tree, x) for x in xs]

    # Calculate the mean squared error
    mse = np.mean((np.array(predicted_output) - np.array(desired_output))**2)

    # Return the fitness value (the reciprocal of the error)
    #print("mse fit: ", 1.0 / (1 + mse))
    fitness = 1.0 / (1 + mse)

    # If the fitness value is complex, return its real part
    if isinstance(fitness, complex) and fitness < 0.1:
        return 0.000000001
    # Otherwise, return the fitness value as is
    else:
        return fitness

def generatePopulation():
    global globina, initial_population_size, array_length_true
    
    population = np.full((initial_population_size, array_length_true), np.nan)
    for i in range(0, initial_population_size):
        population[i, :] = treeToArray(generateTree(globina), array_length)
    
    return population

    
def geneticAlgorithm():
    global population
    
    ga_instance = pygad.GA(num_generations=800,
                        num_parents_mating=50,
                        fitness_func=fitness_func,
                        sol_per_pop=100,
                        initial_population=population,
                        gene_type=np.float64,
                        mutation_type=mutation,
                        crossover_type=crossover, 
                        keep_parents=30,
                        mutation_probability=0.09)
                        

    ga_instance.run()
    
    solution_array, solution_fitness, solution_idx = ga_instance.best_solution()
    """print("\nsolution: ", solution_array)
    solution_tree = arrayToTree(solution_array)
    
    plot(fun_optimal_tree, solution_tree, xs)
    ga_instance.plot_fitness()
    print("solution fitness: ", solution_fitness)
    print("\nsolution: ")
    printTree(solution_tree)
    print("\noptimal: ")
    printTree(fun_optimal_tree)
    print("\n")
    """
    return [solution_array, solution_fitness, ga_instance]

if __name__ == "__main__":
    data = pd.read_csv("./datasets/dataset.csv", sep=",")
    equations = data['Equation']
    xs = data['Xs'][0].strip('][').split(', ')
    xs = np.array(xs)
    ys = data['Ys'][0].strip('][').split(', ')
    ys = np.array(ys)
    fun_optimal_tree = buildTree(infix_to_prefix(equations[0]))
    #fun_generated_tree = buildTree(infix_to_prefix(equations[1]))
        
    array_length = 300 ###
    array_length_true = array_length * 2 ###
    desired_output = ys ###
    globina = 0.2 ###
    initial_population_size = 100 ###    
   
    
    #fun_generated_array = treeToArray(fun_generated_tree, array_length)
    fun_optimal_array = treeToArray(fun_optimal_tree, array_length)

    #plot(fun_optimal_tree, fun_generated_tree, xs)
    
    #fitness_func(0, fun_generated_array, 0)
    solution_fitness = 0
    i = 1
    while solution_fitness < 0.6:
        print(i)
        population = generatePopulation()
        """for i, pop in enumerate(population):
            print("\npopulation ", i, ": ")
            printTree(arrayToTree(population[i]))"""

            
        solution_array, solution_fitness, ga_instance = geneticAlgorithm()
        i += 1
        
    print("\nsolution: ", solution_array)
    solution_tree = arrayToTree(solution_array)
    
    plot(fun_optimal_tree, solution_tree, xs)
    ga_instance.plot_fitness()
    print("solution fitness: ", solution_fitness)
    print("\nsolution: ")
    printTree(solution_tree)
    print("\noptimal: ")
    printTree(fun_optimal_tree)
    print("\n")
    
    