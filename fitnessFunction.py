from tkinter import Y
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from evaluateTree import evaluateTree
from infixToPrefix import infix_to_prefix
from treebuild import *
import time
import pygad

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
    global desired_output, optimal_length
    # Convert the solution array into an expression tree
    solution_tree = arrayToTree(solution)
    
    # Evaluate the tree with the input data
    predicted_output = [evaluateTree(solution_tree, x) for x in xs]

    # Check for non-numeric values in predicted_output and desired_output
    if any(isinstance(i, (complex, str)) for i in predicted_output) or any(isinstance(i, (complex, str)) for i in desired_output):
        return 0

    # Check for invalid values in predicted_output and desired_output
    if any(pd.isna(predicted_output)) or any(pd.isna(desired_output)):
        return 0

    # Check for extremely large values in predicted_output and desired_output
    if any(np.abs(predicted_output) > 1e100) or any(np.abs(desired_output) > 1e100):
        return 0
    
    # Calculate the mean squared error
    try:
        mse = np.mean((np.array(predicted_output) - np.array(desired_output))**2)
    except:
        print("np.array(predicted_output) - np.array(desired_output)", np.array(predicted_output) - np.array(desired_output))
        mse = 1000
    
    penalty_factor = 0.005
    diff = solution[1] - optimal_length
    if diff < 0:
        diff = 0
    length_penalty = diff * penalty_factor

    try:
        fitness = 1.0 / (1 + mse + length_penalty)
    except FloatingPointError:
        fitness = 0.0

    if isinstance(fitness, complex) and fitness < 0.1:
        return 0
    else:
        return fitness

def generatePopulation():
    global globina, initial_population_size, array_length_true
    
    population = np.full((initial_population_size, array_length_true), np.nan)
    for i in range(0, initial_population_size):
        population[i, :] = treeToArray(generateTree(globina), array_length)
    
    return population

def genind(instance):
    global iii
    print(iii)
    iii += 1
    
def geneticAlgorithm():
    global population

    ga_instance = pygad.GA(num_generations=100,
                        num_parents_mating=15,
                        fitness_func=fitness_func,
                        initial_population=population,
                        on_generation=genind,
                        parent_selection_type="tournament",
                        gene_type=np.float64,
                        mutation_type=mutation,
                        crossover_type=crossover, 
                        #keep_parents=30,
                        mutation_probability=0.09)
                        

    ga_instance.run()
    
    solution_array, solution_fitness, solution_idx = ga_instance.best_solution()
    return [solution_array, solution_fitness, ga_instance]

def simplifyTree(node):
    const_large = str(1000)
    const_small = str(0.000000001)
    if node is None:
        return None

    # Recursively simplify the children
    node.left = simplifyTree(node.left)
    node.right = simplifyTree(node.right)
        
    if is_float(node.value) or node.value == 'x' or node.value == '-x':
        return node
    
    # If both children are numbers, evaluate the expression
    if is_float(node.right.value) and is_float(node.left.value):
        if node.value == '+':
            try:
                node.value = str(float(node.left.value) + float(node.right.value))
            except:
                node.value = const_large
        elif node.value == '-':
            try:
                node.value = str(float(node.left.value) - float(node.right.value))
            except:
                node.value = const_large
        elif node.value == '*':
            try:
                node.value = str(float(node.left.value) * float(node.right.value))
            except:
                node.value = const_large
        elif node.value == '/':
            try:
                if float(node.right.value) != 0:  # Avoid division by zero
                    node.value = str(float(node.left.value) / float(node.right.value))
                else:
                    node.value = const_large
            except:
                node.value = const_small
        elif node.value == '^':
            if float(node.left.value) == 0 and float(node.right.value) != 0:
                node.value = str(0)
            elif float(node.left.value) == 0 and float(node.right.value) == 0:
                node.value = const_large
            # Check if the values are within a certain range before calculating the power
            else:
                try:
                    node.value = str(pow(float(node.left.value), float(node.right.value)))  # Return a default value
                except:
                    node.value = const_large
                    
        node.left = None
        node.right = None

    elif (node.left.value == 'x' and node.right.value == 'x') or (node.left.value == '-x' and node.right.value == '-x'):
        if node.value == '-':
            node.value = str(0)
            node.left = None
            node.right = None
        elif node.value == '/':
            node.value = str(1)
            node.left = None
            node.right = None
            
    elif (node.left.value == '-x' and node.right == 'x') or (node.left.value == 'x' and node.right.value == '-x'):
        if node.value == '+':
            node.value = str(0)
            node.left = None
            node.right = None
        elif node.value == '/':
            node.value = str(-1)
            node.left = None
            node.right = None
            
    elif (is_float(node.left.value) and float(node.left.value) == 0 and not is_float(node.right.value)) or \
        (is_float(node.right.value) and float(node.right.value) == 0 and not is_float(node.left.value)):
        if node.value in ['+', '-']:
            node = node.right if is_float(node.right.value) else node.left
        elif node.value == '^' and is_float(node.right.value):
            node.value = str(1)
            node.left = None
            node.right = None
            
    elif (is_float(node.left.value) and float(node.left.value) == 1 and is_float(node.right.value)) or \
        (is_float(node.right.value) and float(node.right.value) == 1 and is_float(node.left.value)):
        if node.value == '*':
            node = node.right if is_float(node.right.value) else node.left
        elif node.value == '^' and is_float(node.right.value):
            node = node.left

        

    return node
    
if __name__ == "__main__":
    data = pd.read_csv("./datasets/dataset.csv", sep=",")
    equations = data['Equation']
    xs = data['Xs'][0].strip('][').split(', ')
    xs = np.array(xs)
    ys = data['Ys'][0].strip('][').split(', ')
    ys = np.array(ys)
    fun_optimal_tree = buildTree(infix_to_prefix(equations[3]))
        
    array_length = 600 ###
    array_length_true = array_length * 2 ###
    desired_output = ys ###
    globina = 0.2 ###
    initial_population_size = 100 ###   
   
    fun_optimal_array = treeToArray(fun_optimal_tree, array_length)
    optimal_length = fun_optimal_array[1]
    desired_output = [evaluateTree(fun_optimal_tree, x) for x in xs]

    #števec iteracije algoritma
    iii = 0
    population = generatePopulation()

    before = time.perf_counter()
        
    solution_array, solution_fitness, ga_instance = geneticAlgorithm()

    after = time.perf_counter()

    timeDiff = after - before
    
    print("\nsolution: ", solution_array)
    solution_tree = arrayToTree(solution_array)
    
    ga_instance.plot_fitness()
    plot(fun_optimal_tree, solution_tree, xs)
    
    
    print("solution fitness: ", solution_fitness)
    print("\nsolution: ")
    printTree(solution_tree)
    simple = simplifyTree(solution_tree)
    plot(fun_optimal_tree, simple, xs)
    print("\nsolution simplified: ")
    printTree(simple)
    print("\noptimal: ")
    printTree(fun_optimal_tree)
    print("\n")
    print(timeDiff)