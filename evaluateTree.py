def evaluateTree(root):
    # Empty tree
    if root is None:
        return 0.0
    if root.left is None and root.right is None:
        return float(root.value)
    
    # evaluate subtrees
    leftSubtree = evaluateTree(root.left)
    rightSubtree = evaluateTree(root.right)
    
    if root.value == '+':
        return leftSubtree + rightSubtree
    if root.value == '-':
        return leftSubtree - rightSubtree
    if root.value == '*':
        return leftSubtree * rightSubtree
    if root.value == '/':
        return leftSubtree / rightSubtree
    if root.value == '**':
        return pow(leftSubtree, rightSubtree)
    return "Something went wrong"
