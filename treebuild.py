import pygad
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def gradi_drevo(expression):
    root = Node(expression[0])
    expression.pop(0)
    if root.value.isnumeric() or root.value.isalpha():
        return root

    root.left = gradi_drevo(expression)
    root.right = gradi_drevo(expression)

    return(root)

def printTree(root):
    if (root != None):
        printTree(root.left)
        printTree(root.right)
        print(root.value, end = "")

drevo = gradi_drevo(['-','+','2','*','3','4','5'])

printTree(drevo)
