import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from evaluateTree import evaluateTree
from infixToPrefix import infix_to_prefix
from treebuild import *
from matplotlib.ticker import FuncFormatter

def plot(fun_optimal_tree, fun_generated_tree, xs):
    
    fun_optimal_values = np.zeros(len(xs))
    fun_generated_values = np.zeros(len(xs))
    fitness = np.zeros(len(xs))
    
    for i, x in enumerate(xs):
        fun_optimal_values[i] = evaluateTree(fun_optimal_tree, x)
        fun_generated_values[i] = evaluateTree(fun_generated_tree, x)

    fitness = np.power(np.subtract(fun_optimal_values, fun_generated_values), 2)
    
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
    
    
if __name__ == "__main__":
    data = pd.read_csv("./datasets/dataset.csv", sep=",")
    equations = data['Equation']
    xs = data['Xs'][0].strip('][').split(', ')
    xs = np.array(xs)
    fun_optimal_tree = buildTree(infix_to_prefix(equations[0]))
    fun_generated_tree = buildTree(infix_to_prefix(equations[2]))

    plot(fun_optimal_tree, fun_generated_tree, xs)