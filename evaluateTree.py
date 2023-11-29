from treebuild import printTree

const = 1000

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
    
    """
    print("------------------------------------------\nROOT:")
    printTree(root)
    
    print("\n\nroot.left:")
    printTree(root.left)
    print("\n\nx: ", x)
    print("root.right:")
    printTree(root.right)
    print("\n\nx: ", x)
    """
    
    # evaluate subtrees
    leftSubtree = evaluateTree(root.left, x)
    rightSubtree = evaluateTree(root.right, x)
    
    """
    print("\n\nleftSubtree: ", leftSubtree)
    print("rightSubtree: ", rightSubtree)
    """ 
    if root.value == '+':
        return leftSubtree + rightSubtree
    if root.value == '-':
        return leftSubtree - rightSubtree
    if root.value == '*':
        return leftSubtree * rightSubtree
    if root.value == '/':
        return (leftSubtree / rightSubtree) if rightSubtree != 0 else const
    if root.value == '^':
        # Check if the values are within a certain range before calculating the power
        if (abs(leftSubtree) > 100 and abs(rightSubtree) > 3) or abs(rightSubtree) > 10:
            return 0  # Return a default value
        else:
            return pow(leftSubtree, rightSubtree) if leftSubtree != 0 else 0
    return "Something went wrong"


