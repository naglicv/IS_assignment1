from treebuild import printTree
import math

const = 1000000

def evaluateTree(root, x):
    # Empty tree
    if root is None:
        return 0.0
    if root.left is None and root.right is None:
        if root.value == 'x':
            return float(x)
        elif root.value == '-x':
            return float(-float(x))
        else:
            return float(root.value)
     
    # evaluate subtrees
    leftSubtree = evaluateTree(root.left, x)
    rightSubtree = evaluateTree(root.right, x)
    
    if root.value == '+':
        # Check for extremely large values in leftSubtree and rightSubtree
        if abs(leftSubtree) > 10000000 or abs(rightSubtree) > 10000000:
            return const
        else:
            return leftSubtree + rightSubtree
    if root.value == '-':
        try:
            return leftSubtree - rightSubtree
        except:
            return const
    if root.value == '*':
        try:
            return leftSubtree * rightSubtree
        except OverflowError:
            return const
    if root.value == '/':
        try:
            return (leftSubtree / rightSubtree) if rightSubtree != 0 else const
        except:
            return 0.000001
    if root.value == '&':
        try:
            return math.log(rightSubtree, leftSubtree)
        except:
            return 0
    if root.value == '^':
        if leftSubtree == 0 and rightSubtree != 0:
            return 0
        elif leftSubtree == 0 and rightSubtree == 0:
            return const
        else:
            try:
                return pow(leftSubtree, rightSubtree)
            except:
                return const
    return "Something went wrong"


