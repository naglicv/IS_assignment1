import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import pygad
import numpy as np
from scipy.stats import norm

#fitness function
def fitness(ga_instance, solution, solution_idx):
    print('aaa')



data = pd.read_csv("./datasets/dataset.csv", sep=",")
equation = data['Equation']
Xs = data['Xs']
Ys = data['Ys']




print(equation[0])