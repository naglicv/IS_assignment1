def infix_to_prefix(infix):
    infix = infix.replace(" ", "")
    infix = infix.replace("**", "^")
    # Function to convert infix to prefix expression
    def precedence(op):
        # Returns the precedence of the operator
        if op in ['+', '-']:
            return 1
        if op in ['*', '/']:
            return 2
        if op in ['^']:
            return 3
        return 0

    def is_operator(op):
        # Returns true if the operator is an operator
        return op in ['+', '-', '*', '/', '^']

    stack = []
    output = []
    for token in reversed(infix):
        if is_operator(token):
            while stack and precedence(token) < precedence(stack[-1]):
                output.append(stack.pop())
            stack.append(token)
        elif token == ')':
            stack.append(token)
        elif token == '(':
            while stack[-1] != ')':
                output.append(stack.pop())
            stack.pop()
        else:
            output.append(token)

    while stack:
        output.append(stack.pop())

    output.reverse()
    return output

if __name__ == '__main__':
    s = "((x+y )** z)/ w+u"
    print(infix_to_prefix(s))
