import pygad
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import infixToPrefix as itp
import re
import random
import evaluateTree as eval
import infixToPrefix as i2p

konstanta = 1.e-10

#ustvari strukturo node (vozlišče) drevesa
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def buildTree(expression):
    root = Node(expression[0])
    expression.pop(0)
    if root.value.lstrip('-+').isnumeric() or root.value.lstrip('-+').isalpha():
        return root

    root.left = buildTree(expression)
    root.right = buildTree(expression)

    return(root)

def printTree(root):
    if (root != None):
        print(root.value, end = "")
        print(end =" ")
        printTree(root.left)
        print(end =" ")
        printTree(root.right)


def generateExpression(globina):
    rng = np.random.default_rng()
    operatorji = ['+', '-', '*', '/', '^']
    operandi = list(range(-10,10))
    spremenljivka = ['x', '-x']
    rand = int(rng.random()*10) + (0.2 * globina)
    if rand <= 5:
        expression = operatorji[int(rng.random() * 5 - konstanta)]
    elif rand <= 7:
        expression = spremenljivka[int(rng.random() * 2 - konstanta)]
    else:
        expression = str(operandi[int(rng.random() * 19 - konstanta)])
    return expression


def generateTree(globina):
    expression = generateExpression(globina)
    root = Node(expression)
    if root.value.lstrip('-+').isnumeric() or root.value.lstrip('-+').isalpha():
        return root
    root.left = generateTree(globina+1)
    root.right = generateTree(globina+1)
    return root


def countTree(root):
    count = 0
    if root != None:
        count += 1
        count += countTree(root.left)
        count += countTree(root.right)
    return count


def poddrevo_gen(node, target, index=1):
    if node is None:
        return None
    if index == target:
        return node

    l_poddrevo = poddrevo_gen(node.left, target, 2 * index)
    d_poddrevo = poddrevo_gen(node.right, target, 2 * index + 1)
    return l_poddrevo or d_poddrevo


def crossover(tree1, tree2):
    crossover_point = random.randint(1, min(countTree(tree1), countTree(tree2)))

    poddrevo1 = poddrevo_gen(tree1, crossover_point)
    poddrevo2 = poddrevo_gen(tree2, crossover_point)

    if poddrevo1 is not None and poddrevo2 is not None:
        poddrevo1.left, poddrevo2.left = poddrevo2.left, poddrevo1.left
        poddrevo1.right, poddrevo2.right = poddrevo2.right, poddrevo1.right
        poddrevo1.value, poddrevo2.value = poddrevo2.value, poddrevo1.value


def mutation(tree):
    mutation_point = random.randint(1, countTree(tree))
    operatorji = ['+', '-', '*', '/', '^']
    poddrevo = poddrevo_gen(tree, mutation_point)
    if poddrevo.value in operatorji:
        poddrevo.value = operatorji[random.randint(0, len(operatorji))]
    else:
        operandi = list(range(-10,10))
        operandi.extend(['x', '-x'])
        poddrevo.value = operandi[random.randint(0, len(operandi))]



'''X = []

for i in range(20):
    drevo = generateTree(0)
    X.append(drevo)

for i in range(19):
    crossover(X[i], X[i+1])

for i in range(20):
    try:
        print(eval.evaluateTree(X[i], 10))
    except:
        print(1.e10)'''
    
