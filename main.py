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
Xs = list(data['Xs'])
Ys = data['Ys']


'''sss = "((-x * -4) - 6)"
prefix = i2p.infix_to_prefix(sss)
print(prefix)
drevo = tb.gradi_drevo(prefix)
tb.printTree(drevo)
print('\n')
print(eval.evaluateTree(drevo, 2))'''


for i,x_vrstica in enumerate(Xs):
    eq = i2p.infix_to_prefix(equations[i])
    drevo = tb.gradi_drevo(eq)
    tb.printTree(drevo)
    x_list = x_vrstica.strip('][').split(', ')
    y_list = Ys[i].strip('][').split(', ')
    for j,x in enumerate(x_list):
        print(x)
        print(eval.evaluateTree(drevo, x_list[j]))
    print('\n')



