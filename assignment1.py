class nptr:
   
    # Constructor to set the data of
    # the newly created tree node
    def __init__(self, c):
        self.data = c
        self.left = None
        self.right = None
 
# Function to create new node
def newNode(c):
    n = nptr(c)
    return n
 
# Function to build Expression Tree
def build(s):
   
    # Stack to hold nodes
    stN = []
 
    # Stack to hold chars
    stC = []
 
    # Prioritising the operators
    p = [0]*(123)
    p[ord('+')] = p[ord('-')] = 1
    p[ord('/')] = p[ord('*')] = 2
    p[ord('^')] = 3
    p[ord(')')] = 0
 
    for i in range(len(s)):
        if (s[i] == '('):
            # Push '(' in char stack
            stC.append(s[i])
 
        # Push the operands in node stack
        elif (s[i].isnumeric()):
            t = newNode(s[i])
            stN.append(t)
        elif (p[ord(s[i])] > 0):
           
            # If an operator with lower or
            # same associativity appears
            while (len(stC) != 0 and stC[-1] != '(' and ((s[i] != '^' and p[ord(stC[-1])] >= p[ord(s[i])])
                    or (s[i] == '^'and
                    p[ord(stC[-1])] > p[ord(s[i])]))):
               
                # Get and remove the top element
                # from the character stack
                t = newNode(stC[-1])
                stC.pop()
 
                # Get and remove the top element
                # from the node stack
                t1 = stN[-1]
                stN.pop()
 
                # Get and remove the currently top
                # element from the node stack
                t2 = stN[-1]
                stN.pop()
 
                # Update the tree
                t.left = t2
                t.right = t1
 
                # Push the node to the node stack
                stN.append(t)
 
            # Push s[i] to char stack
            stC.append(s[i])
             
        elif (s[i] == ')'):
            while (len(stC) != 0 and stC[-1] != '('):
                t = newNode(stC[-1])
                stC.pop()
                t1 = stN[-1]
                stN.pop()
                t2 = stN[-1]
                stN.pop()
                t.left = t2
                t.right = t1
                stN.append(t)
            stC.pop()
    t = stN[-1]
    return t
 
# Function to print the post order
# traversal of the tree
def postorder(root):
    if (root != None):
        postorder(root.left)
        postorder(root.right)
        print(root.data, end = "")
 
s = "(3*5-2*6)"
s = "(" + s
s += ")"
root = build(s)
 
# Function call
postorder(root)
 
# This code is contributed by divyeshrabadiya07.