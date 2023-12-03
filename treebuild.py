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
#from fitnessFunction import simplifyTree


konstanta = 1.e-10
array_length = 800

#ustvari strukturo node (vozlišče) drevesa
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


#zgradi drevo na podlagi prefiksne oblike enačbe
def buildTree(expression):
    if len(expression) > 0:  # Check if there are elements in the list
        root = Node(expression[0])
        expression.pop(0)
        if is_float(root.value) or root.value.lstrip('-+').isalpha():
            return root

        root.left = buildTree(expression)
        root.right = buildTree(expression)
    else:
        root = None
        
    return(root)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

#izpis drevesa
def printTree(root):
    string = ""
    if (root != None):
        string = root.value
        print(root.value, end = "")
        string += printTree(root.left)
        string += printTree(root.right)
    return string


#generiraj random expression (tree value)
def generateExpression(globina):
    rng = np.random.default_rng()
    operatorji = ['+', '-', '*', '/', '^']
    operandi = list(range(-10,10))
    spremenljivka = ['x', '-x']
    rand = rng.random()*10 + (0.2 * globina)
    if rand <= 4.5:
        expression = operatorji[random.randint(0, len(operatorji)-1)]
    elif rand <= 7:
        expression = spremenljivka[random.randint(0, 1)]
    else:
        expression = str(operandi[random.randint(0, len(operandi)-1)])
    return expression


#generiraj random drevo
"""def generateTree(globina):
    expression = generateExpression(globina)
    root = Node(expression)
    if root.value.lstrip('-+').isnumeric() or root.value.lstrip('-+').isalpha():
        return root
    root.left = generateTree(globina+1)
    root.right = generateTree(globina+1)
    return root"""

def generateTree(globina, is_root=True):
    expression = generateExpression(globina)
    # If the expression is empty and this is the root of the tree, create a node with a value of 0
    if not expression and is_root:
        return Node(0)
    # If the expression is empty and this is not the root, return None
    elif not expression:
        return None
    root = Node(expression)
    if root.value.lstrip('-+').isnumeric() or root.value.lstrip('-+').isalpha():
        return root
    root.left = generateTree(globina+0.5, is_root=False) ############# change back to globina+1
    root.right = generateTree(globina+0.5, is_root=False) ############# change back to globina+1
    return root

# pretvori drevo v array
def treeToArray(root, array_length):
    # Initialize the array with [0, 0]
    arr = [[0, 0] for _ in range(array_length)]
    arr = np.array(arr)
    #root = simplifyTree(root)
    
    # List of operators
    operators = ['+', '-', '*', '/', '^'] 
    
    # Helper function to recursively traverse the tree
    def traverse(node, index):
        if node is None:
            index -= 1
            return index
        
        if node.value.lstrip('-+').isnumeric():
            # If the node is a number, store [0, number]
            arr[index] = [0, int(node.value)]
        elif node.value == 'x':
            # If the node is 'x', store [2, x]
            arr[index] = [2, 0]
        elif node.value == '-x':
            # If the node is '-x', store [2, -x]
            arr[index] = [2, 1]
        elif node.value in operators:
            # If the node is an operator, store [1, index of operator]
            arr[index] = [1, operators.index(node.value)]
        
        # Traverse the left and right children
        index = traverse(node.left, index + 1)
        index = traverse(node.right, index + 1)
        
        return index
    
    # Count the number of nodes and store it in the first element
    
    try:
        num_nodes = traverse(root, 1)
    except:
        num_nodes = 0
    arr[0] = [-1, num_nodes+1]
    
    arr = arr.flatten()
    #print(arr)
    return arr

def isOperator(op):
    # Returns true if the operator is an operator
    if op in ['+', '-', '*', '/', '^']:
        return 1
    else:
        return 0
        
#preštej število vozlšč v drevesu
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
    if index >= target:
        return node

    l_poddrevo = poddrevo_gen(node.left, target, index+1)
    d_poddrevo = poddrevo_gen(node.right, target, index + 1 + countTree(node.left))
    return l_poddrevo or d_poddrevo


def crossover(parents, offspring_size, instance):
    offspring = []
    num_parents = len(parents)
    while len(offspring) < offspring_size[0]:
        # Select two parents
        arr1 = parents[random.randint(0, num_parents-1)]
        arr2 = parents[random.randint(0, num_parents-1)]
        tree1 = arrayToTree(arr1)
        tree2 = arrayToTree(arr2)
        
        tree_count1 = countTree(tree1)
        tree_count2 = countTree(tree2)
        crossover_point1 = random.randint(1, min(array_length/2-1, tree_count1)) if tree_count1 > 1 else 1
        crossover_point2 = random.randint(1, min(array_length/2-1, tree_count2)) if tree_count2 > 1 else 1

        poddrevo1 = poddrevo_gen(tree1, crossover_point1)
        poddrevo2 = poddrevo_gen(tree2, crossover_point2)

        if poddrevo1 is not None and poddrevo2 is not None:
            poddrevo1.left, poddrevo2.left = poddrevo2.left, poddrevo1.left
            poddrevo1.right, poddrevo2.right = poddrevo2.right, poddrevo1.right
            poddrevo1.value, poddrevo2.value = poddrevo2.value, poddrevo1.value

        # Add the offspring to the list
        offspring.append(treeToArray(tree1, array_length)) ###############################################
        # If there is room for another offspring, add it
        if len(offspring) < offspring_size[0]:
            offspring.append(treeToArray(tree2, array_length)) ###############################################

    return np.array(offspring) 

def mutation(offspring, instance):
    for idx, arr in enumerate(offspring):
        tree = arrayToTree(arr)
        tree_count = countTree(tree)
        if tree_count > 1:
            mutation_point = random.randint(1, tree_count)
        else:
            mutation_point = 1  # or some other default value
            
        operators = ['+', '-', '*', '/', '^']
        subtree = poddrevo_gen(tree, mutation_point)
        if subtree is not None:
            if subtree.value in operators:
                subtree.value = operators[random.randint(0, len(operators) - 1)]
            else:
                operands = list(range(-10,10))
                operands.extend(['x', '-x'])
                subtree.value = str(operands[random.randint(0, len(operands) - 1)])
            offspring[idx] = treeToArray(tree, array_length) ###############################################
    return offspring


def arrayToTree(array):
    prefix = []
    dolzina = array[1]
    operatorji = ['+', '-', '*', '/', '^']
    x = ['x', '-x']
    for i in range(2, 2*int(dolzina), 2):
        if array[i] == 0:
            prefix.append(str(array[i+1]))
        elif array[i] == 1:
            prefix.append(operatorji[int(array[i+1])])
        elif array[i] == 2:
            prefix.append(x[int(array[i+1])])
    return buildTree(prefix)    


if __name__ == '__main__':
    """#drevo = generateTree(0)
    #bbb = printTree(drevo)
    array = [[-1,4],[1,2],[2,1],[0,5]]

    kk = arrayToTree(array)
    printTree(kk)

    globina = 4
    tree = generateTree(globina)
    printTree(tree)
    print("\n")
    arr = treeToArray(tree, 100)
    print("arr: ", arr)
    tree1 = arrayToTree(arr)
    print("tree: ")
    printTree(tree)
    print("\ntree1: ")
    printTree(tree1)
    """

    tree = buildTree(['^', '*', '-6.0', '-6.0', '-x'])
    print(hasX(tree))
    