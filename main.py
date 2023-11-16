import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import pygad
import numpy as np
from scipy.stats import norm
import treebuild as tb
import infixToPrefix as i2p
import evaluateTree as eval

#fitness function
def fitness(ga_instance, solution, solution_idx):
    print('aaa')



data = pd.read_csv("./datasets/dataset.csv", sep=",")
equations = data['Equation']
Xs = data['Xs']
Ys = data['Ys']


sss = "(((1+2)**3)/2+1)"
drevo = tb.gradi_drevo(i2p.infix_to_prefix(sss))
tb.printTree(drevo)
print(eval.evaluateTree(drevo))

'''for equation in equations:
    eq = i2p.infix_to_prefix(equation)
    print(i2p.infix_to_prefix(equation))
    #drevo = tb.gradi_drevo(eq)
    #tb.printTree(drevo)
    print('\n')'''

