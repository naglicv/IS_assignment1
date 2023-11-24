const = 1000

def evaluateTree(root, x):
    # Empty tree
    if root is None:
        return 0.0
    if root.left is None and root.right is None:
        if root.value == 'x':
            return float(x)
        elif root.value == '-x':
            return float(-x)
        else:
            return float(root.value)
    
    # evaluate subtrees
    leftSubtree = evaluateTree(root.left, x)
    rightSubtree = evaluateTree(root.right, x)
    
    if root.value == '+':
        return leftSubtree + rightSubtree
    if root.value == '-':
        return leftSubtree - rightSubtree
    if root.value == '*':
        return leftSubtree * rightSubtree
    if root.value == '/':
        return (leftSubtree / rightSubtree) if rightSubtree > 0 else const
    if root.value == '^':
        return pow(leftSubtree, rightSubtree) if leftSubtree > 0 else const
    return "Something went wrong"
