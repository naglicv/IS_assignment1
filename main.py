import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import pygad
import numpy as np
from scipy.stats import norm
import treebuild as tb
import infixToPrefix

#fitness function
def fitness(ga_instance, solution, solution_idx):
    print('aaa')



data = pd.read_csv("./datasets/dataset.csv", sep=",")
equations = data['Equation']
Xs = data['Xs']
Ys = data['Ys']


for equation in equations:
    eq = infixToPrefix.infix_to_prefix(equation)
    print(infixToPrefix.infix_to_prefix(equation))
    #drevo = tb.gradi_drevo(eq)
    #tb.printTree(drevo)
    print('\n')




print(equation[0])