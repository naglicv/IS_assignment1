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
        fun_optimal_values[i] = evaluateTree(fun_optimal_tree, x)
        fun_generated_values[i] = evaluateTree(fun_generated_tree, x)

    fitness = np.square(np.subtract(fun_generated_values,fun_optimal_values))
    
    # mean squared error
    mean_sq_error = mse(fun_optimal_values, fun_generated_values)
    
    print("mse plot: ", 1/(1+mean_sq_error))
    
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

    # Evaluate the tree with the input data
    predicted_output = [evaluateTree(solution_tree, x) for x in xs]
    desired_output = [evaluateTree(fun_optimal_tree, x) for x in xs]

    # Calculate the mean squared error
    mse = np.mean((np.array(predicted_output) - np.array(desired_output))**2)

    # Return the fitness value (the reciprocal of the error)
    print("mse fit: ", 1.0 / (1 + mse))
    return 1.0 / (1 + mse)
    
if __name__ == "__main__":
    data = pd.read_csv("./datasets/dataset.csv", sep=",")
    equations = data['Equation']
    xs = data['Xs'][0].strip('][').split(', ')
    xs = np.array(xs)
    ys = data['Ys'][0].strip('][').split(', ')
    ys = np.array(ys)
    fun_optimal_tree = buildTree(infix_to_prefix(equations[0]))
    fun_generated_tree = buildTree(infix_to_prefix(equations[1]))
    
    fun_generated_array = treeToArray(fun_generated_tree, 200)
    fun_optimal_array = treeToArray(fun_optimal_tree, 200)

    plot(fun_optimal_tree, fun_generated_tree, xs)
    
    desired_output = ys
    
    fitness_func(0, fun_generated_array, 0)