import pygad
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import infixToPrefix as itp


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def gradi_drevo(expression):
    if expression[0] == '*' and expression[1] == '*':
        root = Node('**')
        expression.pop(0)
    else:
        root = Node(expression[0])
    expression.pop(0)
    if root.value.isnumeric() or root.value.isalpha():
        return root

    root.left = gradi_drevo(expression)
    root.right = gradi_drevo(expression)

    return(root)

def printTree(root):
    if (root != None):
        print(root.value, end = "")
        printTree(root.left)
        printTree(root.right)
        

sss = "((x+y)**z)/w+u"
drevo = gradi_drevo(itp.infix_to_prefix(sss))

printTree(drevo)
