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
    if root.value == '^':
        if leftSubtree == 0 and rightSubtree != 0:
            return 0
        elif leftSubtree == 0 and rightSubtree == 0:
            return const
        # Check if the values are within a certain range before calculating the power
        else:
            try:
                """print("leftSubtree: ", leftSubtree)
                print("rightSubtree: ", rightSubtree)"""
                return pow(leftSubtree, rightSubtree)  # Return a default value
            except:
                return const
    return "Something went wrong"


