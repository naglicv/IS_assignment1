def evaluateTree(root, x):
    # Empty tree
    if root is None:
        return 0.0
    if root.value == 'x':
        root.value = float(x)
    elif root.value == '-x':
        root.value = float(-x)
    if root.left is None and root.right is None:
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
        return leftSubtree / rightSubtree
    if root.value == '^':
        return pow(leftSubtree, rightSubtree)
    return "Something went wrong"
