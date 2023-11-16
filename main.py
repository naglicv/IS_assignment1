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
'''def fitness(ga_instance, y, solution_idx):
    value = eval.evaluateTree(tb.gradi_drevo(i2p.infix_to_prefix(equations)))
    realvalue = Ys
    return realvalue - value
    print('aaa')'''



data = pd.read_csv("./datasets/dataset.csv", sep=",")
equations = data['Equation']
Xs = data['Xs']
Ys = data['Ys']


'''sss = "((-x * -4) - 6)"
prefix = i2p.infix_to_prefix(sss)
print(prefix)
drevo = tb.gradi_drevo(prefix)
tb.printTree(drevo)
print('\n')
print(eval.evaluateTree(drevo, 2))'''


for equation in equations:
    print(equation + ':')
    eq = i2p.infix_to_prefix(equation)
    drevo = tb.gradi_drevo(eq)
    tb.printTree(drevo)
    print('\n')



