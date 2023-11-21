import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot(expressions):
    # input:    expressions -> expressions in list format
    
    lengths = np.zeros_like(expressions)
    for i, expression in enumerate(expressions):
        lengths[i] = len(expression)
        
    lengths_optimal = np.ones_like(expressions)
    
    plt.subplot(2,1,1)
    plt.plot(lengths_optimal, label="Optimal")
    plt.plot(lengths, label="Actual")
    plt.legend()

    differenceOptimalActual = np.subtract(lengths, lengths_optimal)
    
    plt.subplot(2,1,2)
    plt.plot(-differenceOptimalActual)
    plt.title("Difference between optimal and actual")
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    data = pd.read_csv("./datasets/dataset.csv", sep=",")
    equations = data['Equation']
    plot(equations)