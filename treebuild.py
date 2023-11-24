import pygad
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import infixToPrefix as itp
import re

const = 1.e-10

#ustvari strukturo node (vozlišče) drevesa
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def gradi_drevo(expression):
    root = Node(expression[0])
    expression.pop(0)
    if root.value.lstrip('-+').isnumeric() or root.value.lstrip('-+').isalpha():
        return root

    root.left = gradi_drevo(expression)
    root.right = gradi_drevo(expression)

    return(root)

def printTree(root):
    if (root != None):
        print(root.value, end = "")
        printTree(root.left)
        printTree(root.right)


def generateExpression(globina):
    rng = np.random.default_rng()
    operatorji = ['+', '-', '*', '/', '^']
    operandi = list(range(-10,10))
    spremenljivka = ['x', '-x']
    rand = int(rng.random()*10) + (0.2 * globina)
    if rand <= 5:
        expression = operatorji[int(rng.random() * 5 - const)]
    elif rand <= 7:
        expression = spremenljivka[int(rng.random() * 2 - const)]
    else:
        expression = str(operandi[int(rng.random() * 19 - const)])
    return expression



def generateTree(globina):
    expression = generateExpression(globina)
    root = Node(expression)
    if root.value.lstrip('-+').isnumeric() or root.value.lstrip('-+').isalpha():
        return root
    root.left = generateTree(globina+1)
    root.right = generateTree(globina+1)
    return root


X = []
for i in range (20):
    drevo = generateTree(0)
    X.append(drevo)
    printTree(drevo)
    print()
    
